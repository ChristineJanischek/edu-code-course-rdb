const PAGE_MATCHERS = [
  /\/generated\/uebungen\/UE\d+_.*_sql_abfragen\.html$/i,
  /\/generated\/klassenarbeiten\/KA\d+_.*_aufg\.html$/i,
];

const STORAGE_PREFIX = "sql-practice";
const SQL_API_BASE_URL = window.SUBMISSION_API_BASE_URL || window.PYTHON_API_URL || "/api-proxy.php";

const CLAUSE_PATTERNS = [
  { key: "SELECT", regex: /\bSELECT\b/i, label: "SELECT" },
  { key: "FROM", regex: /\bFROM\b/i, label: "FROM" },
  { key: "LEFT JOIN", regex: /\bLEFT\s+JOIN\b/i, label: "LEFT JOIN" },
  { key: "JOIN", regex: /\bJOIN\b/i, label: "JOIN" },
  { key: "WHERE", regex: /\bWHERE\b/i, label: "WHERE" },
  { key: "GROUP BY", regex: /\bGROUP\s+BY\b/i, label: "GROUP BY" },
  { key: "HAVING", regex: /\bHAVING\b/i, label: "HAVING" },
  { key: "ORDER BY", regex: /\bORDER\s+BY\b/i, label: "ORDER BY" },
];

function shouldEnhancePage() {
  return PAGE_MATCHERS.some((matcher) => matcher.test(window.location.pathname));
}

