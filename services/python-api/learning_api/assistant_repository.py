import json
from pathlib import Path

from .assistant_models import AssistantInteraction, AssistantHintRequest


class AssistantKnowledgeRepository:
    """Speichert Interaktionen append-only und liefert didaktische Kontextquellen."""

    def __init__(self, storage_file: Path):
        self._storage_file = storage_file

    def build_context_sources(self, request: AssistantHintRequest) -> list[str]:
        normalized_topic = request.topic.strip().lower()
        topic_sources: dict[str, list[str]] = {
            "relationale-datenbanken": [
                "w3schools-sql",
                "lokales-handbuch-rdb",
                "aufgabenkatalog-rdb",
            ]
        }
        return topic_sources.get(normalized_topic, ["lokales-handbuch"])

    def append_interaction(self, interaction: AssistantInteraction) -> None:
        self._storage_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "question": interaction.question,
            "response_hint": interaction.response_hint,
            "actor_role": interaction.actor_role,
            "topic": interaction.topic,
            "metadata": interaction.metadata,
            "created_at": interaction.created_at,
        }
        with self._storage_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
