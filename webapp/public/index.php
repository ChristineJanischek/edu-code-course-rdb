<?php
declare(strict_types=1);

require_once __DIR__ . '/../app/Repository/LearningContentRepository.php';
require_once __DIR__ . '/../app/Controller/StudentPortalController.php';

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'");

$pythonApiUrl = getenv('PYTHON_API_URL') ?: '/api-proxy.php';
$submissionApiBaseUrl = '/api-proxy.php';

$contentRepository = new LearningContentRepository(__DIR__ . '/data/learning-content.json');
$studentPortalController = new StudentPortalController($contentRepository, __DIR__ . '/generated');
$viewModel = $studentPortalController->buildViewModel();

/**
 * Remove internal governance markers from all student-facing strings.
 * This keeps the portal focused on learner content only.
 */
function sanitizeStudentText(string $text): string
{
  $text = preg_replace('/^\s*#{1,6}\s*CTX-GOV\b.*$/im', '', $text) ?? $text;
  $text = preg_replace('/^\s*CTX-GOV\s*:\s*.*$/im', '', $text) ?? $text;
  $text = preg_replace('/\bCTX-GOV\b[^\r\n]*/i', '', $text) ?? $text;
  $text = preg_replace('/\n{3,}/', "\n\n", $text) ?? $text;

  return trim($text);
}

function sanitizeStudentValue(mixed $value): mixed
{
  if (is_string($value)) {
    return sanitizeStudentText($value);
  }

  if (!is_array($value)) {
    return $value;
  }

  $sanitized = [];
  foreach ($value as $key => $child) {
    $sanitized[$key] = sanitizeStudentValue($child);
  }

  return $sanitized;
}

function hasCtxGovMarker(mixed $value): bool
{
  if (is_string($value)) {
    return (bool) preg_match('/\bCTX-GOV\b/i', $value);
  }

  if (!is_array($value)) {
    return false;
  }

  foreach ($value as $child) {
    if (hasCtxGovMarker($child)) {
      return true;
    }
  }

  return false;
}

$viewModel = sanitizeStudentValue($viewModel);

$learningPaths = $viewModel['learningPaths'];
$curriculumTopics = $viewModel['curriculumTopics'];
$learningPlanLinks = $viewModel['learningPlanLinks'];
$exerciseLinks = $viewModel['exerciseLinks'];
$indexLinks = $viewModel['indexLinks'];
$catalogMeta = $viewModel['catalogMeta'];

$learningPaths = array_values(array_filter($learningPaths, static fn ($item): bool => !hasCtxGovMarker($item)));
$curriculumTopics = array_values(array_filter($curriculumTopics, static fn ($item): bool => !hasCtxGovMarker($item)));
$learningPlanLinks = array_values(array_filter($learningPlanLinks, static fn ($item): bool => !hasCtxGovMarker($item)));
$exerciseLinks = array_values(array_filter($exerciseLinks, static fn ($item): bool => !hasCtxGovMarker($item)));
$indexLinks = array_values(array_filter($indexLinks, static fn ($item): bool => !hasCtxGovMarker($item)));

