"""Shared Pydantic models for the Layerbrain SDK.

These models represent the response objects returned by the brain API.
They are used by resource classes to provide typed responses.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Generic list response
# ---------------------------------------------------------------------------

class ListResponse(BaseModel):
    """Standard list response envelope: {"object": "list", "data": [...], "has_more": false}"""
    object: str = "list"
    data: list[dict[str, Any]] = Field(default_factory=list)
    has_more: bool = False


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------

class Account(BaseModel):
    id: str
    object: str = "account"
    email: str
    name: str | None = None
    data: dict[str, Any] | None = None
    created: str | None = None
    modified: str | None = None


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------

class Organization(BaseModel):
    id: str
    object: str = "organization"
    name: str | None = None
    data: dict[str, Any] | None = None
    created: str | None = None
    modified: str | None = None
    deleted: str | None = None


# ---------------------------------------------------------------------------
# Machines
# ---------------------------------------------------------------------------

class Machine(BaseModel):
    id: str
    object: str = "machine"
    name: str | None = None
    organization: str | None = None
    environment: str | None = None
    state: str | None = None
    zone: str | None = None
    type: str | None = None
    cwd: str | None = None
    host: str | None = None
    ipv4: str | None = None
    ipv6: str | None = None
    key: str | None = None
    vcpu: int | None = None
    ram_gb: int | None = None
    ssh_secret_id: str | None = None
    created: str | None = None
    modified: str | None = None
    expires_at: str | None = None


# ---------------------------------------------------------------------------
# Models (AI models listing)
# ---------------------------------------------------------------------------

class Model(BaseModel):
    id: str
    object: str = "model"
    type: str | None = None
    provider: str | None = None
    pricing: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Chat Completions
# ---------------------------------------------------------------------------

class ChatCompletionMessage(BaseModel):
    role: str
    content: str | None = None


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: ChatCompletionMessage | None = None
    finish_reason: str | None = None


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletion(BaseModel):
    id: str | None = None
    object: str = "chat.completion"
    created: int | None = None
    model: str | None = None
    choices: list[ChatCompletionChoice] = Field(default_factory=list)
    usage: ChatCompletionUsage | None = None


class ChatCompletionChunkDelta(BaseModel):
    role: str | None = None
    content: str | None = None


class ChatCompletionChunkChoice(BaseModel):
    index: int = 0
    delta: ChatCompletionChunkDelta = Field(default_factory=ChatCompletionChunkDelta)
    finish_reason: str | None = None


class ChatCompletionChunk(BaseModel):
    id: str | None = None
    object: str = "chat.completion.chunk"
    created: int | None = None
    model: str | None = None
    choices: list[ChatCompletionChunkChoice] = Field(default_factory=list)
    usage: ChatCompletionUsage | None = None


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------

class APIKey(BaseModel):
    id: str
    name: str | None = None
    note: str | None = None
    value: str | None = None
    secret: str | None = None
    status: str | None = None
    created: str | None = None


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

class Secret(BaseModel):
    id: str
    object: str = "secret"
    name: str | None = None
    organization: str | None = None
    machine: str | None = None
    data: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None
    value: str | None = None


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class AuthToken(BaseModel):
    object: str = "token"
    access: str
    refresh: str
    email: str | None = None
    id: str | None = None
    name: str | None = None
    membership: str | None = None
    organization: str | None = None
    machine: str | None = None


class DeviceAuthorization(BaseModel):
    device_code: str
    code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


# ---------------------------------------------------------------------------
# Memberships
# ---------------------------------------------------------------------------

class Membership(BaseModel):
    id: str
    object: str = "membership"
    organization: str | None = None
    account: str | None = None
    role: str | None = None
    data: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------

class Subscription(BaseModel):
    id: str
    object: str = "subscription"
    organization: str | None = None
    plan: str | None = None
    status: str | None = None
    data: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

class ImageGeneration(BaseModel):
    object: str = "image.generation"
    data: list[dict[str, Any]] | None = None


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

class AudioSpeech(BaseModel):
    object: str = "audio.speech"
    data: bytes | None = None


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------

class Embedding(BaseModel):
    object: str = "embedding"
    embedding: list[float] | None = None
    index: int = 0