function normalizeSql(sql) {
  return String(sql || "")
    .replace(/--.*$/gm, "")
    .replace(/\/\*[\s\S]*?\*\//g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function toUpperNormalized(sql) {
  return normalizeSql(sql).toUpperCase();
}

function extractTableNames(sql) {
  const tables = [];
  const matcher = /\b(?:FROM|JOIN)\s+([`"']?[A-Za-z_][A-Za-z0-9_]*[`"']?)/gi;
  let match;

  while ((match = matcher.exec(sql)) !== null) {
    const raw = String(match[1] || "").replace(/[`"']/g, "").toLowerCase();
    if (!raw) {
      continue;
    }
    if (!tables.includes(raw)) {
      tables.push(raw);
    }
  }

  return tables;
}

function inferRequiredClauses(solutionSql) {
  const clauses = [];
  for (const candidate of CLAUSE_PATTERNS) {
    if (candidate.regex.test(solutionSql)) {
      clauses.push(candidate.label);
    }
  }
  return clauses;
}

function buildCoachSteps(solutionSql, solutionTables) {
  const steps = [
    "Lies zuerst die Aufgabe: Welche Spalten sollen in der Ausgabe stehen?",
    "Starte mit SELECT und waehle nur die benoetigten Ausgabespalten.",
  ];

  if (solutionTables.length > 0) {
    steps.push(`Setze die Basistabelle in FROM (${solutionTables[0]}).`);
  }

  for (let i = 1; i < solutionTables.length; i += 1) {
    steps.push(`Fuege JOIN fuer ${solutionTables[i]} ueber den passenden PK/FK-Pfad hinzu.`);
  }

  if (/\bWHERE\b/i.test(solutionSql)) {
    steps.push("Ergaenze danach WHERE-Filter fuer fachlich korrekte Zeilen.");
  }
  if (/\bGROUP\s+BY\b/i.test(solutionSql)) {
    steps.push("Baue GROUP BY nur fuer Spalten, die nicht aggregiert sind.");
  }
  if (/\bHAVING\b/i.test(solutionSql)) {
    steps.push("Nutze HAVING fuer Bedingungen auf Gruppenergebnisse.");
  }
  if (/\bORDER\s+BY\b/i.test(solutionSql)) {
    steps.push("Setze ORDER BY am Ende fuer die geforderte Sortierung.");
  }

  steps.push("Teste danach die Lesbarkeit: kurze Aliase, klare Reihenfolge, saubere Einrueckung.");
  return steps;
}

function evaluateAttempt(inputSql, blueprint) {
  const cleaned = toUpperNormalized(inputSql);
  if (!cleaned) {
    return {
      state: "warning",
      score: 0,
      checks: [],
      message: "Noch keine Abfrage eingetragen. Starte mit SELECT ... FROM ...",
      missingSteps: blueprint.steps,
    };
  }

  const checks = [];
  const requiredClauses = blueprint.requiredClauses;
  const requiredTables = blueprint.requiredTables;

  checks.push({
    ok: /\bSELECT\b/.test(cleaned),
    label: "SELECT vorhanden",
    hint: "Jede Loesung startet mit SELECT.",
  });
  checks.push({
    ok: /\bFROM\b/.test(cleaned),
    label: "FROM vorhanden",
    hint: "Lege die Basistabelle in FROM fest.",
  });

  for (const table of requiredTables) {
    const tablePattern = new RegExp(`\\b${table.toUpperCase()}\\b`, "i");
    checks.push({
      ok: tablePattern.test(cleaned),
      label: `Tabelle ${table}`,
      hint: `Pruefe, ob ${table} in FROM/JOIN enthalten ist.`,
    });
  }

  for (const clause of requiredClauses) {
    if (clause === "SELECT" || clause === "FROM") {
      continue;
    }
    const clausePattern = new RegExp(`\\b${clause.replace(/\s+/g, "\\s+")}\\b`, "i");
    checks.push({
      ok: clausePattern.test(cleaned),
      label: `${clause} verwendet`,
      hint: `${clause} fehlt oder ist anders aufgebaut als im Erwartungsmuster.`,
    });
  }

  const okCount = checks.filter((item) => item.ok).length;
  const score = checks.length > 0 ? Math.round((okCount / checks.length) * 100) : 0;
  const missing = checks.filter((item) => !item.ok).map((item) => item.hint);

  return {
    state: score >= 85 ? "success" : "warning",
    score,
    checks,
    message:
      score >= 85
        ? `Stark! Die Abfrage trifft das Erwartungsmuster zu ${score}%.`
        : `Zwischenstand: ${score}%. Arbeite die offenen Punkte Schritt fuer Schritt nach.`,
    missingSteps: missing,
  };
}

function injectStylesOnce() {
  if (document.getElementById("sql-practice-runtime-style")) {
    return;
  }

  const style = document.createElement("style");
  style.id = "sql-practice-runtime-style";
  style.textContent = `
  .sql-practice-box { margin-top: 10px; border: 1px solid #d7e2ec; border-radius: 10px; padding: 10px; background: #fbfdff; }
  .sql-practice-box .sql-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .sql-practice-box button { border: 0; border-radius: 8px; padding: 7px 12px; cursor: pointer; font-weight: 600; }
  .sql-practice-box .btn-test { background: #e7f5ef; color: #0a7d5c; }
  .sql-practice-box .btn-step { background: #e9f0fb; color: #0b5fa5; }
  .sql-practice-box .btn-info { background: #fff6db; color: #915e00; }
  .sql-practice-box .coach-output { margin-top: 10px; font-size: 0.9rem; color: #24384b; }
  .sql-practice-box .coach-output ul { margin: 6px 0 0 18px; }
  .sql-practice-box .coach-output li.ok { color: #0a7d5c; }
  .sql-practice-box .coach-output li.miss { color: #8d1b2a; }
  .sql-practice-box .coach-state-success { border-left: 4px solid #0a7d5c; padding-left: 8px; }
  .sql-practice-box .coach-state-warning { border-left: 4px solid #b8860b; padding-left: 8px; }
  .sql-practice-box .result-grid { display: grid; grid-template-columns: 1fr; gap: 10px; margin-top: 10px; }
  .sql-practice-box .result-card { border: 1px solid #d7e2ec; border-radius: 8px; padding: 8px; background: #fff; }
  .sql-practice-box .result-card h5 { margin: 0 0 6px; font-size: 0.86rem; color: #28425b; }
  .sql-practice-box .result-card table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  .sql-practice-box .result-card th, .sql-practice-box .result-card td { border: 1px solid #d7e2ec; padding: 4px 6px; text-align: left; }
  .sql-practice-box .result-card th { background: #eef5ff; }
  .sql-practice-box .result-note { font-size: 0.8rem; color: #52667a; margin-top: 4px; }
  `;
  document.head.appendChild(style);
}

function createCoachBox(cardId) {
  const wrapper = document.createElement("div");
  wrapper.className = "sql-practice-box";
  wrapper.dataset.cardId = cardId;

  wrapper.innerHTML = `
    <strong>SQL-Assistent</strong>
    <div class="sql-actions">
      <button type="button" class="btn-test">Abfrage testen (Ergebnis)</button>
      <button type="button" class="btn-step">Naechster Schritt</button>
      <button type="button" class="btn-info">i Lernhilfe</button>
    </div>
    <div class="coach-output" aria-live="polite">Tippe eine Abfrage ein und starte den Test.</div>
  `;

  return wrapper;
}

function storageKey(cardId) {
  return `${STORAGE_PREFIX}:${window.location.pathname}:${cardId}`;
}

function pageDatasetKey() {
  const path = window.location.pathname.toLowerCase();
  if (path.includes("ue01_foodtrucknetz")) {
    return "foodtrucknetz_uebung";
  }
  if (path.includes("ue02_stadtfahrradverleih")) {
    return "stadtfahrradverleih_uebung";
  }
  if (path.includes("ka02") && path.includes("version1")) {
    return "stadtfahrradverleih_ka";
  }
  if (path.includes("ka02") && path.includes("version2")) {
    return "coworkingcampus_ka";
  }
  if (path.includes("ka02") && path.includes("version3")) {
    return "foodtrucknetz_ka";
  }
  return "stadtfahrradverleih_uebung";
}

async function executeSqlAgainstSandbox(datasetKey, candidateSql, referenceSql) {
  const response = await fetch(`${SQL_API_BASE_URL}/api/v1/sql-sandbox/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dataset_key: datasetKey,
      candidate_sql: candidateSql,
      reference_sql: referenceSql,
    }),
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload?.success === false) {
    const message = payload?.error?.message || payload?.error || "SQL-Sandbox momentan nicht erreichbar.";
    throw new Error(message);
  }

  return payload?.data || payload;
}

function renderResultTable(title, dataset) {
  const columns = Array.isArray(dataset?.columns) ? dataset.columns : [];
  const rows = Array.isArray(dataset?.rows) ? dataset.rows.slice(0, 12) : [];

  if (columns.length === 0) {
    return `
      <div class="result-card">
        <h5>${title}</h5>
        <p class="result-note">Keine auswertbaren Spalten vorhanden.</p>
      </div>
    `;
  }

  const header = columns.map((name) => `<th>${name}</th>`).join("");
  const body = rows
    .map((row) => `<tr>${columns.map((_, index) => `<td>${row?.[index] ?? ""}</td>`).join("")}</tr>`)
    .join("");

  return `
    <div class="result-card">
      <h5>${title}</h5>
      <table>
        <thead><tr>${header}</tr></thead>
        <tbody>${body}</tbody>
      </table>
      <p class="result-note">Zeilen: ${dataset?.row_count ?? rows.length}${(dataset?.row_count || 0) > rows.length ? ` (Anzeige gekuerzt auf ${rows.length})` : ""}</p>
    </div>
  `;
}

function bindCoach(card, blueprint) {
  const textarea = card.querySelector("textarea.sql-input");
  if (!textarea) {
    return;
  }

  const cardId = card.id || `card-${Math.random().toString(36).slice(2, 9)}`;
  const coach = createCoachBox(cardId);
  textarea.insertAdjacentElement("afterend", coach);

  const testButton = coach.querySelector(".btn-test");
  const stepButton = coach.querySelector(".btn-step");
  const infoButton = coach.querySelector(".btn-info");
  const output = coach.querySelector(".coach-output");
  const datasetKey = pageDatasetKey();

  let stepIndex = 0;

  const saved = window.localStorage.getItem(storageKey(cardId));
  if (saved) {
    textarea.value = saved;
  }

  textarea.addEventListener("input", () => {
    window.localStorage.setItem(storageKey(cardId), textarea.value);
  });

  textarea.addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key === "Enter") {
      event.preventDefault();
      testButton?.click();
    }
  });

  testButton?.addEventListener("click", () => {
    const candidateSql = textarea.value;
    if (!candidateSql.trim()) {
      output.textContent = "Bitte zuerst eine SQL-Abfrage eingeben.";
      return;
    }

    const result = evaluateAttempt(textarea.value, blueprint);
    const stateClass = result.state === "success" ? "coach-state-success" : "coach-state-warning";

    const checks = result.checks
      .map((item) => `<li class="${item.ok ? "ok" : "miss"}">${item.ok ? "OK" : "Offen"}: ${item.label}</li>`)
      .join("");

    output.innerHTML = `
      <div class="${stateClass}"><strong>${result.message}</strong></div>
      <ul>${checks}</ul>
      <p class="result-note">Pruefe jetzt mit der Sandbox den echten Ergebnissatz ...</p>
    `;

    executeSqlAgainstSandbox(datasetKey, candidateSql, blueprint.solutionSql)
      .then((sandboxResult) => {
        const quality = sandboxResult?.ok ? "coach-state-success" : "coach-state-warning";
        const feedback = sandboxResult?.feedback || {};

        output.innerHTML += `
          <div class="${quality}" style="margin-top:8px;"><strong>Sandbox:</strong> ${feedback.message || "Vergleich abgeschlossen."} (Score: ${sandboxResult?.score ?? 0}%)</div>
          <div class="result-grid">
            ${renderResultTable("Dein Ergebnissatz", sandboxResult?.actual)}
            ${renderResultTable("Referenz-Ergebnissatz", sandboxResult?.expected)}
          </div>
          ${Array.isArray(feedback.missing_samples) && feedback.missing_samples.length > 0 ? `<p class="result-note">Fehlende Beispielzeilen: ${feedback.missing_samples.join(" | ")}</p>` : ""}
          ${Array.isArray(feedback.extra_samples) && feedback.extra_samples.length > 0 ? `<p class="result-note">Zusatzzeilen: ${feedback.extra_samples.join(" | ")}</p>` : ""}
        `;
      })
      .catch((error) => {
        output.innerHTML += `<p class="result-note">Sandbox-Hinweis: ${error.message}</p>`;
      });
  });

  stepButton?.addEventListener("click", () => {
    if (stepIndex >= blueprint.steps.length) {
      stepIndex = 0;
    }

    output.textContent = `Schritt ${stepIndex + 1}/${blueprint.steps.length}: ${blueprint.steps[stepIndex]}`;
    stepIndex += 1;
  });

  infoButton?.addEventListener("click", () => {
    const tips = [
      "Arbeite immer in der Reihenfolge SELECT -> FROM/JOIN -> WHERE -> GROUP BY/HAVING -> ORDER BY.",
      "Verbinde Tabellen nur ueber fachlich passende PK/FK-Beziehungen.",
      "Nutze sprechende Aliase, wenn Tabellen mehrfach vorkommen.",
      "Bei GROUP BY duerfen nicht aggregierte Ausgabespalten nicht vergessen werden.",
    ];
    output.innerHTML = `<strong>Didaktische Kurzinfo</strong><ul>${tips.map((tip) => `<li>${tip}</li>`).join("")}</ul>`;
  });
}

function buildBlueprintFromCard(card) {
  const solutionSql = String(card.querySelector(".sol-box pre")?.textContent || "").trim();
  const requiredTables = extractTableNames(solutionSql);
  const requiredClauses = inferRequiredClauses(solutionSql);

  return {
    solutionSql,
    requiredTables,
    requiredClauses,
    steps: buildCoachSteps(solutionSql, requiredTables),
  };
}

function enhanceExerciseCards() {
  const cards = Array.from(document.querySelectorAll(".card.exercise"));
  if (cards.length === 0) {
    return 0;
  }

  for (const card of cards) {
    if (!card.querySelector("textarea.sql-input") || card.querySelector(".sql-practice-box")) {
      continue;
    }
    const blueprint = buildBlueprintFromCard(card);
    bindCoach(card, blueprint);
  }

  return cards.length;
}

async function loadKaSolutions() {
  const solutionUrl = window.location.pathname.replace(/_aufg\.html$/i, "_lsg.html");
  if (solutionUrl === window.location.pathname) {
    return new Map();
  }

  try {
    const response = await fetch(solutionUrl, { credentials: "same-origin" });
    if (!response.ok) {
      return new Map();
    }

    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, "text/html");
    const map = new Map();
    const headings = Array.from(doc.querySelectorAll("h3"));

    for (const heading of headings) {
      const label = heading.textContent?.trim() || "";
      if (!/^Aufgabe\s+4\./i.test(label)) {
        continue;
      }

      let cursor = heading.nextElementSibling;
      while (cursor && cursor.tagName.toLowerCase() !== "h3") {
        const pre = cursor.querySelector("pre");
        if (pre && pre.textContent?.includes("SELECT")) {
          map.set(label, pre.textContent.trim());
          break;
        }
        cursor = cursor.nextElementSibling;
      }
    }

    return map;
  } catch {
    return new Map();
  }
}

async function enhanceKaPartC() {
  if (!/\/generated\/klassenarbeiten\/KA\d+_.*_aufg\.html$/i.test(window.location.pathname)) {
    return 0;
  }

  const h3Nodes = Array.from(document.querySelectorAll("h3"));
  const taskHeadings = h3Nodes.filter((node) => /^Aufgabe\s+4\./i.test(node.textContent || ""));
  if (taskHeadings.length === 0) {
    return 0;
  }

  const solutionMap = await loadKaSolutions();
  let count = 0;

  for (const heading of taskHeadings) {
    if (heading.nextElementSibling?.classList?.contains("sql-practice-box")) {
      continue;
    }

    const label = heading.textContent?.trim() || "Aufgabe 4";
    const textarea = document.createElement("textarea");
    textarea.className = "sql-input";
    textarea.placeholder = "SELECT ...\nFROM ...\nJOIN ...\nWHERE ...";
    textarea.setAttribute("aria-label", `${label}: SQL-Eingabe`);

    const shell = document.createElement("div");
    shell.className = "card exercise";
    shell.id = `coach-${label.replace(/[^\w]+/g, "-").toLowerCase()}`;

    const solutionSql = solutionMap.get(label) || "SELECT ... FROM ...";
    const blueprint = {
      solutionSql,
      requiredTables: extractTableNames(solutionSql),
      requiredClauses: inferRequiredClauses(solutionSql),
      steps: buildCoachSteps(solutionSql, extractTableNames(solutionSql)),
    };

    const title = document.createElement("p");
    title.className = "sql-label";
    title.textContent = `${label}: SQL in die Box eingeben und testen`;

    shell.appendChild(title);
    shell.appendChild(textarea);
    heading.insertAdjacentElement("afterend", shell);
    bindCoach(shell, blueprint);
    count += 1;
  }

  return count;
}

function patchLegacyToggle() {
  if (typeof window.toggle === "function") {
    return;
  }

  window.toggle = (id) => {
    const element = document.getElementById(id);
    if (!element) {
      return;
    }
    element.classList.toggle("hidden");
  };
}

async function init() {
  if (!shouldEnhancePage()) {
    return;
  }

  injectStylesOnce();
  patchLegacyToggle();
  const enhancedCards = enhanceExerciseCards();
  const enhancedKa = await enhanceKaPartC();

  if (enhancedCards === 0 && enhancedKa === 0) {
    return;
  }

  console.info(`[sql-practice] Aktiv: ${enhancedCards + enhancedKa} Aufgabenbereiche erweitert.`);
}

init();
