import { ApiClient } from "../api-client.mjs";
import { sanitizeStudentFacingMessage, withRetry } from "../error-handler.mjs";

const COURSE_NAME = "Kurs: RDB";
const MODULE_CONFIGS = [
  {
    slug: "UE01_foodtrucknetz_sql_abfragen.html",
    datasetKey: "foodtrucknetz_uebung",
    eermImage: "/generated/klassenarbeiten/foodtrucknetz_2025.png",
    eermAlt: "EERM FoodTruckNetz",
    storageKey: "rdb-guided-workflow-ue01-v2",
    moduleTitle: "SQL Abfragen Foodtrucknetz DB",
  },
  {
    slug: "UE02_stadtfahrradverleih_sql_abfragen.html",
    datasetKey: "stadtfahrradverleih_uebung",
    eermImage: "/generated/klassenarbeiten/stadtfahrradverleih_2025.png",
    eermAlt: "EERM Stadtfahrradverleih",
    storageKey: "rdb-guided-workflow-ue02-v2",
    moduleTitle: "SQL Abfragen Stadtfahrradverleih DB",
  },
];

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

function normalizeHref(value) {
  return String(value || "").trim();
}

function configForHref(moduleHref) {
  const href = normalizeHref(moduleHref);
  return MODULE_CONFIGS.find((entry) => href.includes(entry.slug)) || MODULE_CONFIGS[0];
}

class SqlLearningStateStore {
  constructor(totalTasks, storageKey) {
    this.totalTasks = Math.max(0, Number(totalTasks) || 0);
    this.storageKey = String(storageKey || "rdb-guided-workflow-v2");
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
      const raw = window.localStorage.getItem(this.storageKey);
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
    window.localStorage.setItem(this.storageKey, JSON.stringify(this.state));
  }

