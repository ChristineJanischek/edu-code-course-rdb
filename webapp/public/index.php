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

        <div class="header-nav-shell">
          <button type="button" class="nav-toggle" aria-controls="primaryNav" aria-expanded="false">Kursnavigation</button>
          <nav id="primaryNav" class="primary-nav" aria-label="Kursnavigation">
            <a href="#left-window">Reiter 1: Aufgabe/Information</a>
            <a href="#right-window">Reiter 2: SQL, Dateien, ModellER</a>
            <a href="#assistant-footer">Assistenz-Funktionen</a>
            <a href="#" data-nav-action="toggle-assistant-dock" aria-controls="assistantDock" aria-expanded="false">KI-Assistenz-Avatar öffnen</a>
          </nav>
        </div>
      </header>

      <main class="page">
        <div class="workspace-frames">
          <section class="workspace-pane" id="left-window" aria-label="Reiter 1: Aufgabe und Stichwortsuche">
            <section class="window-shell">
              <div class="tab-toolbar window-tabs" role="tablist" aria-label="Reiter 1 Fenster" data-tab-group="workspace-left-window">
                <button type="button" role="tab" id="tab-left-info" aria-controls="panel-left-info" aria-selected="true" data-tab-target="panel-left-info" class="tab-button is-active">Fenster: Aufgabe/Information</button>
                <button type="button" role="tab" id="tab-left-keywords" aria-controls="panel-left-keywords" aria-selected="false" data-tab-target="panel-left-keywords" class="tab-button">Fenster: Stichwortsuche</button>
              </div>

              <section class="workspace-panel is-active" id="panel-left-info" role="tabpanel" aria-labelledby="tab-left-info">
                <section class="card intro-card">
                  <div class="split-grid">
                    <div>
                      <p class="eyebrow">Reiter 1</p>
                      <h2>Aufgabe und Information</h2>
                      <p>Dieser Bereich bündelt alle Aufgabenkontexte. Die konkrete Bearbeitung erfolgt im rechten Reiter mit SQL-Editor, Datei-Upload und optionalem ModellER.</p>
                    </div>
                    <div>
                      <h3>Arbeitslogik</h3>
                      <ul class="check-list">
                        <li>Aufgabe lesen und Anforderungen markieren</li>
                        <li>Vorgehen planen und Schlüsselbegriffe klären</li>
                        <li>Lösung im rechten Reiter erstellen</li>
                        <li>Weiter/Check im Footer nutzen</li>
                      </ul>
                    </div>
                  </div>
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
              </section>

              <section class="workspace-panel" id="panel-left-keywords" role="tabpanel" aria-labelledby="tab-left-keywords" hidden>
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
            </section>
          </section>

          <section class="workspace-pane" id="right-window" aria-label="Reiter 2: SQL, Dateien und ModellER">
            <section class="window-shell">
              <div class="tab-toolbar window-tabs" role="tablist" aria-label="Reiter 2 Fenster" data-tab-group="workspace-right-window">
                <button type="button" role="tab" id="tab-right-workbench" aria-controls="panel-right-workbench" aria-selected="true" data-tab-target="panel-right-workbench" class="tab-button is-active">Fenster: SQL-Code + Upload</button>
                <button type="button" role="tab" id="tab-right-files" aria-controls="panel-right-files" aria-selected="false" data-tab-target="panel-right-files" class="tab-button">Fenster: Datei-Reiter</button>
                <button type="button" role="tab" id="tab-right-modeler" aria-controls="panel-right-modeler" aria-selected="false" data-tab-target="panel-right-modeler" class="tab-button">Fenster: ModellER</button>
              </div>

              <section class="workspace-panel is-active" id="panel-right-workbench" role="tabpanel" aria-labelledby="tab-right-workbench">
                <section class="section-block" id="editor-section">
                  <article class="card editor-card">
                    <h3>SQL-Code im Editor (Arbeitsstand)</h3>
                    <label for="practiceFileName" class="field-label">Arbeitsdatei</label>
                    <input id="practiceFileName" type="text" value="aufgabe_loesung.sql" maxlength="120" />
                    <label for="practiceEditor" class="field-label">Entwurf</label>
                    <textarea id="practiceEditor" class="practice-editor" rows="10" placeholder="Schreibe hier deinen SQL-Entwurf oder deine fachliche Begründung."></textarea>
                  </article>
                </section>

                <section class="section-block" id="submission-section">
                  <div class="section-head">
                    <p class="eyebrow">Datei-Upload</p>
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
              </section>

              <section class="workspace-panel" id="panel-right-files" role="tabpanel" aria-labelledby="tab-right-files" hidden>
                <article class="card" id="files-panel">
                  <h3>Datei-Reiter</h3>
                  <div class="tab-toolbar compact" role="tablist" aria-label="Datei-Reiter" data-tab-group="workspace-practice-side">
                    <button type="button" role="tab" id="tab-files" aria-controls="panel-files" aria-selected="true" data-tab-target="panel-files" class="tab-button is-active">Dateien</button>
                    <button type="button" role="tab" id="tab-resources" aria-controls="panel-resources" aria-selected="false" data-tab-target="panel-resources" class="tab-button">Aufgabenquellen</button>
                  </div>

                  <section id="panel-files" role="tabpanel" aria-labelledby="tab-files" class="workspace-subpanel is-active">
                    <label for="workingFiles" class="field-label">Dateien zur Bearbeitung</label>
                    <input id="workingFiles" type="file" multiple />
                    <ul id="workingFileList" class="file-list" aria-live="polite"></ul>
                  </section>

                  <section id="panel-resources" role="tabpanel" aria-labelledby="tab-resources" class="workspace-subpanel" hidden>
                    <ul class="resource-list">
                      <?php foreach ($exerciseLinks as $item): ?>
                        <li><a href="<?php echo htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener"><?php echo htmlspecialchars($item['title'], ENT_QUOTES, 'UTF-8'); ?></a></li>
                      <?php endforeach; ?>
                    </ul>
                  </section>
                </article>
              </section>

              <section class="workspace-panel" id="panel-right-modeler" role="tabpanel" aria-labelledby="tab-right-modeler" hidden>
                <article class="card modeler-card">
                  <h3>ModellER (EERM-Designer)</h3>
                  <div class="modeler-toolbar" role="toolbar" aria-label="Werkzeugleiste ModellER">
                    <button type="button">Entität</button>
                    <button type="button">Beziehung</button>
                    <button type="button">Attribut</button>
                    <button type="button">1:N</button>
                    <button type="button">N:M</button>
                    <button type="button">Export</button>
                  </div>
                  <div class="modeler-canvas" aria-label="EERM Zeichenfläche" tabindex="0">
                    Platzhalter für den EERM-Designer. Hier kann ein bestehender Designer oder eine Canvas-Komponente angebunden werden.
                  </div>
                </article>
              </section>
            </section>
          </section>
        </div>

        <?php if (!empty($catalogMeta)): ?>
          <p class="meta-note">Inhaltsquelle: <?php echo htmlspecialchars($catalogMeta['managed_by'] ?? 'unbekannt', ENT_QUOTES, 'UTF-8'); ?></p>
        <?php endif; ?>
      </main>

      <footer class="app-footer" id="assistant-footer">
        <div class="footer-inner">
          <article class="card assistant-card">
            <h3>Assistenz-Funktionen</h3>
            <p class="muted">Weiter und Check sind im Footer verortet und greifen auf den Arbeitsstand aus dem rechten Fenster zu. Das KI-Assistenz-Avatar-Fenster kann separat rechts eingeblendet werden.</p>
            <form id="assistantHintForm" class="assistant-form">
              <label>
                <span>Frage zu SQL, Normalisierung oder Modellierung</span>
                <textarea
                  name="question"
                  rows="3"
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
            <div class="info-box feedback-box" aria-live="polite" data-state="warning">
              <strong>Status</strong>
              <p id="assistantHintStatus">Noch keine Anfrage gesendet.</p>
            </div>
            <div id="assistantHintOutput" class="assistant-output" aria-live="polite"></div>
          </article>
        </div>
      </footer>

      <aside id="assistantDock" class="assistant-dock" aria-label="KI-Assistenz-Avatar" hidden>
        <div class="assistant-dock-head">
          <h3>KI-Assistenz-Avatar</h3>
          <button type="button" id="assistantDockClose" class="assistant-dock-close" aria-label="Assistenzfenster schließen">Schließen</button>
        </div>
        <div class="assistant-avatar" aria-hidden="true">KI</div>
        <p class="muted">Quelle: LLM. Dieses Fenster ist als rechtses Assistenz-Frame andockbar.</p>
        <div class="assistant-dock-body">
          <p>Nutze im Footer die Buttons Weiter/Check. Die Hinweise erscheinen dort und können hier als Assistenzbereich ergänzt werden.</p>
        </div>
      </aside>
    </div>

    <script>
      window.PYTHON_API_URL = <?php echo json_encode($pythonApiUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.SUBMISSION_API_BASE_URL = <?php echo json_encode($submissionApiBaseUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.LEARNING_CONTENT = <?php echo json_encode($viewModel, JSON_UNESCAPED_SLASHES); ?>;
    </script>
    <script src="app.js" defer></script>
  </body>
</html>