$viewModel['learningPaths'] = $learningPaths;
$viewModel['curriculumTopics'] = $curriculumTopics;
$viewModel['learningPlanLinks'] = $learningPlanLinks;
$viewModel['exerciseLinks'] = $exerciseLinks;
$viewModel['indexLinks'] = $indexLinks;
?>
<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>eLearning RDB Portal</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="app-shell">
      <header class="app-header">
        <div class="hero-surface">
          <p class="eyebrow">Schülerportal</p>
          <h1>Relationale Datenbanken: Lernpfade, Übungen und Abgaben</h1>
          <p class="hero-text">Fokussiert auf die für dich relevanten Bausteine: Themen nach Lehrplan, Stoffverlaufsplan, Übungen mit Lösungen, Stichwortindex und Upload für Schülerlösungen.</p>
        </div>

        <nav id="primaryNav" class="primary-nav" aria-label="Hauptnavigation">
          <a href="#panel-learning">Reiter 1: Information</a>
          <a href="#panel-practice">Reiter 2: Editor und Assistent</a>
          <a href="#files-panel">Dateien</a>
          <a href="#submission-section">Upload</a>
        </nav>
      </header>

      <main class="page">
        <div class="content-layout">
          <aside class="course-nav" aria-label="Kursnavigation">
            <div class="card sticky-card">
              <h2>Kursnavigation</h2>
              <ul>
                <li><a href="#panel-learning">Reiter 1: Information, Aufgaben, Suche</a></li>
                <li><a href="#panel-practice">Reiter 2: Praktische Umsetzung</a></li>
                <li><a href="#assistant-section">Assistenz Weiter/Check</a></li>
                <li><a href="#files-panel">Dateien bearbeiten</a></li>
                <li><a href="#submission-section">Upload</a></li>
              </ul>
              <h3>Direkt zu den Quellen</h3>
              <ul>
                <li><a href="/generated/anleitungen/stoffverlaufsplan_rdb_3wochen.html" target="_blank" rel="noopener">Stoffverlaufsplan</a></li>
                <li><a href="/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html" target="_blank" rel="noopener">Stichwortverzeichnis</a></li>
                <li><a href="/generated/uebungen/README.md" target="_blank" rel="noopener">Übungsübersicht</a></li>
              </ul>
              <p class="muted">Verstehenslinie: verstehen → modellieren → normalisieren → anwenden → reflektieren.</p>
            </div>
          </aside>

          <div class="content-column">
            <section class="card workspace-switcher" aria-label="Arbeitsbereiche">
              <p class="eyebrow">Arbeitsmodus</p>
              <h2>2-Reiter-Ansicht für Lernen und praktische Umsetzung</h2>
              <div class="tab-toolbar" role="tablist" aria-label="Hauptreiter" data-tab-group="workspace-main">
                <button type="button" role="tab" id="tab-learning" aria-controls="panel-learning" aria-selected="true" data-tab-target="panel-learning" class="tab-button is-active">1. Reiter: Information und Aufgaben</button>
                <button type="button" role="tab" id="tab-practice" aria-controls="panel-practice" aria-selected="false" data-tab-target="panel-practice" class="tab-button">2. Reiter: Editor und Assistenz</button>
              </div>
            </section>

            <section class="workspace-panel is-active" id="panel-learning" role="tabpanel" aria-labelledby="tab-learning">
              <section class="card intro-card">
                <div class="split-grid">
                  <div>
                    <p class="eyebrow">Reiter 1</p>
                    <h2>Information, Aufgabenstellung und Stichwortsuche</h2>
                    <p>Dieser Bereich ist für den schnellen Überblick und die fachliche Orientierung optimiert. Lernende und Lehrkräfte finden hier Themen, Aufgaben und den Suchindex ohne Ablenkung.</p>
                  </div>
                  <div>
                    <h3>Didaktische Leitlinie</h3>
                    <ul class="check-list">
                      <li>Zuerst verstehen, dann anwenden</li>
                      <li>Klare Aufgabenkontexte und Lernziele</li>
                      <li>Stichwortzugriff für präzises Nachschlagen</li>
                      <li>Barrierearme, mobilfreundliche Darstellung</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section class="section-block" id="learning-paths-section">
                <div class="section-head">
                  <p class="eyebrow">Lernpfade</p>
                  <h2>Themen laut Lehrplan und Stoffverlaufsplan</h2>
                </div>

                <div class="card-grid">
                  <?php foreach ($curriculumTopics as $topic): ?>
                    <article class="card">
                      <h3><?php echo htmlspecialchars(($topic['code'] ?? '') . ': ' . ($topic['title'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></h3>
                      <p><?php echo htmlspecialchars($topic['description'] ?? '', ENT_QUOTES, 'UTF-8'); ?></p>
                      <p class="muted">Zeithorizont: <?php echo htmlspecialchars($topic['time_horizon'] ?? '-', ENT_QUOTES, 'UTF-8'); ?></p>
                    </article>
                  <?php endforeach; ?>
                </div>

                <div class="card-grid compact">
                  <?php foreach ($learningPlanLinks as $item): ?>
                    <article class="card link-card">
                      <h3><?php echo htmlspecialchars($item['title'], ENT_QUOTES, 'UTF-8'); ?></h3>
                      <p><?php echo htmlspecialchars($item['description'], ENT_QUOTES, 'UTF-8'); ?></p>
                      <a class="action-link" href="<?php echo htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener">Öffnen</a>
                    </article>
                  <?php endforeach; ?>
                </div>

                <?php if (!empty($learningPaths)): ?>
                  <div class="card-grid compact">
                    <?php foreach ($learningPaths as $path): ?>
                      <article class="card">
                        <h3><?php echo htmlspecialchars($path['title'] ?? '', ENT_QUOTES, 'UTF-8'); ?></h3>
                        <p class="muted"><?php echo htmlspecialchars($path['focus'] ?? '', ENT_QUOTES, 'UTF-8'); ?></p>
                        <ol>
                          <?php foreach (($path['steps'] ?? []) as $step): ?>
                            <li><?php echo htmlspecialchars((string) $step, ENT_QUOTES, 'UTF-8'); ?></li>
                          <?php endforeach; ?>
                        </ol>
                      </article>
                    <?php endforeach; ?>
                  </div>
                <?php endif; ?>
              </section>

              <section class="section-block" id="exercise-section">
                <div class="section-head">
                  <p class="eyebrow">Aufgabenstellung</p>
                  <h2>Übungen und Lösungen</h2>
                </div>
                <div class="card-grid compact">
                  <?php foreach ($exerciseLinks as $item): ?>
                    <article class="card link-card">
                      <h3><?php echo htmlspecialchars($item['title'], ENT_QUOTES, 'UTF-8'); ?></h3>
                      <p><?php echo htmlspecialchars($item['description'], ENT_QUOTES, 'UTF-8'); ?></p>
                      <a class="action-link" href="<?php echo htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener">Öffnen</a>
                    </article>
                  <?php endforeach; ?>
                </div>
              </section>

              <section class="section-block" id="index-section">
                <div class="section-head">
                  <p class="eyebrow">Stichwortsuche</p>
                  <h2>Index für Modellierung, Normalisierung und SQL</h2>
                </div>

                <article class="card">
                  <label for="keywordSearch" class="field-label">Suchbegriff</label>
                  <input id="keywordSearch" class="keyword-search" type="search" placeholder="z. B. 3NF, Kardinalität, JOIN" autocomplete="off" />
                  <ul id="keywordList" class="keyword-list">
                    <?php foreach ($indexLinks as $item): ?>
                      <li data-topic="<?php echo htmlspecialchars(strtolower($item['topic']), ENT_QUOTES, 'UTF-8'); ?>" data-title="<?php echo htmlspecialchars(strtolower($item['title']), ENT_QUOTES, 'UTF-8'); ?>">
                        <span class="topic-pill"><?php echo htmlspecialchars($item['topic'], ENT_QUOTES, 'UTF-8'); ?></span>
                        <a href="<?php echo htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener"><?php echo htmlspecialchars($item['title'], ENT_QUOTES, 'UTF-8'); ?></a>
                      </li>
                    <?php endforeach; ?>
                  </ul>
                </article>
              </section>
            </section>

            <section class="workspace-panel" id="panel-practice" role="tabpanel" aria-labelledby="tab-practice" hidden>
              <section class="card">
                <div class="section-head">
                  <p class="eyebrow">Reiter 2</p>
                  <h2>Editor, Assistenz und Selbstkontrolle</h2>
                </div>
                <p class="muted">Hier wird praktisch gearbeitet: Entwurf im Editor, Assistenz über Weiter- und Check-Funktion, Dateiüberblick und anschließender Upload.</p>
              </section>

              <section class="practice-layout">
                <div class="practice-main">
                  <section class="section-block" id="editor-section">
                    <article class="card editor-card">
                      <h3>Praktischer Editor</h3>
                      <label for="practiceFileName" class="field-label">Arbeitsdatei</label>
                      <input id="practiceFileName" type="text" value="aufgabe_loesung.sql" maxlength="120" />
                      <label for="practiceEditor" class="field-label">Arbeitsstand</label>
                      <textarea id="practiceEditor" class="practice-editor" rows="12" placeholder="Schreibe hier deinen SQL-Entwurf oder deine fachliche Begründung."></textarea>
                    </article>
                  </section>

                  <section class="section-block" id="assistant-section">
                    <article class="card assistant-card">
                      <h3>Assistenz für selbstständiges Lernen</h3>
                      <p class="muted">Nutze Weiter für den nächsten Schritt und Check für eine didaktische Prüfung deines aktuellen Arbeitsstands.</p>
                      <form id="assistantHintForm" class="assistant-form">
                        <label>
                          <span>Frage zu SQL, Normalisierung oder Modellierung</span>
                          <textarea
                            name="question"
                            rows="4"
                            required
                            maxlength="4000"
                            placeholder="z. B. Wie entscheide ich, ob eine Bedingung in WHERE oder HAVING gehört?"
                          ></textarea>
                        </label>
                        <label>
                          <span>Rolle</span>
                          <select name="actor_role">
                            <option value="student" selected>Schüler</option>
                            <option value="teacher">Lehrkraft</option>
                          </select>
                        </label>
                        <div class="exercise-actions action-row">
                          <button id="assistantContinueButton" type="button">Weiter</button>
                          <button id="assistantCheckButton" type="button">Check</button>
                          <button type="submit">Freie Frage senden</button>
                        </div>
                      </form>
                      <div class="card self-check-card">
                        <h4>Selbstkontrolle</h4>
                        <div class="self-check-list" id="selfCheckList">
                          <label><input type="checkbox" value="problem" /> Problemstellung verstanden</label>
                          <label><input type="checkbox" value="tables" /> Tabellen und Schlüssel identifiziert</label>
                          <label><input type="checkbox" value="logic" /> Abfragelogik schrittweise aufgebaut</label>
                          <label><input type="checkbox" value="review" /> Ergebnis überprüft und begründet</label>
                        </div>
                        <p id="selfCheckProgress" class="muted">Fortschritt: 0 von 4 Kriterien erfüllt.</p>
                      </div>
                      <div class="info-box feedback-box" aria-live="polite" data-state="warning">
                        <strong>Status</strong>
                        <p id="assistantHintStatus">Noch keine Anfrage gesendet.</p>
                      </div>
                      <div id="assistantHintOutput" class="assistant-output" aria-live="polite"></div>
                    </article>
                  </section>

                  <section class="section-block" id="submission-section">
                    <div class="section-head">
                      <p class="eyebrow">Upload</p>
                      <h2>Schülerlösungen sicher einreichen</h2>
                    </div>
                    <article class="card submission-card">
                      <form id="submissionForm" class="submission-form">
                        <label>
                          <span>Schüler-ID</span>
                          <input type="text" name="student_id" autocomplete="off" required maxlength="128" placeholder="z. B. s-1024" />
                        </label>
                        <label>
                          <span>Aufgaben-ID</span>
                          <input type="text" name="task_id" autocomplete="off" required maxlength="128" placeholder="z. B. task_sql_join_count" />
                        </label>
                        <label class="submission-content">
                          <span>Antwort</span>
                          <textarea name="content" rows="8" required placeholder="Hier kann Code, Text, Zusammenfassung oder Übersetzung eingetragen werden."></textarea>
                        </label>
                        <div class="submission-meta-grid">
                          <label>
                            <span>Inhaltstyp</span>
                            <select name="content_type">
                              <option value="text">Text</option>
                              <option value="code">Code</option>
                              <option value="summary">Zusammenfassung</option>
                              <option value="translation">Übersetzung</option>
                              <option value="transcript">Transkript</option>
                            </select>
                          </label>
                          <label>
                            <span>Quelle</span>
                            <input type="text" name="source" maxlength="32" value="webapp" />
                          </label>
                        </div>
                        <div class="exercise-actions">
                          <button type="submit">Abgabe senden</button>
                        </div>
                        <div class="info-box feedback-box" aria-live="polite">
                          <strong>Status</strong>
                          <p id="submissionStatus">Noch keine Abgabe gesendet.</p>
                        </div>
                      </form>
                    </article>
                  </section>
                </div>

                <aside class="practice-side">
                  <article class="card" id="files-panel">
                    <h3>Dateien und Referenzen</h3>
                    <div class="tab-toolbar compact" role="tablist" aria-label="Praxis-Reiter" data-tab-group="workspace-practice-side">
                      <button type="button" role="tab" id="tab-files" aria-controls="panel-files" aria-selected="true" data-tab-target="panel-files" class="tab-button is-active">Dateien</button>
                      <button type="button" role="tab" id="tab-resources" aria-controls="panel-resources" aria-selected="false" data-tab-target="panel-resources" class="tab-button">Referenzen</button>
                    </div>

                    <section id="panel-files" role="tabpanel" aria-labelledby="tab-files" class="workspace-subpanel is-active">
                      <label for="workingFiles" class="field-label">Dateien zur Bearbeitung</label>
                      <input id="workingFiles" type="file" multiple />
                      <ul id="workingFileList" class="file-list" aria-live="polite"></ul>
                    </section>

                    <section id="panel-resources" role="tabpanel" aria-labelledby="tab-resources" class="workspace-subpanel" hidden>
                      <ul class="resource-list">
                        <li><a href="/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html" target="_blank" rel="noopener">Stichwortverzeichnis</a></li>
                        <li><a href="/generated/anleitungen/stoffverlaufsplan_rdb_3wochen.html" target="_blank" rel="noopener">Stoffverlaufsplan</a></li>
                        <li><a href="/generated/uebungen/README.md" target="_blank" rel="noopener">Übungsübersicht</a></li>
                      </ul>
                    </section>
                  </article>
                </aside>
              </section>
            </section>

            <?php if (!empty($catalogMeta)): ?>
              <p class="meta-note">Inhaltsquelle: <?php echo htmlspecialchars($catalogMeta['managed_by'] ?? 'unbekannt', ENT_QUOTES, 'UTF-8'); ?></p>
            <?php endif; ?>
          </div>
        </div>
      </main>
    </div>

    <script>
      window.PYTHON_API_URL = <?php echo json_encode($pythonApiUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.SUBMISSION_API_BASE_URL = <?php echo json_encode($submissionApiBaseUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.LEARNING_CONTENT = <?php echo json_encode($viewModel, JSON_UNESCAPED_SLASHES); ?>;
    </script>
    <script src="app.js" defer></script>
  </body>
</html>
