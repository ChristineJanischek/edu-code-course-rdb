import { ApiClient } from "../api-client.mjs";
import { sanitizeStudentFacingMessage, withRetry } from "../error-handler.mjs";

const COURSE_NAME = "Kurs: RDB";
const MODULE_DATASET_KEY = "foodtrucknetz_uebung";
const MODULE_EERM_IMAGE = "/generated/klassenarbeiten/foodtrucknetz_2025.png";
const STORAGE_KEY = "rdb-foodtruck-guided-workflow-v1";

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function compactText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

class SqlLearningStateStore {
  constructor(totalTasks) {
    this.totalTasks = Math.max(0, Number(totalTasks) || 0);
    this.state = this.load();
  }

  load() {
    const fallback = {
      currentTaskIndex: 0,
      unlockedTaskIndex: 0,
      taskAttempts: {},
      taskSolved: {},
      errorStats: {},
      sqlByTaskId: {},
      lastUpdatedAt: null,
    };

    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return fallback;
      }

      const parsed = JSON.parse(raw);
      const currentTaskIndex = Number(parsed?.currentTaskIndex);
      const unlockedTaskIndex = Number(parsed?.unlockedTaskIndex);

      return {
        currentTaskIndex: Number.isInteger(currentTaskIndex) ? currentTaskIndex : 0,
        unlockedTaskIndex: Number.isInteger(unlockedTaskIndex) ? unlockedTaskIndex : 0,
        taskAttempts: parsed?.taskAttempts && typeof parsed.taskAttempts === "object" ? parsed.taskAttempts : {},
        taskSolved: parsed?.taskSolved && typeof parsed.taskSolved === "object" ? parsed.taskSolved : {},
        errorStats: parsed?.errorStats && typeof parsed.errorStats === "object" ? parsed.errorStats : {},
        sqlByTaskId: parsed?.sqlByTaskId && typeof parsed.sqlByTaskId === "object" ? parsed.sqlByTaskId : {},
        lastUpdatedAt: typeof parsed?.lastUpdatedAt === "string" ? parsed.lastUpdatedAt : null,
      };
    } catch {
      return fallback;
    }
  }

  save() {
    this.state.lastUpdatedAt = new Date().toISOString();
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
  }

  getCurrentTaskIndex() {
    return this.clamp(this.state.currentTaskIndex, 0, Math.max(this.totalTasks - 1, 0));
  }

  setCurrentTaskIndex(index) {
    this.state.currentTaskIndex = this.clamp(index, 0, Math.max(this.totalTasks - 1, 0));
    this.save();
  }

  getUnlockedTaskIndex() {
    return this.clamp(this.state.unlockedTaskIndex, 0, Math.max(this.totalTasks - 1, 0));
  }

  unlockThrough(index) {
    const next = this.clamp(index, 0, Math.max(this.totalTasks - 1, 0));
    this.state.unlockedTaskIndex = Math.max(this.getUnlockedTaskIndex(), next);
    this.save();
  }

  saveSqlDraft(taskId, sqlText) {
    this.state.sqlByTaskId[taskId] = String(sqlText || "");
    this.save();
  }

  loadSqlDraft(taskId) {
    return String(this.state.sqlByTaskId[taskId] || "");
  }

  incrementAttempt(taskId) {
    const current = Number(this.state.taskAttempts[taskId] || 0);
    this.state.taskAttempts[taskId] = current + 1;
    this.save();
    return this.state.taskAttempts[taskId];
  }

  markSolved(taskId) {
    this.state.taskSolved[taskId] = true;
    this.save();
  }

  isSolved(taskId) {
    return Boolean(this.state.taskSolved[taskId]);
  }

  recordError(signature) {
    const key = String(signature || "Unbekannter Fehler").slice(0, 180);
    const current = Number(this.state.errorStats[key] || 0);
    this.state.errorStats[key] = current + 1;
    this.save();
  }

  attemptsFor(taskId) {
    return Number(this.state.taskAttempts[taskId] || 0);
  }

  buildSummary(tasks) {
    const byTask = tasks.map((task) => ({
      id: task.id,
      title: task.title,
      attempts: this.attemptsFor(task.id),
      solved: this.isSolved(task.id),
    }));

    const errorEntries = Object.entries(this.state.errorStats)
      .map(([error, count]) => ({ error, count: Number(count || 0) }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);

    const solvedCount = byTask.filter((entry) => entry.solved).length;

    return {
      solvedCount,
      totalTasks: tasks.length,
      byTask,
      errorEntries,
    };
  }

  clamp(value, min, max) {
    return Math.min(max, Math.max(min, Number(value) || 0));
  }
}

