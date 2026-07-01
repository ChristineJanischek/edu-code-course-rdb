import os
from pathlib import Path

from flask import request

from .assistant_models import AssistantHintRequest
from .assistant_repository import AssistantKnowledgeRepository
from .assistant_service import AssistantTutoringService, TutoringSafetyPolicy


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
