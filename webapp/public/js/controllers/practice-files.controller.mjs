class PracticeFilesController {
  constructor(inputElement, listElement) {
    this.inputElement = inputElement;
    this.listElement = listElement;
  }

  bind() {
    if (!this.inputElement || !this.listElement) {
      return;
    }

    this.inputElement.addEventListener("change", () => this.renderFiles());
    this.renderFiles();
  }

  renderFiles() {
    this.listElement.innerHTML = "";

    const files = Array.from(this.inputElement.files || []);
    if (files.length === 0) {
      const emptyItem = document.createElement("li");
      emptyItem.textContent = "Noch keine Dateien ausgewählt.";
      this.listElement.appendChild(emptyItem);
      return;
    }

    files.forEach((file) => {
      const item = document.createElement("li");
      const fileSizeKb = Math.max(1, Math.round(file.size / 1024));
      item.textContent = `${file.name} (${fileSizeKb} KB)`;
      this.listElement.appendChild(item);
    });
  }
}

export function initPracticeFilesController() {
  new PracticeFilesController(
    document.getElementById("workingFiles"),
    document.getElementById("workingFileList")
  ).bind();
}