class FoodtruckModuleRepository {
  async load(moduleHref) {
    const response = await fetch(moduleHref, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error("Modul konnte nicht geladen werden.");
    }

    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, "text/html");
    const tasks = this.parseTasks(doc);

    return {
      tasks,
      info: this.parseInfo(doc),
    };
  }

  parseTasks(doc) {
    const cards = Array.from(doc.querySelectorAll(".card.exercise"));
    return cards
      .map((card, index) => {
        const id = card.id || `a${index + 1}`;
        const heading = compactText(card.querySelector(".task strong")?.textContent || `Aufgabe ${index + 1}`);

        const taskClone = card.querySelector(".task")?.cloneNode(true);
        if (taskClone) {
          const strong = taskClone.querySelector("strong");
          if (strong) {
            strong.remove();
          }
        }

        const description = compactText(taskClone?.textContent || "");
        const hint = compactText(card.querySelector(".hint")?.textContent || "");
        const topic = compactText(card.querySelector(".topic-badge")?.textContent || "");
        const solutionSql = String(card.querySelector(`.sol-box pre`)?.textContent || "").trim();

        return {
          id,
          number: index + 1,
          title: heading,
          description,
          hint,
          topic,
          solutionSql,
        };
      })
      .filter((task) => task.solutionSql);
  }

  parseInfo(doc) {
    const schemaHeading = Array.from(doc.querySelectorAll("h3")).find((node) => compactText(node.textContent).toLowerCase().includes("schema-kurzreferenz"));
    const schemaCard = schemaHeading ? schemaHeading.closest(".card") : null;
    const schemaItems = Array.from(schemaCard?.querySelectorAll(".schema-table") || []).slice(0, 6).map((item) => {
      const title = compactText(item.querySelector("strong")?.textContent || "Tabelle");
      const body = compactText(item.querySelector("code")?.textContent || "");
      return { title, body };
    });

    return {
      schemaItems,
      clauseOrder: "SELECT -> FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> ORDER BY",
      tips: [
        "Nutze fuer jede Aufgabe zuerst die Tabellen- und Schluesselanalyse.",
        "Filter auf Zeilen gehoeren in WHERE, Filter auf Gruppen in HAVING.",
        "Bei LEFT JOIN mit IS NULL pruefst du fehlende Treffer auf der rechten Seite.",
      ],
      links: [
        { title: "UE01 FoodTruckNetz (komplettes Modul)", href: "/generated/uebungen/UE01_foodtrucknetz_sql_abfragen.html" },
        { title: "Stichwortverzeichnis RDB", href: "/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html" },
      ],
    };
  }
}

class SqlLearningView {
  constructor(options) {
    this.courseName = options.courseName;
    this.taskTitle = options.taskTitle;
    this.taskDescription = options.taskDescription;
    this.taskTopic = options.taskTopic;
    this.taskLink = options.taskLink;
    this.modulePosition = options.modulePosition;
    this.infoText = options.infoText;
    this.infoContent = options.infoContent;
    this.footerStatus = options.footerStatus;
    this.editor = options.editor;
    this.logBox = options.logBox;
    this.logText = options.logText;
    this.logHint = options.logHint;
    this.resultGrid = options.resultGrid;
    this.modelerCanvas = options.modelerCanvas;
  }

  renderTask(task, totalTasks, attemptCount, solved, moduleHref) {
    if (this.courseName) {
      this.courseName.textContent = COURSE_NAME;
    }
    if (this.taskTitle) {
      this.taskTitle.textContent = `Aufgabe ${task.number}: ${task.title}`;
    }
    if (this.taskDescription) {
      this.taskDescription.textContent = task.description;
    }
    if (this.taskTopic) {
      const solvedBadge = solved ? " | Status: geloest" : " | Status: offen";
      this.taskTopic.textContent = `Thema: ${task.topic || "SQL"} | Testversuche: ${attemptCount}${solvedBadge}`;
    }
    if (this.modulePosition) {
      this.modulePosition.textContent = `Aufgabe ${task.number} von ${totalTasks}`;
    }
    if (this.taskLink) {
      this.taskLink.href = `${moduleHref}#${task.id}`;
      this.taskLink.textContent = `Aufgabe ${task.number} im Modul oeffnen`;
    }
  }

