import re

from . import keyword_knowledge
from .assistant_models import (
    AssistantHintRequest,
    AssistantHintResponse,
    AssistantInteraction,
    AssistantKeywordInsight,
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
        if "select" in lowered or "projektion" in lowered:
            return "Beginne mit der Ergebnissicht: Welche Spalten braucht die Aufgabe wirklich? Formuliere dann zuerst SELECT, bevor du Filter oder Aggregation ergänzt."
        if "from" in lowered or "basistabelle" in lowered or "quelltabelle" in lowered:
            return "Lege zuerst die Basistabelle in FROM fest. Prüfe danach, welche weiteren Tabellen wirklich benötigt werden und ergänze nur diese per JOIN."
        if "left join" in lowered or "left outer join" in lowered or "linker join" in lowered:
            return "Denke bei LEFT JOIN von links nach rechts: Alle Zeilen der linken Tabelle bleiben erhalten; rechte Treffer können NULL sein."
        if "join" in lowered:
            return "Starte mit zwei Tabellen und notiere zuerst Primar- und Fremdschluessel. Formuliere danach den Join Schritt fuer Schritt."
        if "where" in lowered or "filter" in lowered or "bedingung" in lowered:
            return "Trenne Zeilenfilter und Gruppenfilter sauber: Bedingungen auf Einzelzeilen gehören in WHERE, nicht in HAVING."
        if "normal" in lowered or "3nf" in lowered:
            return "Suche funktionale Abhaengigkeiten und pruefe, ob Nicht-Schluesselattribute transitiv von einem Schluessel abhaengen."
        if "group by" in lowered or "aggregation" in lowered or "gruppierung" in lowered:
            return "Trenne zuerst Detailspalten und Aggregatspalten. Jede nicht aggregierte Spalte muss in GROUP BY stehen."
        if "having" in lowered or "gruppenfilter" in lowered:
            return "Nutze HAVING nur für Bedingungen auf Aggregatwerte (z. B. COUNT(*) >= 2). Rohdaten-Filter bleiben in WHERE."
        if "order by" in lowered or "sortierung" in lowered:
            return "Sortiere erst ganz am Ende mit ORDER BY. Prüfe dabei explizit ASC oder DESC, damit die Ergebnisreihenfolge fachlich passt."
        return "Beschreibe zuerst in eigenen Worten den Datenbedarf der Aufgabe und leite daraus dann die SQL-Bausteine SELECT, FROM und WHERE ab."


class AssistantKeywordSearchService:
    """Rangt Stichwort-Kandidaten mit einer lernorientierten, LLM-aehnlichen Heuristik."""

    def search(self, request: AssistantKeywordSearchRequest) -> AssistantKeywordSearchResponse:
        normalized_term = self._normalize_text(request.search_term)
        expanded_terms = self._expand_terms(normalized_term)
        insights = self._build_insights(normalized_term, expanded_terms)

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
        knowledge_sources = self._collect_knowledge_sources(insights, limited)

        if not limited and not insights:
            summary = "Kein direkter Treffer. Nutze einen allgemeineren SQL-, Modellierungs- oder Normalisierungsbegriff."
        else:
            parts: list[str] = []
            if limited:
                parts.append(f"{len(limited)} passende Index-Treffer")
            if insights:
                parts.append(f"{len(insights)} Beispielkarten mit Syntax, SQL und VIEW")
            if knowledge_sources:
                parts.append(f"Quellen: {', '.join(knowledge_sources)}")
            summary = f"{'; '.join(parts)} fuer '{request.search_term.strip()}'."

        return AssistantKeywordSearchResponse(
            search_term=request.search_term.strip(),
            summary=summary,
            results=limited,
            insights=insights,
            knowledge_sources=knowledge_sources,
        )

    def _build_insights(self, normalized_term: str, expanded_terms: set[str]) -> list[AssistantKeywordInsight]:
        ranked_cards: list[tuple[float, AssistantKeywordInsight]] = []
        for card in keyword_knowledge.INSIGHT_CARDS:
            score = self._score_insight_card(card, normalized_term, expanded_terms)
            if score <= 0:
                continue

            ranked_cards.append(
                (
                    score,
                    AssistantKeywordInsight(
                        title=str(card["key"]).replace("-", " ").upper() if str(card["key"]).islower() and "nf" not in str(card["key"]) else self._format_insight_title(str(card["key"])),
                        category=str(card["category"]),
                        summary=str(card["summary"]),
                        syntax=str(card.get("syntax", "")),
                        example_sql=str(card.get("example_sql", "")),
                        example_view=str(card.get("example_view", "")),
                        related_sources=[
                            {"label": str(s.get("label", "")), "url": str(s.get("url", ""))}
                            for s in (card.get("related_sources") or [])
                            if isinstance(s, dict)
                        ],
                    ),
                )
            )

        ranked_cards.sort(key=lambda entry: entry[0], reverse=True)
        return [insight for _, insight in ranked_cards[:3]]

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

    def _score_insight_card(self, card: dict[str, object], normalized_term: str, expanded_terms: set[str]) -> float:
        aliases = {self._normalize_text(entry) for entry in card.get("aliases", set()) if str(entry).strip()}

        score = 0.0
        if normalized_term and normalized_term in aliases:
            score += 2.2

        query_tokens = set(self._tokenize(normalized_term))
        for alias in aliases:
            alias_tokens = set(self._tokenize(alias))
            overlap = self._token_overlap(expanded_terms | query_tokens, alias_tokens)
            if overlap > 0:
                score += overlap * 1.4
            if normalized_term and normalized_term in alias:
                score += 0.8

        summary_tokens = set(self._tokenize(str(card.get("summary", ""))))
        score += self._token_overlap(expanded_terms | query_tokens, summary_tokens)
        return score

    @staticmethod
    def _collect_knowledge_sources(insights: list[AssistantKeywordInsight], results: list[AssistantKeywordSearchItem]) -> list[str]:
        labels: list[str] = []
        if results:
            labels.append("Lokaler Index")

        for insight in insights:
            for source in insight.related_sources:
                label = str(source.get("label", "")).strip()
                if label and label not in labels:
                    labels.append(label)

        return labels

    @staticmethod
    def _format_insight_title(key: str) -> str:
        mapping = {
            "select-from": "SELECT + FROM",
            "group-by": "GROUP BY",
            "having": "HAVING",
            "join": "JOIN",
            "left-join": "LEFT JOIN",
            "where": "WHERE",
            "order-by": "ORDER BY",
            "distinct": "DISTINCT",
            "select": "SELECT",
            "3nf": "3NF",
            "kardinalitaet": "Kardinalität",
        }
        return mapping.get(key, key.replace("-", " ").title())

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
            expanded.update(keyword_knowledge.SYNONYMS.get(token, set()))

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
