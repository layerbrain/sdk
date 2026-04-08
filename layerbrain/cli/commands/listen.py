"""Live webhook event listener for the Layerbrain CLI."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse, urlunparse

import httpx
import typer
import websockets

from layerbrain import Layerbrain
from layerbrain.cli._output import console, print_error, print_json
from layerbrain.exceptions import LayerbrainError


@dataclass(frozen=True)
class ListenConfig:
    websocket_url: str
    websocket_headers: dict[str, str]
    events: str | None
    forward_to: str | None
    forward_headers: dict[str, str]
    forward_secret: str | None
    print_json: bool
    skip_verify: bool
    print_secret: bool


def _parse_events(events: str | None) -> str | None:
    if not events:
        return None
    normalized = ",".join(part.strip() for part in events.split(",") if part.strip())
    return normalized or None


def _normalize_forward_url(value: str) -> str:
    if "://" not in value:
        return f"http://{value}"
    return value


def _parse_forward_headers(values: list[str] | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    for value in values or []:
        if ":" not in value:
            raise typer.BadParameter(
                f"Invalid --header value '{value}'. Use the form 'Name: Value'."
            )
        name, raw_header_value = value.split(":", 1)
        name = name.strip()
        header_value = raw_header_value.strip()
        if not name or not header_value:
            raise typer.BadParameter(
                f"Invalid --header value '{value}'. Use the form 'Name: Value'."
            )
        headers[name] = header_value
    return headers


def _merge_forward_url(base_url: str, webhook_url: str | None) -> str:
    if not webhook_url:
        return base_url

    base = urlparse(base_url)
    remote = urlparse(webhook_url)
    if (base.path and base.path != "/") or not remote.path or remote.path == "/":
        return base_url

    merged = base._replace(path=remote.path, query=remote.query)
    return urlunparse(merged)


def _generate_forward_secret() -> str:
    return f"whsec_{secrets.token_urlsafe(32)}"


def _build_signature_header(body: bytes, secret: str, timestamp: int | None = None) -> str:
    signature_timestamp = timestamp or int(time.time())
    signed_payload = f"{signature_timestamp}.".encode() + body
    digest = hmac.new(
        secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    return f"t={signature_timestamp},v1={digest}"


def _build_listen_config(
    *,
    events: str | None,
    forward_to: str | None,
    header_values: list[str] | None,
    print_json_output: bool,
    skip_verify: bool,
    print_secret_value: bool,
    load_from_webhooks_api: str | None,
) -> ListenConfig:
    normalized_events = _parse_events(events)
    normalized_forward_to = _normalize_forward_url(forward_to) if forward_to else None
    forward_headers = _parse_forward_headers(header_values)

    with Layerbrain() as client:
        if load_from_webhooks_api:
            webhook = client.webhooks.retrieve(load_from_webhooks_api)
            if not normalized_events:
                enabled_events = webhook.get("enabled_events") or []
                normalized_events = ",".join(enabled_events) if enabled_events else None
            if normalized_forward_to:
                normalized_forward_to = _merge_forward_url(
                    normalized_forward_to,
                    webhook.get("url"),
                )

        websocket_url, websocket_headers = client.webhooks.listen_request(events=normalized_events)

    forward_secret = _generate_forward_secret() if normalized_forward_to else None
    return ListenConfig(
        websocket_url=websocket_url,
        websocket_headers=websocket_headers,
        events=normalized_events,
        forward_to=normalized_forward_to,
        forward_headers=forward_headers,
        forward_secret=forward_secret,
        print_json=print_json_output,
        skip_verify=skip_verify,
        print_secret=print_secret_value,
    )


def _event_label(event: dict[str, Any]) -> str:
    event_type = str(event.get("type") or "event")
    event_id = str(event.get("id") or "-")
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp}  --> {event_type} [{event_id}]"


async def _forward_event(
    client: httpx.AsyncClient,
    *,
    target_url: str,
    payload: dict[str, Any],
    extra_headers: dict[str, str],
    secret: str,
) -> tuple[int, str, int]:
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Layerbrain-Signature": _build_signature_header(body, secret),
        **extra_headers,
    }
    started = time.perf_counter()
    response = await client.post(
        target_url,
        content=body,
        headers=headers,
    )
    duration_ms = int((time.perf_counter() - started) * 1000)
    return response.status_code, response.reason_phrase, duration_ms


async def _consume_events(config: ListenConfig) -> None:
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=httpx.Timeout(10.0, connect=5.0),
        verify=not config.skip_verify,
    ) as forward_client:
        backoff_seconds = 1.0

        while True:
            try:
                async with websockets.connect(
                    config.websocket_url,
                    additional_headers=config.websocket_headers,
                    ping_interval=20,
                    ping_timeout=20,
                    max_size=None,
                ) as websocket:
                    backoff_seconds = 1.0
                    async for raw_message in websocket:
                        message = (
                            raw_message.decode("utf-8")
                            if isinstance(raw_message, bytes)
                            else raw_message
                        )
                        payload = json.loads(message)

                        if config.forward_to and config.forward_secret:
                            status_code, reason, duration_ms = await _forward_event(
                                forward_client,
                                target_url=config.forward_to,
                                payload=payload,
                                extra_headers=config.forward_headers,
                                secret=config.forward_secret,
                            )
                            if config.print_json:
                                print_json(payload)
                            else:
                                console.print(
                                    f"{_event_label(payload)} -> "
                                    f"{status_code} {reason} ({duration_ms}ms)"
                                )
                            continue

                        if config.print_json:
                            print_json(payload)
                        else:
                            console.print(_event_label(payload))
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print_error(
                    f"listen disconnected ({exc}). Reconnecting in {int(backoff_seconds)}s."
                )
                await asyncio.sleep(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, 30.0)


async def _run_listen(config: ListenConfig) -> None:
    if config.forward_secret and (config.print_secret or not config.print_json):
        console.print(f"[cyan]Forward signing secret:[/cyan] {config.forward_secret}")
    if not config.print_json:
        console.print(f"[dim]Connecting to {config.websocket_url}[/dim]")
    await _consume_events(config)


def listen(
    events: str | None = typer.Option(
        None,
        "--events",
        help="Comma-separated event types to stream. Omit to receive all events.",
    ),
    forward_to: str | None = typer.Option(
        None,
        "--forward-to",
        help="Forward each event to a local HTTP endpoint.",
    ),
    header_values: list[str] | None = typer.Option(
        None,
        "--header",
        help="Extra header to include when forwarding, in 'Name: Value' form.",
    ),
    print_json_output: bool = typer.Option(
        False,
        "--print-json",
        help="Print raw event JSON instead of human-readable output.",
    ),
    print_secret_value: bool = typer.Option(
        False,
        "--print-secret",
        help="Print the generated forwarding secret.",
    ),
    skip_verify: bool = typer.Option(
        False,
        "--skip-verify",
        help="Disable TLS verification for forwarded HTTPS requests.",
    ),
    load_from_webhooks_api: str | None = typer.Option(
        None,
        "--load-from-webhooks-api",
        help="Webhook ID to load enabled events and forward path from.",
    ),
) -> None:
    """Listen for live webhook events over WebSocket."""
    try:
        config = _build_listen_config(
            events=events,
            forward_to=forward_to,
            header_values=header_values,
            print_json_output=print_json_output,
            skip_verify=skip_verify,
            print_secret_value=print_secret_value,
            load_from_webhooks_api=load_from_webhooks_api,
        )
        asyncio.run(_run_listen(config))
    except KeyboardInterrupt:
        raise typer.Exit(130)
    except (LayerbrainError, typer.BadParameter) as exc:
        print_error(str(exc))
        raise typer.Exit(1) from exc
