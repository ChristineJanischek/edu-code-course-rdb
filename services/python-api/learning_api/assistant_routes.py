import os
from pathlib import Path

from flask import request

from .assistant_models import AssistantHintRequest
from .assistant_repository import AssistantKnowledgeRepository
from .assistant_service import AssistantKeywordSearchService, AssistantTutoringService, TutoringSafetyPolicy
from .assistant_models import AssistantKeywordSearchRequest, KeywordCandidate


def _build_tutoring_service() -> AssistantTutoringService:
    storage_path = os.getenv("ASSISTANT_INTERACTIONS_PATH", "/tmp/assistant/interactions.jsonl")
    storage_file = Path(storage_path)
    repository = AssistantKnowledgeRepository(storage_file)
    policy = TutoringSafetyPolicy()
    return AssistantTutoringService(repository, policy)


def assistant_hint_route(dual_response, dual_error):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return dual_error("ASSISTANT_INVALID_PAYLOAD", "Invalid JSON payload", status_code=400)

    question = payload.get("question")
    if not isinstance(question, str) or not question.strip():
        return dual_error("ASSISTANT_INVALID_QUESTION", "Field 'question' must be a non-empty string", status_code=400)

    request_dto = AssistantHintRequest(
        question=question.strip(),
        learner_level=str(payload.get("learner_level", "sek2")).strip() or "sek2",
        topic=str(payload.get("topic", "relationale-datenbanken")).strip() or "relationale-datenbanken",
        language=str(payload.get("language", "de")).strip() or "de",
        actor_role=str(payload.get("actor_role", "student")).strip() or "student",
        metadata=payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
    )

    response_dto = _build_tutoring_service().generate_hint(request_dto)
    payload_response = {
        "hint": response_dto.hint,
        "follow_up_questions": response_dto.follow_up_questions,
        "safety_note": response_dto.safety_note,
        "knowledge_sources": response_dto.knowledge_sources,
        "created_at": response_dto.created_at,
    }
    return dual_response(payload_response, status_code=200)


def assistant_keyword_search_route(dual_response, dual_error):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return dual_error("ASSISTANT_KEYWORD_INVALID_PAYLOAD", "Invalid JSON payload", status_code=400)

    search_term = payload.get("search_term")
    if not isinstance(search_term, str) or not search_term.strip():
        return dual_error("ASSISTANT_KEYWORD_INVALID_TERM", "Field 'search_term' must be a non-empty string", status_code=400)

    candidates_payload = payload.get("candidates")
    if not isinstance(candidates_payload, list):
        return dual_error("ASSISTANT_KEYWORD_INVALID_CANDIDATES", "Field 'candidates' must be an array", status_code=400)

    candidates: list[KeywordCandidate] = []
    for item in candidates_payload[:200]:
        if not isinstance(item, dict):
            continue

        title = str(item.get("title", "")).strip()
        topic = str(item.get("topic", "")).strip()
        href = str(item.get("href", "")).strip()
        if not title or not href:
            continue

        candidates.append(KeywordCandidate(title=title, topic=topic, href=href))

    if not candidates:
        return dual_error(
            "ASSISTANT_KEYWORD_EMPTY_CANDIDATES",
            "At least one valid candidate is required",
            status_code=400,
        )

    request_dto = AssistantKeywordSearchRequest(
        search_term=search_term.strip(),
        language=str(payload.get("language", "de")).strip() or "de",
        topic=str(payload.get("topic", "relationale-datenbanken")).strip() or "relationale-datenbanken",
        candidates=candidates,
    )

    response_dto = AssistantKeywordSearchService().search(request_dto)
    response_payload = {
        "search_term": response_dto.search_term,
        "summary": response_dto.summary,
        "results": [
            {
                "title": item.title,
                "topic": item.topic,
                "href": item.href,
                "score": item.score,
                "rationale": item.rationale,
            }
            for item in response_dto.results
        ],
        "insights": [
            {
                "title": item.title,
                "category": item.category,
                "summary": item.summary,
                "syntax": item.syntax,
                "example_sql": item.example_sql,
                "example_view": item.example_view,
                "source_label": item.source_label,
                "source_url": item.source_url,
            }
            for item in response_dto.insights
        ],
        "knowledge_sources": response_dto.knowledge_sources,
        "created_at": response_dto.created_at,
    }
    return dual_response(response_payload, status_code=200)
