export class AssistantModel {
  constructor(formElement) {
    this.formElement = formElement;
  }

  createPayload() {
    if (!this.formElement) {
      return null;
    }

    const formData = new FormData(this.formElement);
    const question = (formData.get("question") || "").toString().trim();
    const actorRole = (formData.get("actor_role") || "student").toString().trim() || "student";

    return {
      question,
      actor_role: actorRole,
      topic: "relationale-datenbanken",
      language: "de",
      learner_level: "sek2",
    };
  }

  validate(payload) {
    if (!payload || typeof payload.question !== "string" || payload.question.length < 8) {
      return ["Bitte formuliere eine Frage mit mindestens 8 Zeichen."];
    }
    if (payload.question.length > 4000) {
      return ["Die Frage ist zu lang."];
    }
    return [];
  }

  createGuidedPayload(mode, editorText, fileName) {
    const normalizedEditorText = (editorText || "").toString().trim();
    const normalizedFileName = (fileName || "").toString().trim() || "unbenannt";

    const basePrompt = mode === "check"
      ? "Bitte prüfe meinen aktuellen Stand didaktisch und nenne nur Verbesserungshinweise, keine fertige Lösung."
      : "Bitte gib mir den nächsten sinnvollen Schritt für meine eigenständige Lösungsfindung, ohne die komplette Antwort vorwegzunehmen.";

    const draftSnippet = normalizedEditorText
      ? ` Aktueller Stand in ${normalizedFileName}: ${normalizedEditorText.slice(0, 1400)}`
      : ` Es liegt noch kein Entwurf in ${normalizedFileName} vor.`;

    return {
      question: `${basePrompt}${draftSnippet}`,
      actor_role: "student",
      topic: "relationale-datenbanken",
      language: "de",
      learner_level: "sek2",
      metadata: {
        mode,
        file_name: normalizedFileName,
      },
    };
  }
}
