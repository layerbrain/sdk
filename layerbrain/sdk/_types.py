"""Shared Pydantic models for the Layerbrain SDK.

These models represent the response objects returned by the brain API.
They are used by resource classes to provide typed responses.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Generic list response
# ---------------------------------------------------------------------------

class ListResponse(BaseModel):
    """Standard list response envelope: {"object": "list", "data": [...], "has_more": false}"""
    object: str = "list"
    data: List[Dict[str, Any]] = Field(default_factory=list)
    has_more: bool = False


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------

class Account(BaseModel):
    id: str
    object: str = "account"
    email: str
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created: Optional[str] = None
    modified: Optional[str] = None


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------

class Organization(BaseModel):
    id: str
    object: str = "organization"
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    deleted: Optional[str] = None


# ---------------------------------------------------------------------------
# Machines
# ---------------------------------------------------------------------------

class Machine(BaseModel):
    id: str
    object: str = "machine"
    name: Optional[str] = None
    organization: Optional[str] = None
    environment: Optional[str] = None
    state: Optional[str] = None
    zone: Optional[str] = None
    type: Optional[str] = None
    cwd: Optional[str] = None
    host: Optional[str] = None
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None
    key: Optional[str] = None
    vcpu: Optional[int] = None
    ram_gb: Optional[int] = None
    ssh_secret_id: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    expires_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Models (AI models listing)
# ---------------------------------------------------------------------------

class Model(BaseModel):
    id: str
    object: str = "model"
    type: Optional[str] = None
    provider: Optional[str] = None
    pricing: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Chat Completions
# ---------------------------------------------------------------------------

class ChatCompletionMessage(BaseModel):
    role: str
    content: Optional[str] = None


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: Optional[ChatCompletionMessage] = None
    finish_reason: Optional[str] = None


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletion(BaseModel):
    id: Optional[str] = None
    object: str = "chat.completion"
    created: Optional[int] = None
    model: Optional[str] = None
    choices: List[ChatCompletionChoice] = Field(default_factory=list)
    usage: Optional[ChatCompletionUsage] = None


class ChatCompletionChunkDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class ChatCompletionChunkChoice(BaseModel):
    index: int = 0
    delta: ChatCompletionChunkDelta = Field(default_factory=ChatCompletionChunkDelta)
    finish_reason: Optional[str] = None


class ChatCompletionChunk(BaseModel):
    id: Optional[str] = None
    object: str = "chat.completion.chunk"
    created: Optional[int] = None
    model: Optional[str] = None
    choices: List[ChatCompletionChunkChoice] = Field(default_factory=list)
    usage: Optional[ChatCompletionUsage] = None


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------

class APIKey(BaseModel):
    id: str
    name: Optional[str] = None
    note: Optional[str] = None
    value: Optional[str] = None
    secret: Optional[str] = None
    status: Optional[str] = None
    created: Optional[str] = None


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

class Secret(BaseModel):
    id: str
    object: str = "secret"
    name: Optional[str] = None
    organization: Optional[str] = None
    machine: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None
    value: Optional[str] = None


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class AuthToken(BaseModel):
    object: str = "token"
    access: str
    refresh: str
    email: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    membership: Optional[str] = None
    organization: Optional[str] = None
    machine: Optional[str] = None


class AuthIntent(BaseModel):
    object: str = "intent"
    type: str
    status: Optional[str] = None
    expires: Optional[str] = None
    id: Optional[str] = None
    host: Optional[str] = None
    redirect_url: Optional[str] = None
    url: Optional[str] = None


class DeviceAuthorization(BaseModel):
    device_code: str
    code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


# ---------------------------------------------------------------------------
# Engrams
# ---------------------------------------------------------------------------

class Engram(BaseModel):
    id: str
    object: str = "engram"
    name: Optional[str] = None
    organization: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None
    created: Optional[str] = None
    modified: Optional[str] = None


# ---------------------------------------------------------------------------
# Environments
# ---------------------------------------------------------------------------

class Environment(BaseModel):
    id: str
    object: str = "environment"
    name: Optional[str] = None
    slug: Optional[str] = None
    organization: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None


# ---------------------------------------------------------------------------
# Memberships
# ---------------------------------------------------------------------------

class Membership(BaseModel):
    id: str
    object: str = "membership"
    organization: Optional[str] = None
    account: Optional[str] = None
    role: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------

class Subscription(BaseModel):
    id: str
    object: str = "subscription"
    organization: Optional[str] = None
    plan: Optional[str] = None
    status: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

class ImageGeneration(BaseModel):
    object: str = "image.generation"
    data: Optional[List[Dict[str, Any]]] = None


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

class AudioSpeech(BaseModel):
    object: str = "audio.speech"
    data: Optional[bytes] = None


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------

class Embedding(BaseModel):
    object: str = "embedding"
    embedding: Optional[List[float]] = None
    index: int = 0
