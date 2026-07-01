import re

from .assistant_models import (
    AssistantHintRequest,
    AssistantHintResponse,
    AssistantInteraction,
    AssistantKeywordSearchItem,
    AssistantKeywordSearchRequest,
    AssistantKeywordSearchResponse,
    KeywordCandidate,
)
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


class AssistantKeywordSearchService:
    """Rangt Stichwort-Kandidaten mit einer lernorientierten, LLM-aehnlichen Heuristik."""

    _SYNONYMS: dict[str, set[str]] = {
        "join": {"verbund", "verknuepfung", "verknüpfung", "tabellenverbund"},
        "normalisierung": {"1nf", "2nf", "3nf", "boyce-codd", "bcnf", "anomalie"},
        "3nf": {"normalisierung", "transitiv", "anomalie"},
        "kardinalitaet": {"kardinalität", "1:n", "n:m", "beziehung"},
        "kardinalität": {"kardinalitaet", "1:n", "n:m", "beziehung"},
        "aggregation": {"group by", "having", "sum", "count", "avg", "min", "max"},
        "group": {"aggregation", "having"},
        "having": {"aggregation", "group by"},
        "fremdschluessel": {"fremdschlüssel", "foreign key", "fk", "beziehung"},
        "fremdschlüssel": {"fremdschluessel", "foreign key", "fk", "beziehung"},
        "primarschluessel": {"primärschlüssel", "primary key", "pk", "schluessel"},
        "primärschlüssel": {"primarschluessel", "primary key", "pk", "schlüssel"},
    }

    def search(self, request: AssistantKeywordSearchRequest) -> AssistantKeywordSearchResponse:
        normalized_term = self._normalize_text(request.search_term)
        expanded_terms = self._expand_terms(normalized_term)

        ranked: list[AssistantKeywordSearchItem] = []
        for candidate in request.candidates:
            score, rationale = self._score_candidate(candidate, normalized_term, expanded_terms)
            if score <= 0:
                continue

            ranked.append(
                AssistantKeywordSearchItem(
                    title=candidate.title,
                    topic=candidate.topic,
                    href=candidate.href,
                    score=round(score, 3),
                    rationale=rationale,
                )
            )

        ranked.sort(key=lambda item: item.score, reverse=True)
        limited = ranked[:8]

        if not limited:
            summary = "Kein direkter Treffer. Nutze einen allgemeineren SQL- oder Modellierungsbegriff."
        else:
            summary = f"{len(limited)} passende Treffer fuer '{request.search_term.strip()}' gefunden."

        return AssistantKeywordSearchResponse(
            search_term=request.search_term.strip(),
            summary=summary,
            results=limited,
        )

    def _score_candidate(
        self,
        candidate: KeywordCandidate,
        normalized_term: str,
        expanded_terms: set[str],
    ) -> tuple[float, str]:
        title = self._normalize_text(candidate.title)
        topic = self._normalize_text(candidate.topic)
        haystack = f"{title} {topic}".strip()

        if not haystack:
            return 0.0, "Kein Suchtext in Kandidat vorhanden."

        score = 0.0
        rationale_parts: list[str] = []

        if normalized_term and normalized_term in title:
            score += 1.2
            rationale_parts.append("Direkter Treffer im Titel")
        elif normalized_term and normalized_term in topic:
            score += 1.0
            rationale_parts.append("Direkter Treffer im Themenbereich")

        hay_tokens = set(self._tokenize(haystack))
        for token in expanded_terms:
            if token in hay_tokens:
                score += 0.55

        overlap = self._token_overlap(expanded_terms, hay_tokens)
        if overlap > 0:
            score += overlap * 0.8
            rationale_parts.append("Semantische Uebereinstimmung")

        if score == 0.0 and normalized_term:
            if self._contains_fuzzy(haystack, normalized_term):
                score = 0.4
                rationale_parts.append("Aehnlicher Begriff")

        rationale = ", ".join(rationale_parts) if rationale_parts else "Basis-Match"
        return score, rationale

    @staticmethod
    def _token_overlap(query_terms: set[str], hay_terms: set[str]) -> float:
        if not query_terms:
            return 0.0
        return len(query_terms & hay_terms) / max(len(query_terms), 1)

    @staticmethod
    def _contains_fuzzy(text: str, term: str) -> bool:
        if len(term) < 4:
            return False
        return any(token.startswith(term[:4]) for token in text.split())

    def _expand_terms(self, normalized_term: str) -> set[str]:
        tokens = set(self._tokenize(normalized_term))
        if normalized_term:
            tokens.add(normalized_term)

        expanded = set(tokens)
        for token in tokens:
            expanded.update(self._SYNONYMS.get(token, set()))

        # Einfache Wortvarianten in Suche aufnehmen.
        for token in list(expanded):
            if token.endswith("en") and len(token) > 4:
                expanded.add(token[:-2])
            if token.endswith("ung") and len(token) > 5:
                expanded.add(token[:-3])

        return {entry for entry in expanded if entry}

    @staticmethod
    def _tokenize(value: str) -> list[str]:
        return [token for token in re.split(r"[^a-z0-9äöüß]+", value.lower()) if token]

    @staticmethod
    def _normalize_text(value: str) -> str:
        return re.sub(r"\s+", " ", str(value or "").strip().lower())