  renderInfo(task, info) {
    if (this.infoText) {
      this.infoText.textContent = `Didaktik fuer Aufgabe ${task.number}: ${task.title}`;
    }

    if (!this.infoContent) {
      return;
    }

    const schemaHtml = info.schemaItems
      .map((entry) => `<div class="schema-mini-item"><strong>${escapeHtml(entry.title)}</strong><br>${escapeHtml(entry.body)}</div>`)
      .join("");

    const tipsHtml = info.tips.map((tip) => `<li>${escapeHtml(tip)}</li>`).join("");
    const linksHtml = info.links
      .map((link) => `<li><a href="${escapeHtml(link.href)}" target="_blank" rel="noopener">${escapeHtml(link.title)}</a></li>`)
      .join("");

    this.infoContent.innerHTML = `
      <section>
        <strong>Klauselreihenfolge</strong>
        <p class="muted">${escapeHtml(info.clauseOrder)}</p>
      </section>
      <section class="schema-mini">
        <strong>Schema-Kurzreferenz</strong>
        ${schemaHtml}
      </section>
      <section>
        <strong>Tipps zur Loesungsfindung (Sek II)</strong>
        <ul>${tipsHtml}</ul>
      </section>
      <section>
        <strong>Weiterfuehrende Materialien</strong>
        <ul>${linksHtml}</ul>
      </section>
    `;
  }

  renderModeler(imageHref) {
    if (!this.modelerCanvas) {
      return;
    }

    this.modelerCanvas.innerHTML = `
      <img src="${escapeHtml(imageHref)}" alt="EERM FoodTruckNetz" loading="lazy">
      <p class="muted">EERM FoodTruckNetz fuer Aufgabe und Information.</p>
    `;
  }

  renderLog(message, hint = "", state = "warning") {
    if (this.logBox) {
      this.logBox.dataset.state = state;
    }
    if (this.logText) {
      this.logText.textContent = sanitizeStudentFacingMessage(message) || "Status aktualisiert.";
    }
    if (this.logHint) {
      this.logHint.textContent = sanitizeStudentFacingMessage(hint) || "";
    }
  }

  renderResult(data) {
    if (!this.resultGrid) {
      return;
    }

    const buildTable = (title, payload) => {
      const columns = Array.isArray(payload?.columns) ? payload.columns : [];
      const rows = Array.isArray(payload?.rows) ? payload.rows.slice(0, 12) : [];

      const head = columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("");
      const body = rows
        .map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell === null ? "NULL" : String(cell))}</td>`).join("")}</tr>`)
        .join("");

      return `
        <article class="sql-result-card">
          <h4>${escapeHtml(title)} (${Number(payload?.row_count || 0)} Zeilen)</h4>
          ${columns.length > 0 ? `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>` : `<p class="muted">Keine Daten.</p>`}
        </article>
      `;
    };

    this.resultGrid.hidden = false;
    this.resultGrid.innerHTML = `${buildTable("Deine Abfrage", data.actual)}${buildTable("Referenz", data.expected)}`;
  }

  clearResult() {
    if (!this.resultGrid) {
      return;
    }
    this.resultGrid.hidden = true;
    this.resultGrid.innerHTML = "";
  }

  renderSummary(summary) {
    if (!this.infoText || !this.infoContent) {
      return;
    }

    this.infoText.textContent = "Modul abgeschlossen: Abschlussauswertung";

    const taskRows = summary.byTask
      .map((entry) => `<tr><td>${escapeHtml(entry.id)}</td><td>${escapeHtml(entry.title)}</td><td>${entry.attempts}</td><td>${entry.solved ? "ja" : "nein"}</td></tr>`)
      .join("");

    const errorRows = summary.errorEntries.length > 0
      ? summary.errorEntries.map((entry) => `<li>${escapeHtml(entry.error)} (${entry.count})</li>`).join("")
      : "<li>Keine wiederkehrenden Fehler erfasst.</li>";

    this.infoContent.innerHTML = `
      <section>
        <strong>Ergebnis</strong>
        <p class="muted">Geloeste Aufgaben: ${summary.solvedCount} von ${summary.totalTasks}</p>
      </section>
      <section>
        <strong>Testversuche je Aufgabe</strong>
        <table>
          <thead><tr><th>Aufgabe</th><th>Titel</th><th>Versuche</th><th>Geloest</th></tr></thead>
          <tbody>${taskRows}</tbody>
        </table>
      </section>
      <section>
        <strong>Haeufige Fehler</strong>
        <ul>${errorRows}</ul>
      </section>
    `;
  }

  setFooterStatus(message) {
    if (this.footerStatus) {
      this.footerStatus.textContent = sanitizeStudentFacingMessage(message) || "Lernpfad bereit.";
    }
  }
}

