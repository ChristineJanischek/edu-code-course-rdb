from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class AssistantHintRequest:
    question: str
    learner_level: str = "sek2"
    topic: str = "relationale-datenbanken"
    language: str = "de"
    actor_role: str = "student"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AssistantHintResponse:
    hint: str
    follow_up_questions: list[str]
    safety_note: str
    knowledge_sources: list[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class AssistantInteraction:
    question: str
    response_hint: str
    actor_role: str
    topic: str
    metadata: dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class KeywordCandidate:
    title: str
    topic: str
    href: str


@dataclass(slots=True)
class AssistantKeywordSearchRequest:
    search_term: str
    language: str = "de"
    topic: str = "relationale-datenbanken"
    candidates: list[KeywordCandidate] = field(default_factory=list)


@dataclass(slots=True)
class AssistantKeywordSearchItem:
    title: str
    topic: str
    href: str
    score: float
    rationale: str


@dataclass(slots=True)
class AssistantKeywordSearchResponse:
    search_term: str
    summary: str
    results: list[AssistantKeywordSearchItem]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