  resetToStart() {
    this.state.currentTaskIndex = 0;
    this.save();
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

class ModuleRepository {
  async load(moduleHref) {
    const response = await fetch(moduleHref, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error("Modul konnte nicht geladen werden.");
    }

    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, "text/html");

    return {
      moduleTitle: compactText(doc.querySelector("h1")?.textContent || ""),
      moduleSubtitle: compactText(doc.querySelector(".subtitle")?.textContent || ""),
      tasks: this.parseTasks(doc),
      info: this.parseInfo(doc),
    };
  }

  parseTasks(doc) {
    const cards = Array.from(doc.querySelectorAll(".card.exercise"));

    return cards.map((card, index) => {
      const id = card.id || `a${index + 1}`;
      const heading = compactText(card.querySelector(".task strong")?.textContent || `Aufgabe ${index + 1}`);
      const difficulty = compactText(card.querySelector(".ex-header .badge")?.textContent || "");
      const topic = compactText(card.querySelector(".topic-badge")?.textContent || "");

      const taskClone = card.querySelector(".task")?.cloneNode(true);
      if (taskClone) {
        const strong = taskClone.querySelector("strong");
        if (strong) {
          strong.remove();
        }
      }

      const hintNode = card.querySelector(".hint");
      const hintHtml = String(hintNode?.innerHTML || "").trim();
      const solutionSql = String(card.querySelector(".sol-box pre")?.textContent || "").trim();
      const expectedResultHtml = String(card.querySelector(".res-box")?.innerHTML || "").trim();
      const editorPlaceholder = String(card.querySelector("textarea.sql-input")?.getAttribute("placeholder") || "");

      return {
        id,
        number: index + 1,
        title: heading,
        difficulty,
        topic,
        descriptionHtml: String(taskClone?.innerHTML || "").trim(),
        hintHtml,
        solutionSql,
        expectedResultHtml,
        editorPlaceholder,
      };
    }).filter((task) => task.solutionSql);
  }

  parseInfo(doc) {
    const schemaHeading = Array.from(doc.querySelectorAll("h3")).find((node) => compactText(node.textContent).toLowerCase().includes("schema-kurzreferenz"));
    const schemaCard = schemaHeading ? schemaHeading.closest(".card") : null;
    const schemaItems = Array.from(schemaCard?.querySelectorAll(".schema-table") || []).slice(0, 8).map((item) => {
      const title = compactText(item.querySelector("strong")?.textContent || "Tabelle");
      const body = compactText(item.querySelector("code")?.textContent || "");
      return { title, body };
    });

    const links = Array.from(doc.querySelectorAll(".nav a")).slice(0, 3).map((link) => ({
      title: compactText(link.textContent || "Link"),
      href: String(link.getAttribute("href") || "#"),
    }));

    return {
      schemaItems,
      clauseOrder: "SELECT -> FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> ORDER BY",
      tips: [
        "Nutze fuer jede Aufgabe zuerst die Tabellen- und Schluesselanalyse.",
        "Filter auf Zeilen gehoeren in WHERE, Filter auf Gruppen in HAVING.",
        "Bei LEFT JOIN mit IS NULL pruefst du fehlende Treffer auf der rechten Seite.",
      ],
      links,
    };
  }
}

class SqlLearningView {
  constructor(options) {
    this.courseName = options.courseName;
    this.taskTitle = options.taskTitle;
    this.taskDescription = options.taskDescription;
    this.taskTopic = options.taskTopic;
    this.taskHintPanel = options.taskHintPanel;
    this.taskHint = options.taskHint;
    this.taskLink = options.taskLink;
    this.moduleSelect = options.moduleSelect;
    this.moduleOpenLink = options.moduleOpenLink;
    this.modulePosition = options.modulePosition;
    this.infoText = options.infoText;
    this.infoContent = options.infoContent;
    this.footerStatus = options.footerStatus;
    this.editor = options.editor;
    this.editorHeading = options.editorHeading;
    this.editorLabel = options.editorLabel;
    this.logBox = options.logBox;
    this.logText = options.logText;
    this.logHint = options.logHint;
    this.resultGrid = options.resultGrid;
    this.modelerCanvas = options.modelerCanvas;
    this.assistantHintBox = options.assistantHintBox;
    this.assistantHintText = options.assistantHintText;
    this.assistantSolutionBox = options.assistantSolutionBox;
    this.assistantSolutionSql = options.assistantSolutionSql;
    this.assistantExpectedBox = options.assistantExpectedBox;
    this.assistantExpectedContent = options.assistantExpectedContent;
  }