class CourseWorkflowController {
  constructor(options = {}) {
    this.exerciseLinks = Array.isArray(options.exerciseLinks) ? options.exerciseLinks : [];
    this.actionLinks = options.actionLinks || [];
    this.editor = options.editor;
    this.exportButton = options.exportButton;
    this.exportPreview = options.exportPreview;
    this.leftTaskTab = options.leftTaskTab;
    this.leftInfoTab = options.leftInfoTab;
    this.rightEditorTab = options.rightEditorTab;

    this.apiClient = new ApiClient(window.PYTHON_API_URL || "/api-proxy.php", { timeoutMs: 15000 });
    this.repository = new FoodtruckModuleRepository();
    this.view = new SqlLearningView(options.view);

    this.moduleHref = null;
    this.tasks = [];
    this.info = null;
    this.store = null;
  }

  async bind() {
    this.moduleHref = this.resolveFoodtruckModuleHref();
    if (!this.moduleHref || !this.editor) {
      this.view.setFooterStatus("Kein UE01-Modul gefunden.");
      return;
    }

    try {
      const payload = await this.repository.load(this.moduleHref);
      this.tasks = payload.tasks;
      this.info = payload.info;
    } catch (error) {
      this.view.setFooterStatus(`Modulstart fehlgeschlagen: ${error.message}`);
      return;
    }

    if (this.tasks.length === 0) {
      this.view.setFooterStatus("Keine Aufgaben im UE01-Modul erkannt.");
      return;
    }

    this.store = new SqlLearningStateStore(this.tasks.length);

    this.actionLinks.forEach((link) => {
      link.addEventListener("click", (event) => this.onAction(event, link));
    });

    this.editor.addEventListener("input", () => {
      const task = this.getCurrentTask();
      if (task) {
        this.store.saveSqlDraft(task.id, this.editor.value);
      }
    });

    this.exportButton?.addEventListener("click", () => this.exportState());

    this.activateInitialTabs();
    this.view.renderModeler(MODULE_EERM_IMAGE);
    this.renderCurrentTask();
    this.view.setFooterStatus("Aufgabe 1 geladen. Schreibe deine SQL-Abfrage und klicke auf testen.");
  }

  resolveFoodtruckModuleHref() {
    const direct = this.exerciseLinks.find((entry) => String(entry?.href || "").includes("UE01_foodtrucknetz_sql_abfragen.html"));
    if (direct && direct.href) {
      return String(direct.href);
    }
    const fallback = this.exerciseLinks[0];
    return fallback?.href ? String(fallback.href) : null;
  }

  activateInitialTabs() {
    this.leftTaskTab?.click();
    this.rightEditorTab?.click();
  }

  getCurrentTask() {
    if (!this.store || this.tasks.length === 0) {
      return null;
    }
    return this.tasks[this.store.getCurrentTaskIndex()] || null;
  }

  renderCurrentTask() {
    const task = this.getCurrentTask();
    if (!task || !this.store) {
      return;
    }

    const attempts = this.store.attemptsFor(task.id);
    const solved = this.store.isSolved(task.id);

    this.view.renderTask(task, this.tasks.length, attempts, solved, this.moduleHref);
    this.view.renderInfo(task, this.info);
    this.editor.value = this.store.loadSqlDraft(task.id);
    this.view.clearResult();
    this.view.renderLog("Noch kein Test gestartet.", "Hinweise erscheinen hier mit Zeilenbezug, sobald die Abfrage getestet wird.", "warning");
    this.updateExportPreview();
  }

