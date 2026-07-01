from .assistant_models import AssistantHintRequest, AssistantHintResponse, AssistantInteraction
from .assistant_repository import AssistantKnowledgeRepository


class TutoringSafetyPolicy:
    """Sorgt dafuer, dass nur lernfoerdernde Hinweise und keine Komplettloesungen erzeugt werden."""

    def enforce(self, generated_hint: str) -> str:
        safe_hint = generated_hint.strip()
        if not safe_hint:
            return "Beschreibe zuerst, welche Tabellen und Schluessel du erkennst, bevor du die SQL-Abfrage formulierst."
        return safe_hint


class AssistantTutoringService:
    def __init__(self, repository: AssistantKnowledgeRepository, safety_policy: TutoringSafetyPolicy):
        self._repository = repository
        self._safety_policy = safety_policy

    def generate_hint(self, request: AssistantHintRequest) -> AssistantHintResponse:
        hint = self._derive_hint_from_question(request.question)
        safe_hint = self._safety_policy.enforce(hint)
        follow_up = [
            "Welche Tabellen sind fuer die Aufgabe wirklich notwendig?",
            "Wie pruefst du, ob dein Join alle benoetigten Datensaetze liefert?",
            "Welche Bedingung gehoert in WHERE und welche in HAVING?",
        ]
        sources = self._repository.build_context_sources(request)
        interaction = AssistantInteraction(
            question=request.question,
            response_hint=safe_hint,
            actor_role=request.actor_role,
            topic=request.topic,
            metadata=request.metadata,
        )
        self._repository.append_interaction(interaction)

        return AssistantHintResponse(
            hint=safe_hint,
            follow_up_questions=follow_up,
            safety_note="Hinweismodus aktiv: Der Assistent gibt Lernimpulse statt fertiger Loesungen.",
            knowledge_sources=sources,
        )

    @staticmethod
    def _derive_hint_from_question(question: str) -> str:
        lowered = question.lower()
        if "join" in lowered:
            return "Starte mit zwei Tabellen und notiere zuerst Primar- und Fremdschluessel. Formuliere danach den Join Schritt fuer Schritt."
        if "normal" in lowered or "3nf" in lowered:
            return "Suche funktionale Abhaengigkeiten und pruefe, ob Nicht-Schluesselattribute transitiv von einem Schluessel abhaengen."
        if "group by" in lowered or "aggregation" in lowered:
            return "Trenne zuerst Detailspalten und Aggregatspalten. Jede nicht aggregierte Spalte muss in GROUP BY stehen."
        return "Beschreibe zuerst in eigenen Worten den Datenbedarf der Aufgabe und leite daraus dann die SQL-Bausteine SELECT, FROM und WHERE ab."
