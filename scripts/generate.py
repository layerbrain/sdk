#!/usr/bin/env python3
"""Generate SDK resource classes from the OpenAPI spec.

Usage:
    python scripts/generate.py                          # Pull latest spec + generate
    python scripts/generate.py --spec path/to/spec.json # Use local spec
    python scripts/generate.py --no-pull                # Use cached spec
    python scripts/generate.py --dry-run                # Preview only
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SDK_DIR = PROJECT_ROOT / "layerbrain" / "sdk"
RESOURCES_DIR = SDK_DIR / "resources"
OPENAPI_DIR = PROJECT_ROOT / "openapi"
REPO_SPEC_FILE = OPENAPI_DIR / "openapi.json"
VENDORED_SPEC_FILE = SDK_DIR / "openapi" / "openapi.json"

SPEC_URL = "https://raw.githubusercontent.com/layerbrain/openapi/main/openapi.json"

# Tags to skip entirely (not user-facing)
SKIP_TAGS = {"Health", "Username"}

# Tag → module name overrides
MODULE_OVERRIDES = {
    "Api-Keys": "api_keys",
    "3D": "threed",
    "Network_Rules": "network_rules",
    "Network_Flows": "network_flows",
}

# Tag → class name overrides
CLASS_OVERRIDES = {
    "Api-Keys": "APIKeys",
    "3D": "ThreeD",
    "Network_Rules": "NetworkRules",
    "Network_Flows": "NetworkFlows",
}

TYPE_MAP = {"string": "str", "integer": "int", "boolean": "bool", "number": "float"}

ACTION_PREFIXES = (
    "list",
    "create",
    "retrieve",
    "patch",
    "put",
    "replace",
    "delete",
    "destroy",
    "archive",
    "restore",
    "download",
    "rotate",
    "validate",
    "presign",
    "reveal",
    "claim",
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class QueryParam:
    name: str
    type: str
    required: bool
    default: Optional[str]

@dataclass
class Endpoint:
    path: str          # e.g. "/machines" (no /v1 prefix)
    method: str        # get, post, delete, patch, put
    operation_id: str
    summary: str
    has_body: bool
    path_params: list[str]
    query_params: list[QueryParam]
    is_list: bool

@dataclass
class Resource:
    tag: str
    module_name: str   # e.g. "machines"
    class_name: str    # e.g. "Machines"
    endpoints: list[Endpoint] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parse spec
# ---------------------------------------------------------------------------

def parse_spec(spec: dict) -> list[Resource]:
    resources: dict[str, Resource] = {}

    for raw_path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method in ("parameters", "servers") or method.startswith("x-"):
                continue

            tag = (details.get("tags") or ["Untagged"])[0]
            if tag in SKIP_TAGS:
                continue

            mod = MODULE_OVERRIDES.get(tag, tag.lower().replace("-", "_"))
            cls = CLASS_OVERRIDES.get(tag, tag.replace("-", "").replace(" ", ""))

            if mod not in resources:
                resources[mod] = Resource(tag=tag, module_name=mod, class_name=cls)

            path_params = re.findall(r"\{(\w+)\}", raw_path)

            query_params = []
            for p in details.get("parameters", []):
                if p.get("in") == "query":
                    s = p.get("schema", {})
                    query_params.append(QueryParam(
                        name=p["name"],
                        type=TYPE_MAP.get(s.get("type", "string"), "str"),
                        required=p.get("required", False),
                        default=str(s["default"]) if "default" in s else None,
                    ))

            # Strip /v1 prefix and trailing slash
            path = raw_path
            if path.startswith("/v1"):
                path = path[3:]
            path = path.rstrip("/")

            op_id = details.get("operationId", "")
            is_list = (
                op_id.startswith(f"{mod}_list_")
                or (
                    method == "get"
                    and not path_params
                    and (
                        raw_path.endswith("/")
                        or raw_path == f"/v1/{mod}"
                        or raw_path == "/v1/models"
                    )
                )
            )

            resources[mod].endpoints.append(Endpoint(
                path=path or f"/{mod}",
                method=method,
                operation_id=details.get("operationId", ""),
                summary=(details.get("summary") or "").strip(),
                has_body="requestBody" in details,
                path_params=path_params,
                query_params=query_params,
                is_list=is_list,
            ))

    for r in resources.values():
        r.endpoints.sort(key=lambda e: (e.path, e.method))

    return sorted(resources.values(), key=lambda r: r.module_name)


# ---------------------------------------------------------------------------
# Method name derivation
# ---------------------------------------------------------------------------

def _relative_method_name(ep: Endpoint, res: Resource) -> str:
    """Build a method name from all non-param path segments after the resource base.

    E.g. for auth resource:
        /auth/device         → "device"
        /auth/device/confirm → "device_confirm"
        /auth/intents/{id}/confirm → "intent_confirm"
        /auth/token/refresh  → "token_refresh"
    """
    base_path = f"/{res.module_name}" if res.module_name != "models" else "/models"
    # Strip the base prefix from the path
    relative = ep.path
    if relative.startswith(base_path):
        relative = relative[len(base_path):]
    relative = relative.strip("/")

    # Take all segments, strip {param} placeholders, singularize trailing-s segments
    parts = []
    for seg in relative.split("/"):
        if seg.startswith("{"):
            continue
        clean = seg.replace("-", "_")
        # Singularize simple plural segments (intents→intent, tokens→token)
        if clean.endswith("s") and len(clean) > 2:
            clean = clean[:-1]
        parts.append(clean)

    return "_".join(parts) if parts else "create"


def _singularize(value: str) -> str:
    if value.endswith("ies") and len(value) > 3:
        return value[:-3] + "y"
    if value.endswith("ses") and len(value) > 3:
        return value[:-2]
    if value.endswith("s") and not value.endswith("ss") and len(value) > 2:
        return value[:-1]
    return value


def _singularize_phrase(value: str) -> str:
    if not value:
        return value
    parts = value.split("_")
    parts[-1] = _singularize(parts[-1])
    return "_".join(parts)


def _operation_core(ep: Endpoint, res: Resource) -> str:
    operation_id = ep.operation_id or ""
    prefix = f"{res.module_name}_"
    if operation_id.startswith(prefix):
        operation_id = operation_id[len(prefix):]
    suffix = f"_{ep.method}"
    if operation_id.endswith(suffix):
        operation_id = operation_id[: -len(suffix)]
    return operation_id


def _parse_operation(ep: Endpoint, res: Resource) -> tuple[str, str, str] | None:
    core = _operation_core(ep, res)
    if not core:
        return None

    for action in ACTION_PREFIXES:
        if core == action:
            return action, "", ""
        prefix = f"{action}_"
        if core.startswith(prefix):
            entity = core[len(prefix):]
            return action, entity, _singularize_phrase(entity)
    return None


def _resource_entities(res: Resource) -> set[str]:
    entities: set[str] = set()
    for endpoint in res.endpoints:
        parsed = _parse_operation(endpoint, res)
        if not parsed:
            continue
        _action, _raw_entity, entity = parsed
        if entity:
            entities.add(entity)
    return entities


def _build_action_method_name(action: str, raw_entity: str, singular_entity: str, *, multi_entity: bool) -> str:
    if action == "destroy":
        action = "delete"
    if action == "patch":
        action = "update"
    if action == "put":
        action = "replace"

    if action == "list":
        return "list" if not multi_entity else f"list_{raw_entity or 'items'}"
    if action in {"create", "retrieve", "update", "replace", "delete"}:
        return action if not multi_entity else f"{action}_{singular_entity or raw_entity or 'item'}"
    if action == "archive":
        return "archive" if not multi_entity else f"archive_{singular_entity or raw_entity or 'item'}"
    if action == "restore":
        return "restore" if not multi_entity else f"restore_{singular_entity or raw_entity or 'item'}"
    if action == "download":
        return "download" if not multi_entity else f"download_{singular_entity or raw_entity or 'item'}"
    if action == "claim":
        return "claim" if not multi_entity else f"claim_{singular_entity or raw_entity or 'item'}"
    if action == "rotate":
        return "rotate" if not raw_entity and not multi_entity else f"rotate_{singular_entity or raw_entity or 'item'}"
    if action == "validate":
        return "validate" if not raw_entity and not multi_entity else f"validate_{singular_entity or raw_entity or 'item'}"
    if action == "presign":
        return "presign" if not raw_entity and not multi_entity else f"presign_{singular_entity or raw_entity or 'item'}"
    if action == "reveal":
        return "reveal" if not raw_entity and not multi_entity else f"reveal_{singular_entity or raw_entity or 'item'}"
    return f"{action}_{singular_entity or raw_entity or 'item'}"


def _method_name(ep: Endpoint, res: Resource, used_names: set[str]) -> Optional[str]:
    parsed = _parse_operation(ep, res)
    if parsed:
        action, raw_entity, singular_entity = parsed
        candidate = _build_action_method_name(
            action,
            raw_entity,
            singular_entity,
            multi_entity=len(_resource_entities(res)) > 1,
        )
        if candidate in used_names:
            fallback = _relative_method_name(ep, res)
            if fallback not in used_names:
                return fallback
        return candidate

    base_path = f"/{res.module_name}" if res.module_name != "models" else "/models"

    if ep.is_list:
        return "list"

    if ep.method == "get" and ep.path_params:
        parts = ep.path.rstrip("/").split("/")
        last = parts[-1]
        if last.startswith("{"):
            candidate = "retrieve"
        else:
            candidate = last.replace("-", "_")
        if candidate in used_names:
            candidate = _relative_method_name(ep, res)
        return candidate

    if ep.method == "delete":
        # Check for sub-path deletes (e.g. /engrams/delete-all vs /engrams/{id})
        parts = ep.path.rstrip("/").split("/")
        last = parts[-1]
        if not last.startswith("{") and last != res.module_name:
            candidate = last.replace("-", "_")
        else:
            candidate = "delete"
        if candidate in used_names:
            candidate = _relative_method_name(ep, res)
        return candidate

    if ep.method == "patch" and ep.path_params:
        return "update"

    if ep.method == "put" and ep.path_params:
        return "replace"

    if ep.method == "post":
        parts = ep.path.rstrip("/").split("/")
        last = parts[-1]
        if last.startswith("{"):
            candidate = "create"
        else:
            clean = ep.path.rstrip("/")
            if clean == base_path or clean == f"/{res.module_name}":
                candidate = "create"
            else:
                candidate = last.replace("-", "_")
        # Disambiguate collisions using full relative path
        if candidate in used_names:
            candidate = _relative_method_name(ep, res)
        return candidate

    return None


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

def _path_expr(ep: Endpoint) -> str:
    if ep.path_params:
        p = ep.path
        for pp in ep.path_params:
            p = p.replace(f"{{{pp}}}", f"{{{pp}}}")
        return f'f"{p}"'
    return f'"{ep.path}"'


def _gen_method(ep: Endpoint, res: Resource, used_names: set[str]) -> Optional[str]:
    name = _method_name(ep, res, used_names)
    if not name:
        return None
    used_names.add(name)

    # Signature
    params = ["self"]
    for pp in ep.path_params:
        params.append(f"{pp}: str")

    for qp in ep.query_params:
        if qp.required:
            params.append(f"{qp.name}: {qp.type}")
        else:
            default = qp.default if qp.default is not None else "None"
            params.append(f"{qp.name}: Optional[{qp.type}] = {default}")

    if ep.has_body:
        params.append("**kwargs: Any")

    doc = ep.summary or f"{name.replace('_', ' ').capitalize()}."

    # Body — use Resource base class helpers (async, handled by _auto wrapper)
    if ep.is_list:
        body = _gen_list_body(ep)
        ret = "SyncPage"
    elif ep.method == "delete":
        body = f"return await self._delete({_path_expr(ep)})"
        ret = "dict"
    elif ep.method == "get":
        body = f"return await self._get({_path_expr(ep)}, params=None)"
        ret = "dict"
    elif ep.method == "patch" and ep.has_body:
        body = f"return await self._patch({_path_expr(ep)}, json=kwargs)"
        ret = "dict"
    elif ep.method == "patch":
        body = f"return await self._patch({_path_expr(ep)}, json={{}})"
        ret = "dict"
    elif ep.method == "put" and ep.has_body:
        body = f"return await self._put({_path_expr(ep)}, json=kwargs)"
        ret = "dict"
    elif ep.method == "put":
        body = f"return await self._put({_path_expr(ep)}, json={{}})"
        ret = "dict"
    elif ep.method == "post" and ep.has_body:
        body = f"return await self._post({_path_expr(ep)}, json=kwargs)"
        ret = "dict"
    elif ep.method == "post":
        body = f"return await self._post({_path_expr(ep)}, json={{}})"
        ret = "dict"
    else:
        body = f"return await self._get({_path_expr(ep)}, params=None)"
        ret = "dict"

    # Build signature, wrapping if it would exceed 100 chars
    inline_sig = ", ".join(params)
    header = f"async def {name}({inline_sig}) -> {ret}:"
    # +4 for class-level indent
    if len(header) + 4 <= 100:
        sig_str = f"async def {name}({inline_sig}) -> {ret}:"
    else:
        joined = ",\n    ".join(params)
        sig_str = f"async def {name}(\n    {joined},\n) -> {ret}:"

    return f'{sig_str}\n    """{doc}"""\n    {body}'


def _gen_list_body(ep: Endpoint) -> str:
    lines = []
    lines.append(f"request_path = {_path_expr(ep)}")
    if ep.query_params:
        lines.append("params: dict[str, Any] = {}")
        for qp in ep.query_params:
            lines.append(f'if {qp.name} is not None:\n        params["{qp.name}"] = {qp.name}')
        lines.append("data = await self._get(request_path, params=params or None)")
    else:
        lines.append("data = await self._get(request_path, params=None)")

    lines.append('return SyncPage(\n        data=data.get("data", []),\n        has_more=data.get("has_more", False),\n        client=self._client,\n        path=request_path,\n    )')
    return "\n    ".join(lines)


def _indent(text: str, prefix: str = "    ") -> str:
    """Indent every line of text by prefix."""
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())


def generate_resource(res: Resource) -> str:
    methods = []
    used_names: set[str] = set()
    for ep in res.endpoints:
        m = _gen_method(ep, res, used_names)
        if m:
            methods.append(m)

    needs_page = any(ep.is_list for ep in res.endpoints)
    needs_optional = any(
        qp for ep in res.endpoints for qp in ep.query_params if not qp.required
    )
    typing_imports = "Any, Optional" if needs_optional else "Any"
    imports = [
        "from __future__ import annotations",
        "",
        f"from typing import {typing_imports}",
        "",
        "from .._resource import Resource",
    ]
    if needs_page:
        imports.append("from .._pagination import SyncPage")

    # Indent each method block by 4 spaces for class body
    indented_methods = [_indent(m) for m in methods]
    body = "\n\n".join(indented_methods) if indented_methods else "    pass"

    return "\n".join(imports) + f"""