  onAction(event, link) {
    event.preventDefault();
    const action = String(link.dataset.courseAction || "").trim();

    if (action === "back") {
      this.moveTask(-1);
      return;
    }
    if (action === "next") {
      this.moveTask(1);
      return;
    }
    if (action === "save") {
      this.store?.save();
      this.view.setFooterStatus("Arbeitsstand gespeichert.");
      return;
    }
    if (action === "test") {
      this.runTest();
    }
  }

  moveTask(step) {
    if (!this.store) {
      return;
    }

    const current = this.store.getCurrentTaskIndex();
    const next = current + step;

    if (next < 0) {
      this.view.setFooterStatus("Du bist bereits bei Aufgabe 1.");
      return;
    }

    if (next >= this.tasks.length) {
      const summary = this.store.buildSummary(this.tasks);
      this.view.renderSummary(summary);
      this.leftInfoTab?.click();
      this.view.setFooterStatus("Modul abgeschlossen. Abschlussauswertung wurde erstellt.");
      return;
    }

    const unlocked = this.store.getUnlockedTaskIndex();
    if (next > unlocked) {
      this.view.setFooterStatus("Bitte loese zuerst die aktuelle Aufgabe erfolgreich und klicke danach auf weiter.");
      return;
    }

    this.store.setCurrentTaskIndex(next);
    this.renderCurrentTask();
    this.leftTaskTab?.click();
    this.view.setFooterStatus(`Aufgabe ${next + 1} geladen.`);
  }

  async runTest() {
    if (!this.store) {
      return;
    }

    const task = this.getCurrentTask();
    if (!task) {
      return;
    }

    const sqlText = String(this.editor.value || "").trim();
    if (!sqlText) {
      this.view.renderLog("Bitte gib zuerst eine SQL-Abfrage ein.", "Starte mit SELECT ... FROM ...", "warning");
      this.view.setFooterStatus("Test abgebrochen: Keine SQL-Abfrage eingegeben.");
      return;
    }

    this.store.saveSqlDraft(task.id, sqlText);
    const attempts = this.store.incrementAttempt(task.id);
    this.view.renderLog(`Testlauf ${attempts} fuer Aufgabe ${task.number} gestartet...`, "", "warning");
    this.view.clearResult();

    try {
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/sql-sandbox/execute", {
        dataset_key: MODULE_DATASET_KEY,
        candidate_sql: sqlText,
        reference_sql: task.solutionSql,
      }), { attempts: 2, baseDelayMs: 180 });

      const ok = Boolean(response?.ok);
      if (ok) {
        this.store.markSolved(task.id);
        const currentIndex = this.store.getCurrentTaskIndex();
        this.store.unlockThrough(Math.min(currentIndex + 1, this.tasks.length - 1));
        this.view.renderLog(
          `Aufgabe ${task.number} korrekt geloest (Score ${Number(response?.score || 0)}%).`,
          currentIndex < this.tasks.length - 1
            ? "Klicke auf weiter, um die naechste Aufgabe zu laden."
            : "Alle Aufgaben bearbeitet. Klicke auf weiter fuer die Abschlussauswertung.",
          "success"
        );
        this.view.renderResult(response);
        this.view.setFooterStatus(`Aufgabe ${task.number} erfolgreich getestet.`);
      } else {
        const feedback = response?.feedback || {};
        const hint = [
          Array.isArray(feedback?.missing_samples) && feedback.missing_samples.length > 0
            ? `Fehlende Zeilen: ${feedback.missing_samples.slice(0, 3).join(" | ")}`
            : "",
          Array.isArray(feedback?.extra_samples) && feedback.extra_samples.length > 0
            ? `Zusaetzliche Zeilen: ${feedback.extra_samples.slice(0, 3).join(" | ")}`
            : "",
        ].filter(Boolean).join(". ");

        this.store.recordError("Ergebnissatz weicht ab");
        this.view.renderLog(
          feedback?.message || "Die Abfrage ist syntaktisch gueltig, aber das Ergebnis weicht ab.",
          hint || "Vergleiche SELECT-Spalten, Filterbedingungen und GROUP BY/HAVING mit der Aufgabenstellung.",
          "warning"
        );
        this.view.renderResult(response);
        this.view.setFooterStatus(`Aufgabe ${task.number} noch nicht korrekt. Bitte korrigieren und erneut testen.`);
      }
    } catch (error) {
      const parsed = this.parseSqlError(error?.message || "SQL-Test fehlgeschlagen.");
      this.store.recordError(parsed.signature);
      this.view.renderLog(parsed.message, parsed.hint, "error");
      this.view.setFooterStatus(`SQL-Fehler in Aufgabe ${task.number}. Bitte Hinweis pruefen und erneut testen.`);
    }

    this.renderCurrentTask();
  }

  parseSqlError(rawMessage) {
    const message = sanitizeStudentFacingMessage(rawMessage) || "SQL-Test fehlgeschlagen.";
    const lineMatch = message.match(/line\s+(\d+)/i);
    const lineText = lineMatch ? `Zeile ${lineMatch[1]}` : "Zeile unbekannt";

    let hint = "Pruefe Klauselreihenfolge, Aliasnamen und Klammern."
    let signature = "SQL-Fehler";
    const lowered = message.toLowerCase();

    if (lowered.includes("syntax")) {
      signature = "Syntaxfehler";
      hint = `${lineText}: Syntax pruefen (Komma, Klammern, fehlende Schluesselwoerter).`;
    } else if (lowered.includes("unknown column")) {
      signature = "Unbekannte Spalte";
      hint = `${lineText}: Spaltenname oder Tabellenalias stimmt nicht.`;
    } else if (lowered.includes("unknown table")) {
      signature = "Unbekannte Tabelle";
      hint = `${lineText}: Tabellenname in FROM/JOIN pruefen.`;
    } else if (lowered.includes("group by")) {
      signature = "GROUP-BY-Regel";
      hint = `${lineText}: Nicht aggregierte Ausgabespalten muessen in GROUP BY stehen.`;
    }

    return {
      message,
      hint,
      signature,
    };
  }

  updateExportPreview() {
    if (!this.exportPreview || !this.store) {
      return;
    }

    const summary = this.store.buildSummary(this.tasks);
    this.exportPreview.value = JSON.stringify({
      course: COURSE_NAME,
      module: this.moduleHref,
      state: this.store.state,
      summary,
      exportedAt: new Date().toISOString(),
    }, null, 2);
  }

  exportState() {
    this.updateExportPreview();
    const content = this.exportPreview?.value || "{}";
    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "rdb-foodtruck-progress.json";
    link.click();
    URL.revokeObjectURL(url);
    this.view.setFooterStatus("Arbeitsstand exportiert: rdb-foodtruck-progress.json");
  }
}

