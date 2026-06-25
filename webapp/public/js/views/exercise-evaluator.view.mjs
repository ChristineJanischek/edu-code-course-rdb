export class ExerciseEvaluatorView {
  constructor(feedbackElement) {
    this.feedbackElement = feedbackElement;
  }

  render(result) {
    if (!this.feedbackElement) {
      return;
    }

    this.feedbackElement.textContent = result.message;
    const feedbackBox = this.feedbackElement.closest(".feedback-box");
    if (feedbackBox) {
      feedbackBox.setAttribute("data-state", result.state || "warning");
    }
  }
}
