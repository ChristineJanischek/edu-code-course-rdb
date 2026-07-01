import { sanitizeStudentFacingMessage } from "../error-handler.mjs";

export class AssistantView {
  constructor(formElement, statusElement, hintElement) {
    this.formElement = formElement;
    this.statusElement = statusElement;
    this.hintElement = hintElement;
  }

  setStatus(message, state = "info") {
    if (!this.statusElement) {
      return;
    }
    this.statusElement.textContent = sanitizeStudentFacingMessage(message) || "Status aktualisiert.";
    this.statusElement.dataset.state = state;
  }

  renderHint(responsePayload) {
    if (!this.hintElement) {
      return;
    }
    const hint = sanitizeStudentFacingMessage(responsePayload?.hint || "Kein Hinweis verfügbar.");
    const questions = Array.isArray(responsePayload?.follow_up_questions)
      ? responsePayload.follow_up_questions.filter(Boolean)
      : [];

    this.hintElement.innerHTML = "";
    const hintParagraph = document.createElement("p");
    hintParagraph.textContent = hint;
    this.hintElement.appendChild(hintParagraph);

    if (questions.length > 0) {
      const list = document.createElement("ul");
      questions.forEach((entry) => {
        const item = document.createElement("li");
        item.textContent = sanitizeStudentFacingMessage(entry);
        list.appendChild(item);
      });
      this.hintElement.appendChild(list);
    }
  }
}