export function initCourseWorkflowController() {
  const content = window.LEARNING_CONTENT || {};
  const exerciseLinks = Array.isArray(content.exerciseLinks) ? content.exerciseLinks : [];

  new CourseWorkflowController({
    exerciseLinks,
    actionLinks: Array.from(document.querySelectorAll("[data-course-action]")),
    editor: document.getElementById("practiceEditor-0"),
    exportButton: document.getElementById("exportWorkspaceButton"),
    exportPreview: document.getElementById("exportPreview"),
    leftTaskTab: document.getElementById("tab-left-task"),
    leftInfoTab: document.getElementById("tab-left-info"),
    rightEditorTab: document.getElementById("tab-right-editor-0"),
    view: {
      courseName: document.getElementById("currentCourseName"),
      taskTitle: document.getElementById("currentTaskTitle"),
      taskDescription: document.getElementById("currentTaskDescription"),
      taskTopic: document.getElementById("currentTaskTopic"),
      taskLink: document.getElementById("currentTaskLink"),
      modulePosition: document.getElementById("currentModulePosition"),
      infoText: document.getElementById("currentInfoText"),
      infoContent: document.getElementById("currentInfoContent"),
      footerStatus: document.getElementById("workflowStatus"),
      editor: document.getElementById("practiceEditor-0"),
      logBox: document.getElementById("sqlTestLogBox"),
      logText: document.getElementById("sqlTestLog"),
      logHint: document.getElementById("sqlTestHint"),
      resultGrid: document.getElementById("sqlResultGrid"),
      modelerCanvas: document.getElementById("modelerCanvas"),
    },
  }).bind();
}
