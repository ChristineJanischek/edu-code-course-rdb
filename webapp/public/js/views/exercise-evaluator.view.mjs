import { sanitizeStudentFacingMessage } from "../error-handler.mjs";

export class ExerciseEvaluatorView {
  constructor(feedbackElement) {
    this.feedbackElement = feedbackElement;
  }

  render(result) {
    if (!this.feedbackElement) {
      return;
    }

    const safeMessage = sanitizeStudentFacingMessage(result.message) || "Keine Rückmeldung verfügbar.";
    this.feedbackElement.textContent = safeMessage;
    const feedbackBox = this.feedbackElement.closest(".feedback-box");
    if (feedbackBox) {
      feedbackBox.setAttribute("data-state", result.state || "warning");
    }
  }
}