  renderTask(task, totalTasks, attemptCount, solved, moduleHref) {
    if (this.courseName) {
      this.courseName.textContent = COURSE_NAME;
    }

    if (this.taskTitle) {
      this.taskTitle.textContent = `Aufgabe ${task.number}: ${task.title}`;
    }

    if (this.taskTopic) {
      const parts = [task.difficulty, task.topic].filter(Boolean);
      const solvedBadge = solved ? "Status: geloest" : "Status: offen";
      const attemptBadge = `Testversuche: ${attemptCount}`;
      this.taskTopic.textContent = [...parts, attemptBadge, solvedBadge].join(" | ");
    }

    if (this.taskDescription) {
      this.taskDescription.innerHTML = task.descriptionHtml || "";
    }

    if (this.taskHintPanel && this.taskHint) {
      if (task.hintHtml) {
        this.taskHintPanel.hidden = false;
        this.taskHint.innerHTML = task.hintHtml;
      } else {
        this.taskHintPanel.hidden = true;
        this.taskHint.textContent = "";
      }
    }

    if (this.modulePosition) {
      this.modulePosition.textContent = `Aufgabe ${task.number} von ${totalTasks}`;
    }

    if (this.taskLink) {
      this.taskLink.href = `${moduleHref}#${task.id}`;
      this.taskLink.textContent = "Aktueller Arbeitsstand öffnen";
    }

    if (this.editorHeading) {
      this.editorHeading.textContent = `SQL-Editor | Aufgabe ${task.number}`;
    }

    if (this.editorLabel) {
      this.editorLabel.textContent = "Dein SQL-Entwurf:";
    }

    if (this.editor) {
      this.editor.placeholder = task.editorPlaceholder || "SELECT ...\nFROM ...\nWHERE ...";
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

  renderModeler(imageHref, imageAltText) {
    if (!this.modelerCanvas) {
      return;
    }

    this.modelerCanvas.innerHTML = `
      <img src="${escapeHtml(imageHref)}" alt="${escapeHtml(imageAltText)}" loading="lazy">
      <p class="muted">${escapeHtml(imageAltText)} fuer Aufgabe und Information.</p>
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

  resetAssistantPanels() {
    if (this.assistantHintBox) {
      this.assistantHintBox.hidden = true;
    }
    if (this.assistantSolutionBox) {
      this.assistantSolutionBox.hidden = true;
    }
    if (this.assistantExpectedBox) {
      this.assistantExpectedBox.hidden = true;
    }
  }

  toggleHint(hintHtml) {
    if (!this.assistantHintBox || !this.assistantHintText) {
      return;
    }

    const willShow = this.assistantHintBox.hidden;
    this.assistantHintBox.hidden = !willShow;
    if (willShow) {
      this.assistantHintText.innerHTML = hintHtml || "Keine Lernhilfe verfuegbar.";
    }
  }

  toggleSolution(solutionSql) {
    if (!this.assistantSolutionBox || !this.assistantSolutionSql) {
      return;
    }

    const willShow = this.assistantSolutionBox.hidden;
    this.assistantSolutionBox.hidden = !willShow;
    if (willShow) {
      this.assistantSolutionSql.textContent = solutionSql || "Keine Musterloesung verfuegbar.";
    }
  }

  toggleExpected(expectedResultHtml) {
    if (!this.assistantExpectedBox || !this.assistantExpectedContent) {
      return;
    }

    const willShow = this.assistantExpectedBox.hidden;
    this.assistantExpectedBox.hidden = !willShow;
    if (willShow) {
      this.assistantExpectedContent.innerHTML = expectedResultHtml || "<p class=\"muted\">Kein erwartetes Ergebnis hinterlegt.</p>";
    }
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
    this.assistantActionLinks = options.assistantActionLinks || [];
    this.editor = options.editor;
    this.exportButton = options.exportButton;
    this.exportPreview = options.exportPreview;
    this.leftTaskTab = options.leftTaskTab;
    this.leftInfoTab = options.leftInfoTab;
    this.rightEditorTab = options.rightEditorTab;

    this.apiClient = new ApiClient(window.PYTHON_API_URL || "/api-proxy.php", { timeoutMs: 15000 });
    this.repository = new ModuleRepository();
    this.view = new SqlLearningView(options.view);

    this.moduleHref = null;
    this.moduleConfig = MODULE_CONFIGS[0];
    this.tasks = [];
    this.info = null;
    this.store = null;
    this.loadingModule = false;
  }

  async bind() {
    if (!this.editor) {
      this.view.setFooterStatus("SQL-Editor nicht gefunden.");
      return;
    }

    this.bindModuleSwitcher();

    this.actionLinks.forEach((button) => {
      button.addEventListener("click", (event) => this.onAction(event, button));
    });

    this.assistantActionLinks.forEach((button) => {
      button.addEventListener("click", (event) => this.onAssistantAction(event, button));
    });

    this.editor.addEventListener("input", () => {
      const task = this.getCurrentTask();
      if (task && this.store) {
        this.store.saveSqlDraft(task.id, this.editor.value);
      }
    });

    this.exportButton?.addEventListener("click", () => this.exportState());

    this.activateInitialTabs();

    const initialHref = normalizeHref(this.view.moduleSelect?.value || this.resolveDefaultModuleHref());
    if (!initialHref) {
      this.view.setFooterStatus("Kein SQL-Modul gefunden.");
      return;
    }

    await this.loadModule(initialHref, { resetToFirstTask: true });
  }

  resolveDefaultModuleHref() {
    const direct = this.exerciseLinks.find((entry) => String(entry?.href || "").includes(MODULE_CONFIGS[0].slug));
    if (direct?.href) {
      return String(direct.href);
    }

    const fallback = this.exerciseLinks[0];
    return fallback?.href ? String(fallback.href) : "";
  }

  bindModuleSwitcher() {
    if (!this.view.moduleSelect || !this.view.moduleOpenLink) {
      return;
    }

    const syncSelectedModuleLink = () => {
      const selectedHref = normalizeHref(this.view.moduleSelect.value);
      if (!selectedHref) {
        return;
      }
      this.view.moduleOpenLink.href = selectedHref;
    };

    syncSelectedModuleLink();

    this.view.moduleSelect.addEventListener("change", async (event) => {
      syncSelectedModuleLink();

      const selectedHref = normalizeHref(event.target?.value);
      if (!selectedHref) {
        return;
      }

      await this.loadModule(selectedHref, { resetToFirstTask: true });
    });
  }

  async loadModule(moduleHref, options = {}) {
    const { resetToFirstTask = false } = options;
    const normalizedHref = normalizeHref(moduleHref);
    if (!normalizedHref || this.loadingModule) {
      return;
    }

    this.loadingModule = true;
    this.view.setFooterStatus("Modul wird geladen...");

    try {
      const payload = await this.repository.load(normalizedHref);
      this.tasks = payload.tasks;
      this.info = payload.info;
      this.moduleHref = normalizedHref;
      this.moduleConfig = configForHref(normalizedHref);

      if (this.tasks.length === 0) {
        this.view.setFooterStatus("Keine Aufgaben im gewaehlten Modul erkannt.");
        return;
      }

      this.store = new SqlLearningStateStore(this.tasks.length, this.moduleConfig.storageKey);
      if (resetToFirstTask) {
        this.store.resetToStart();
      }

      this.view.renderModeler(this.moduleConfig.eermImage, this.moduleConfig.eermAlt);
      this.renderCurrentTask({ resetAssistant: true, resetResult: true });
      this.view.setFooterStatus(`Modul geladen: ${this.moduleConfig.moduleTitle}. Aufgabe 1-14 jetzt linear bearbeiten.`);
    } catch (error) {
      this.view.setFooterStatus(`Modulstart fehlgeschlagen: ${sanitizeStudentFacingMessage(error?.message || "Unbekannter Fehler")}`);
    } finally {
      this.loadingModule = false;
    }
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

  renderCurrentTask(options = {}) {
    const { resetAssistant = false, resetResult = false } = options;
    const task = this.getCurrentTask();
    if (!task || !this.store) {
      return;
    }

    const attempts = this.store.attemptsFor(task.id);
    const solved = this.store.isSolved(task.id);

    this.view.renderTask(task, this.tasks.length, attempts, solved, this.moduleHref);
    this.view.renderInfo(task, this.info || { schemaItems: [], tips: [], links: [], clauseOrder: "" });

    if (this.editor) {
      this.editor.value = this.store.loadSqlDraft(task.id);
    }

    if (resetResult) {
      this.view.clearResult();
      this.view.renderLog("Noch kein Test gestartet.", "Tippe eine Abfrage ein und starte den Test.", "warning");
    }

    if (resetAssistant) {
      this.view.resetAssistantPanels();
    }

    this.updateExportPreview();
  }

  refreshTaskHeaderOnly() {
    const task = this.getCurrentTask();
    if (!task || !this.store) {
      return;
    }

    const attempts = this.store.attemptsFor(task.id);
    const solved = this.store.isSolved(task.id);
    this.view.renderTask(task, this.tasks.length, attempts, solved, this.moduleHref);
  }

  onAction(event, button) {
    event.preventDefault();
    const action = String(button.dataset.courseAction || "").trim();

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

    if (action === "hint") {
      const task = this.getCurrentTask();
      if (!task) {
        return;
      }
      this.view.toggleHint(task.hintHtml);
      this.view.setFooterStatus(`Lernhilfe fuer Aufgabe ${task.number} aktualisiert.`);
      return;
    }

    if (action === "test") {
      this.runTest();
    }
  }

  onAssistantAction(event, button) {
    event.preventDefault();
    const action = String(button.dataset.assistantAction || "").trim();
    const task = this.getCurrentTask();
    if (!task) {
      return;
    }

    if (action === "solution") {
      this.view.toggleSolution(task.solutionSql);
      this.view.setFooterStatus(`Musterloesung fuer Aufgabe ${task.number} umgeschaltet.`);
      return;
    }

    if (action === "expected") {
      this.view.toggleExpected(task.expectedResultHtml);
      this.view.setFooterStatus(`Erwartetes Ergebnis fuer Aufgabe ${task.number} umgeschaltet.`);
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
      this.view.setFooterStatus("Bitte loese zuerst die aktuelle Aufgabe erfolgreich und klicke danach auf Naechster Schritt.");
      return;
    }

    this.store.setCurrentTaskIndex(next);
    this.renderCurrentTask({ resetAssistant: true, resetResult: true });
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

    const sqlText = String(this.editor?.value || "").trim();
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
        dataset_key: this.moduleConfig.datasetKey,
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
            ? "Klicke auf Naechster Schritt, um die naechste Aufgabe zu laden."
            : "Alle Aufgaben bearbeitet. Klicke auf Naechster Schritt fuer die Abschlussauswertung.",
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

    this.refreshTaskHeaderOnly();
    this.updateExportPreview();
  }

  parseSqlError(rawMessage) {
    const message = sanitizeStudentFacingMessage(rawMessage) || "SQL-Test fehlgeschlagen.";
    const lineMatch = message.match(/line\s+(\d+)/i);
    const lineText = lineMatch ? `Zeile ${lineMatch[1]}` : "Zeile unbekannt";

    let hint = "Pruefe Klauselreihenfolge, Aliasnamen und Klammern.";
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
      moduleTitle: this.moduleConfig.moduleTitle,
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
    link.download = "rdb-modul-progress.json";
    link.click();
    URL.revokeObjectURL(url);
    this.view.setFooterStatus("Arbeitsstand exportiert: rdb-modul-progress.json");
  }
}

export function initCourseWorkflowController() {
  const content = window.LEARNING_CONTENT || {};
  const exerciseLinks = Array.isArray(content.exerciseLinks) ? content.exerciseLinks : [];

  new CourseWorkflowController({
    exerciseLinks,
    actionLinks: Array.from(document.querySelectorAll("[data-course-action]")),
    assistantActionLinks: Array.from(document.querySelectorAll("[data-assistant-action]")),
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
      taskHintPanel: document.getElementById("currentTaskHintPanel"),
      taskHint: document.getElementById("currentTaskHint"),
      taskLink: document.getElementById("currentTaskLink"),
      moduleSelect: document.getElementById("moduleSelect"),
      moduleOpenLink: document.getElementById("moduleOpenLink"),
      modulePosition: document.getElementById("currentModulePosition"),
      infoText: document.getElementById("currentInfoText"),
      infoContent: document.getElementById("currentInfoContent"),
      footerStatus: document.getElementById("workflowStatus"),
      editor: document.getElementById("practiceEditor-0"),
      editorHeading: document.getElementById("currentSqlEditorHeading"),
      editorLabel: document.getElementById("currentSqlDraftLabel"),
      logBox: document.getElementById("sqlTestLogBox"),
      logText: document.getElementById("sqlTestLog"),
      logHint: document.getElementById("sqlTestHint"),
      resultGrid: document.getElementById("sqlResultGrid"),
      modelerCanvas: document.getElementById("modelerCanvas"),
      assistantHintBox: document.getElementById("assistantHintBox"),
      assistantHintText: document.getElementById("assistantHintText"),
      assistantSolutionBox: document.getElementById("assistantSolutionBox"),
      assistantSolutionSql: document.getElementById("assistantSolutionSql"),
      assistantExpectedBox: document.getElementById("assistantExpectedBox"),
      assistantExpectedContent: document.getElementById("assistantExpectedContent"),
    },
  }).bind();
}
