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
}
