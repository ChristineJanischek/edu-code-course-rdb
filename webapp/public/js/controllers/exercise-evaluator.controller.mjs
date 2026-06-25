import { ExerciseEvaluatorModel } from "../models/exercise-evaluator.model.mjs";
import { ExerciseEvaluatorView } from "../views/exercise-evaluator.view.mjs";

class ExerciseEvaluatorController {
  constructor(rootElement) {
    this.rootElement = rootElement;
    this.input = rootElement.querySelector(".exercise-input");
    this.button = rootElement.querySelector(".exercise-check");
    this.view = new ExerciseEvaluatorView(rootElement.querySelector(".feedback-box p"));

    const requiredTokens = (rootElement.dataset.checks || "")
      .split("|")
      .map((token) => token.trim())
      .filter(Boolean);
    this.model = new ExerciseEvaluatorModel(requiredTokens);
  }

  bind() {
    if (!this.button) {
      return;
    }

    this.button.addEventListener("click", () => {
      const result = this.model.evaluate(this.input?.value || "");
      this.view.render(result);
    });
  }
}

export function initExerciseEvaluatorControllers() {
  for (const card of document.querySelectorAll(".exercise-card")) {
    new ExerciseEvaluatorController(card).bind();
  }
}
