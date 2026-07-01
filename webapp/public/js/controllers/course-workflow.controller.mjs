class CourseWorkflowController {
  constructor(options = {}) {
    this.exerciseLinks = Array.isArray(options.exerciseLinks) ? options.exerciseLinks : [];
    this.taskTitle = options.taskTitle;
    this.taskDescription = options.taskDescription;
    this.taskLink = options.taskLink;
    this.infoText = options.infoText;
    this.modulePosition = options.modulePosition;
    this.footerStatus = options.footerStatus;
    this.actionLinks = options.actionLinks || [];
    this.editorElements = options.editorElements || [];
    this.exportPreview = options.exportPreview;
    this.exportButton = options.exportButton;
    this.defaultKeywordTab = options.defaultKeywordTab;
    this.storageKey = "rdb-course-progress-v1";
    this.state = this.loadState();
    this.fileNames = this.editorElements
      .map((element) => String(element.dataset.editorFile || "").trim())
      .filter(Boolean);
  }

  bind() {
    if (this.exerciseLinks.length === 0) {
      this.setFooterStatus("Keine Kursmodule gefunden.");
      return;
    }

    this.editorElements.forEach((element) => {
      element.addEventListener("input", () => this.onEditorInput(element));
    });

    this.actionLinks.forEach((link) => {
      link.addEventListener("click", (event) => this.onActionClick(event, link));
    });

    this.exportButton?.addEventListener("click", () => this.exportWorkspaceState());

    this.applyStoredEditorContent();
    this.renderCurrentModule();
    this.updateExportPreview();

    // Default in this UI iteration: open keyword search on load.
    this.defaultKeywordTab?.click();
  }

  loadState() {
    const fallback = {
      moduleIndex: 0,
      fileContents: {},
      lastUpdatedAt: null,
    };

    try {
      const raw = window.localStorage.getItem(this.storageKey);
      if (!raw) {
        return fallback;
      }

      const parsed = JSON.parse(raw);
      const moduleIndex = Number(parsed?.moduleIndex);

      return {
        moduleIndex: Number.isInteger(moduleIndex) ? moduleIndex : 0,
        fileContents: this.isObject(parsed?.fileContents) ? parsed.fileContents : {},
        lastUpdatedAt: typeof parsed?.lastUpdatedAt === "string" ? parsed.lastUpdatedAt : null,
      };
    } catch {
      return fallback;
    }
  }

  saveState() {
    this.state.lastUpdatedAt = new Date().toISOString();
    window.localStorage.setItem(this.storageKey, JSON.stringify(this.state));
    this.updateExportPreview();
  }

  isObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  onEditorInput(element) {
    const fileName = String(element.dataset.editorFile || "").trim();
    if (!fileName) {
      return;
    }

    this.state.fileContents[fileName] = element.value;
    this.saveState();
    this.setFooterStatus(`Zwischengespeichert: ${fileName}`);
  }

  onActionClick(event, link) {
    event.preventDefault();
    const action = String(link.dataset.courseAction || "").trim();

    if (action === "next") {
      this.moveModule(1);
      return;
    }

    if (action === "back") {
      this.moveModule(-1);
      return;
    }

    if (action === "save") {
      this.saveState();
      this.setFooterStatus("Arbeitsstand gespeichert.");
      return;
    }

    if (action === "test") {
      this.setFooterStatus("Testen ist als Workflow-Aktion vorgemerkt und wird im nächsten Schritt integriert.");
    }
  }

  moveModule(step) {
    const maxIndex = Math.max(0, this.exerciseLinks.length - 1);
    const nextIndex = this.clamp(this.state.moduleIndex + step, 0, maxIndex);

    if (nextIndex === this.state.moduleIndex) {
      this.setFooterStatus(step > 0 ? "Du bist bereits beim letzten Modul." : "Du bist bereits beim ersten Modul.");
      return;
    }

    this.state.moduleIndex = nextIndex;
    this.saveState();
    this.renderCurrentModule();

    const current = this.exerciseLinks[this.state.moduleIndex];
    const title = current?.title || `Modul ${this.state.moduleIndex + 1}`;
    this.setFooterStatus(`Geladen: ${title}`);
  }

  clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  renderCurrentModule() {
    const maxIndex = Math.max(0, this.exerciseLinks.length - 1);
    this.state.moduleIndex = this.clamp(this.state.moduleIndex, 0, maxIndex);

    const current = this.exerciseLinks[this.state.moduleIndex] || {};
    const title = String(current.title || `Modul ${this.state.moduleIndex + 1}`);
    const description = String(current.description || "Keine Zusatzinformation verfügbar.");
    const href = String(current.href || "#");

    if (this.taskTitle) {
      this.taskTitle.textContent = title;
    }
    if (this.taskDescription) {
      this.taskDescription.textContent = description;
    }
    if (this.taskLink) {
      this.taskLink.href = href;
      this.taskLink.textContent = href === "#" ? "Modul-Link nicht verfügbar" : "Modul öffnen";
    }
    if (this.infoText) {
      this.infoText.textContent = description;
    }
    if (this.modulePosition) {
      this.modulePosition.textContent = `Modul ${this.state.moduleIndex + 1} von ${this.exerciseLinks.length}`;
    }
  }

  applyStoredEditorContent() {
    this.editorElements.forEach((element) => {
      const fileName = String(element.dataset.editorFile || "").trim();
      if (!fileName) {
        return;
      }

      const savedContent = this.state.fileContents[fileName];
      if (typeof savedContent === "string") {
        element.value = savedContent;
      }
    });
  }

  updateExportPreview() {
    if (!this.exportPreview) {
      return;
    }

    const current = this.exerciseLinks[this.state.moduleIndex] || {};
    const payload = {
      course: "RDB",
      moduleIndex: this.state.moduleIndex,
      moduleTitle: current?.title || null,
      files: this.fileNames.reduce((result, fileName) => {
        result[fileName] = this.state.fileContents[fileName] || "";
        return result;
      }, {}),
      updatedAt: this.state.lastUpdatedAt,
    };

    this.exportPreview.value = JSON.stringify(payload, null, 2);
  }

  exportWorkspaceState() {
    this.updateExportPreview();
    const content = this.exportPreview?.value || "{}";
    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "rdb-arbeitsstand.json";
    link.click();

    URL.revokeObjectURL(url);
    this.setFooterStatus("Export erstellt: rdb-arbeitsstand.json");
  }

  setFooterStatus(message) {
    if (this.footerStatus) {
      this.footerStatus.textContent = message;
    }
  }
}

export function initCourseWorkflowController() {
  const content = window.LEARNING_CONTENT || {};
  const exerciseLinks = Array.isArray(content.exerciseLinks) ? content.exerciseLinks : [];

  new CourseWorkflowController({
    exerciseLinks,
    taskTitle: document.getElementById("currentTaskTitle"),
    taskDescription: document.getElementById("currentTaskDescription"),
    taskLink: document.getElementById("currentTaskLink"),
    infoText: document.getElementById("currentInfoText"),
    modulePosition: document.getElementById("currentModulePosition"),
    footerStatus: document.getElementById("workflowStatus"),
    actionLinks: Array.from(document.querySelectorAll("[data-course-action]")),
    editorElements: Array.from(document.querySelectorAll(".js-course-editor")),
    exportPreview: document.getElementById("exportPreview"),
    exportButton: document.getElementById("exportWorkspaceButton"),
    defaultKeywordTab: document.getElementById("tab-left-keywords"),
  }).bind();
}