class {res.class_name}(Resource):
    \"\"\"{res.tag} API resource (auto-generated).\"\"\"

{body}
"""


def generate_init(resources: list[Resource]) -> str:
    imports = []
    names = []
    for r in resources:
        if r.module_name == "chat":
            imports.append("from .chat import Chat")
        else:
            imports.append(f"from .{r.module_name} import {r.class_name}")
        names.append(r.class_name)

    return '"""SDK resource classes (auto-generated + hand-written)."""\n\n' + "\n".join(sorted(imports)) + "\n\n__all__ = [\n" + "\n".join(f'    "{n}",' for n in sorted(names)) + "\n]\n"


# ---------------------------------------------------------------------------
# Pull
# ---------------------------------------------------------------------------

def pull_spec(url: Optional[str] = None) -> dict:
    import httpx
    target = url or SPEC_URL
    print(f"Pulling {target}")
    resp = httpx.get(target, timeout=30.0, follow_redirects=True)
    resp.raise_for_status()
    spec = resp.json()
    write_spec_files(spec)
    return spec


def write_spec_files(spec: dict) -> None:
    serialized = json.dumps(spec, indent=2) + "\n"
    OPENAPI_DIR.mkdir(parents=True, exist_ok=True)
    VENDORED_SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPO_SPEC_FILE.write_text(serialized)
    VENDORED_SPEC_FILE.write_text(serialized)
    print(f"Saved {REPO_SPEC_FILE}")
    print(f"Mirrored {VENDORED_SPEC_FILE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate SDK resources from OpenAPI spec")
    parser.add_argument("--spec", help="Local openapi.json path")
    parser.add_argument("--no-pull", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--url", help="Override spec URL")
    args = parser.parse_args()

    if args.spec:
        spec = json.loads(Path(args.spec).read_text())
        write_spec_files(spec)
    elif args.no_pull:
        spec = json.loads(REPO_SPEC_FILE.read_text())
    else:
        spec = pull_spec(args.url)

    resources = parse_spec(spec)

    # Hand-written resources that the generator must never overwrite.
    # These require custom logic (streaming, Pydantic response parsing, URL encoding, SSH, etc.)
    PRESERVED_MODULES = {"chat", "machines", "models", "webhooks"}

    preserved = [
        Resource(tag="Chat", module_name="chat", class_name="Chat"),
        Resource(tag="Machines", module_name="machines", class_name="Machines"),
        Resource(tag="Models", module_name="models", class_name="Models"),
        Resource(tag="Webhooks", module_name="webhooks", class_name="Webhooks"),
    ]

    print(f"Parsed {len(resources)} resources from spec:")
    for r in resources:
        label = " (preserved)" if r.module_name in PRESERVED_MODULES else ""
        print(f"  {r.class_name} ({r.module_name}): {len(r.endpoints)} endpoints{label}")

    if args.dry_run:
        print("\nWould generate:")
        for r in resources:
            if r.module_name not in PRESERVED_MODULES:
                print(f"  sdk/resources/{r.module_name}.py")
        print(f"  sdk/resources/__init__.py")
        return

    gen_resources = [r for r in resources if r.module_name not in PRESERVED_MODULES]

    for r in gen_resources:
        path = RESOURCES_DIR / f"{r.module_name}.py"
        path.write_text(generate_resource(r))
        print(f"  {path.name}")

    # __init__.py includes preserved + all generated
    all_resources = gen_resources + preserved
    init_path = RESOURCES_DIR / "__init__.py"
    init_path.write_text(generate_init(all_resources))
    print(f"  __init__.py")

    preserved_names = ", ".join(sorted(PRESERVED_MODULES))
    print(f"\nDone. {len(gen_resources)} resources generated, {preserved_names} preserved.")


if __name__ == "__main__":
    main()
