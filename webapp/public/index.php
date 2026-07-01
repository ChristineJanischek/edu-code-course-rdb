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
$configuredCourseFiles = getenv('COURSE_WORKING_FILES') ?: '';
$courseFiles = array_values(array_filter(array_map(static fn (string $entry): string => trim($entry), explode(',', $configuredCourseFiles))));
if (count($courseFiles) === 0) {
  $courseFiles = ['aufgabe_loesung.sql'];
}

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
            <a href="#left-window">Kurs: RDB</a>
          </nav>
        </div>
      </header>

      <main class="page">
        <div class="workspace-frames">
          <section class="workspace-pane" id="left-window" aria-label="Kursfenster links">
            <section class="window-shell">
              <div class="tab-toolbar window-tabs" role="tablist" aria-label="Linke Fenster" data-tab-group="workspace-left-window">
                <button type="button" role="tab" id="tab-left-task" aria-controls="panel-left-task" aria-selected="false" data-tab-target="panel-left-task" class="tab-button">Aufgabe</button>
                <button type="button" role="tab" id="tab-left-info" aria-controls="panel-left-info" aria-selected="false" data-tab-target="panel-left-info" class="tab-button">Information</button>
                <button type="button" role="tab" id="tab-left-keywords" aria-controls="panel-left-keywords" aria-selected="true" data-tab-target="panel-left-keywords" class="tab-button is-active">Stichwortsuche</button>
              </div>

              <section class="workspace-panel" id="panel-left-task" role="tabpanel" aria-labelledby="tab-left-task" hidden>
                <article class="card">
                  <p class="eyebrow" id="currentCourseName">Kurs: RDB</p>
                  <h2 id="currentTaskTitle">Keine Aufgabe geladen</h2>
                  <p id="currentTaskDescription">Beim späteren Login wird die zuletzt bearbeitete Aufgabe automatisch geladen. Bis dahin wird der lokale Arbeitsstand verwendet.</p>
                  <p class="muted" id="currentModulePosition">Modul 0 von 0</p>
                  <a class="action-link" id="currentTaskLink" href="#" target="_blank" rel="noopener">Modul öffnen</a>
                </article>
              </section>

              <section class="workspace-panel" id="panel-left-info" role="tabpanel" aria-labelledby="tab-left-info" hidden>
                <article class="card">
                  <h2>Information</h2>
                  <p id="currentInfoText">Zu jeder Aufgabe wird die passende Information geladen.</p>
                  <div class="info-box" id="sessionBehaviorNote" data-state="warning">
                    <strong>Hinweis</strong>
                    <p>Finaler Login-Prozess folgt später. Vorbereitung ist bereits enthalten: Aufgabe, Information und Dateistand werden lokal fortgeführt.</p>
                  </div>
                </article>
              </section>

              <section class="workspace-panel is-active" id="panel-left-keywords" role="tabpanel" aria-labelledby="tab-left-keywords">
                <section class="section-block" id="index-section">
                  <div class="section-head">
                    <p class="eyebrow">Stichwortsuche</p>
                    <h2>Index für Modellierung, Normalisierung und SQL</h2>
                  </div>

                  <article class="card">
                    <label for="keywordSearch" class="field-label">Suchbegriff</label>
                    <form id="keywordSearchForm" class="keyword-search-row" novalidate>
                      <input id="keywordSearch" class="keyword-search" type="search" placeholder="z. B. 3NF, Kardinalität, JOIN" autocomplete="off" />
                      <button type="submit" id="keywordSearchButton">Suchen</button>
                    </form>
                    <div class="info-box feedback-box" data-state="warning" aria-live="polite">
                      <strong>Stichwortsuche</strong>
                      <p id="keywordStatus">Lokale Stichwortsuche aktiv.</p>
                    </div>
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

          <section class="workspace-pane" id="right-window" aria-label="Kursfenster rechts">
            <section class="window-shell">
              <div class="tab-toolbar window-tabs" role="tablist" aria-label="Rechte Fenster" data-tab-group="workspace-right-window">
                <?php foreach ($courseFiles as $index => $fileName): ?>
                  <button type="button" role="tab" id="tab-right-editor-<?php echo $index; ?>" aria-controls="panel-right-editor-<?php echo $index; ?>" aria-selected="<?php echo $index === 0 ? 'true' : 'false'; ?>" data-tab-target="panel-right-editor-<?php echo $index; ?>" class="tab-button<?php echo $index === 0 ? ' is-active' : ''; ?>"><?php echo htmlspecialchars($fileName, ENT_QUOTES, 'UTF-8'); ?></button>
                <?php endforeach; ?>
                <button type="button" role="tab" id="tab-right-upload" aria-controls="panel-right-upload" aria-selected="false" data-tab-target="panel-right-upload" class="tab-button">Upload</button>
                <button type="button" role="tab" id="tab-right-export" aria-controls="panel-right-export" aria-selected="false" data-tab-target="panel-right-export" class="tab-button">Export</button>
                <button type="button" role="tab" id="tab-right-modeler" aria-controls="panel-right-modeler" aria-selected="false" data-tab-target="panel-right-modeler" class="tab-button">ModellEERM</button>
              </div>

              <?php foreach ($courseFiles as $index => $fileName): ?>
                <section class="workspace-panel<?php echo $index === 0 ? ' is-active' : ''; ?>" id="panel-right-editor-<?php echo $index; ?>" role="tabpanel" aria-labelledby="tab-right-editor-<?php echo $index; ?>"<?php echo $index === 0 ? '' : ' hidden'; ?>>
                  <article class="card editor-card">
                    <h3>SQL-Editor</h3>
                    <p class="muted">Datei: <?php echo htmlspecialchars($fileName, ENT_QUOTES, 'UTF-8'); ?></p>
                    <label for="practiceEditor-<?php echo $index; ?>" class="field-label">Code-In Box</label>
                    <textarea id="practiceEditor-<?php echo $index; ?>" class="practice-editor js-course-editor" data-editor-file="<?php echo htmlspecialchars($fileName, ENT_QUOTES, 'UTF-8'); ?>" rows="14" placeholder="Schreibe hier deinen Entwurf für <?php echo htmlspecialchars($fileName, ENT_QUOTES, 'UTF-8'); ?>."></textarea>
                  </article>
                </section>
              <?php endforeach; ?>

              <section class="workspace-panel" id="panel-right-upload" role="tabpanel" aria-labelledby="tab-right-upload" hidden>
                <article class="card submission-card">
                  <h3>Upload</h3>
                  <p class="muted">Alternative zur Bearbeitung im Editor: Lösungsdateien direkt hochladen.</p>
                  <label for="workingFiles" class="field-label">Dateien zur Bearbeitung</label>
                  <input id="workingFiles" type="file" multiple />
                  <ul id="workingFileList" class="file-list" aria-live="polite"></ul>
                </article>
              </section>

              <section class="workspace-panel" id="panel-right-export" role="tabpanel" aria-labelledby="tab-right-export" hidden>
                <article class="card">
                  <h3>Export</h3>
                  <p class="muted">Exportiert den aktuellen Arbeitsstand aller Editor-Dateien aus dieser Sitzung.</p>
                  <div class="action-row">
                    <button type="button" id="exportWorkspaceButton">Arbeitsstand exportieren</button>
                  </div>
                  <label for="exportPreview" class="field-label">Vorschau</label>
                  <textarea id="exportPreview" class="practice-editor" rows="8" readonly></textarea>
                </article>
              </section>

              <section class="workspace-panel" id="panel-right-modeler" role="tabpanel" aria-labelledby="tab-right-modeler" hidden>
                <article class="card modeler-card">
                  <h3>ModellEERM</h3>
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

      <footer class="app-footer" id="course-footer">
        <div class="footer-inner">
          <div class="footer-actions" aria-label="Kursaktionen">
            <a href="#" data-course-action="back">zurück</a>
            <a href="#" data-course-action="next">weiter</a>
            <a href="#" data-course-action="test">testen</a>
            <a href="#" data-course-action="save">speichern</a>
          </div>
          <p class="footer-status" id="workflowStatus" aria-live="polite">Lernpfad bereit.</p>
        </div>
      </footer>
    </div>

    <script>
      window.PYTHON_API_URL = <?php echo json_encode($pythonApiUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.SUBMISSION_API_BASE_URL = <?php echo json_encode($submissionApiBaseUrl, JSON_UNESCAPED_SLASHES); ?>;
      window.LEARNING_CONTENT = <?php echo json_encode($viewModel, JSON_UNESCAPED_SLASHES); ?>;
    </script>
    <script src="app.js" defer></script>
  </body>
</html>
