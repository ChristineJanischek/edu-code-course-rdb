class SelfCheckController {
  constructor(listElement, progressElement) {
    this.listElement = listElement;
    this.progressElement = progressElement;
  }

  bind() {
    if (!this.listElement || !this.progressElement) {
      return;
    }

    this.listElement.addEventListener("change", () => this.updateProgress());
    this.updateProgress();
  }

  updateProgress() {
    const checkboxes = Array.from(this.listElement.querySelectorAll('input[type="checkbox"]'));
    const total = checkboxes.length;
    const completed = checkboxes.filter((checkbox) => checkbox.checked).length;

    this.progressElement.textContent = `Fortschritt: ${completed} von ${total} Kriterien erfüllt.`;
  }
}

export function initSelfCheckController() {
  new SelfCheckController(
    document.getElementById("selfCheckList"),
    document.getElementById("selfCheckProgress")
  ).bind();
}
