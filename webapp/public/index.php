<?php
declare(strict_types=1);

require_once __DIR__ . '/../app/Repository/LearningContentRepository.php';
require_once __DIR__ . '/../app/Repository/TeacherUiModulePlanRepository.php';
require_once __DIR__ . '/../app/Repository/TeachingModuleRepository.php';
require_once __DIR__ . '/../app/Controller/StudentPortalController.php';

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'");

$pythonApiUrl = getenv('PYTHON_API_URL') ?: '/api-proxy.php';
$submissionApiBaseUrl = '/api-proxy.php';

function resolveGeneratedBasePath(): string
{
  $candidates = [];

  $configuredPath = getenv('GENERATED_BASE_PATH');
  if (is_string($configuredPath) && trim($configuredPath) !== '') {
    $candidates[] = trim($configuredPath);
  }

  $documentRoot = $_SERVER['DOCUMENT_ROOT'] ?? '';
  if (is_string($documentRoot) && trim($documentRoot) !== '') {
    $candidates[] = rtrim(trim($documentRoot), '/\\') . '/generated';
  }

  $scriptDir = __DIR__;
  $candidates[] = $scriptDir . '/generated';
  $candidates[] = dirname($scriptDir, 2) . '/generated';

  foreach ($candidates as $candidate) {
    if (is_string($candidate) && $candidate !== '' && is_dir($candidate)) {
      return $candidate;
    }
  }

  return $candidates[0] ?? ($scriptDir . '/generated');
}

$contentRepository = new LearningContentRepository(__DIR__ . '/data/learning-content.json');
$teacherUiModulePlanRepository = new \TeacherUiModulePlanRepository(__DIR__ . '/data/teacher-ui-module-plan.json');
$teachingModuleRepository = new \TeachingModuleRepository(__DIR__ . '/data/teaching-modules.json');
$generatedBasePath = resolveGeneratedBasePath();
$studentPortalController = new StudentPortalController($contentRepository, $teacherUiModulePlanRepository, $teachingModuleRepository, $generatedBasePath);
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
$teacherUiPlan = is_array($viewModel['teacherUiPlan'] ?? null) ? $viewModel['teacherUiPlan'] : [];
$teacherUiSource = is_array($teacherUiPlan['source'] ?? null) ? $teacherUiPlan['source'] : [];
$teacherUiNeeds = is_array($teacherUiPlan['needs'] ?? null) ? $teacherUiPlan['needs'] : [];
$teacherUiCurriculumRecommendations = is_array($teacherUiPlan['curriculum_recommendations'] ?? null) ? $teacherUiPlan['curriculum_recommendations'] : [];
$teacherUiModules = is_array($teacherUiPlan['modules'] ?? null) ? $teacherUiPlan['modules'] : [];
$teacherUiMilestones = is_array($teacherUiPlan['milestones'] ?? null) ? $teacherUiPlan['milestones'] : [];
$teacherUiWeeklyReport = is_array($teacherUiPlan['weekly_report'] ?? null) ? $teacherUiPlan['weekly_report'] : [];
$teacherUiMeta = is_array($teacherUiPlan['meta'] ?? null) ? $teacherUiPlan['meta'] : [];
$teachingModulesPayload = is_array($viewModel['teachingModules'] ?? null) ? $viewModel['teachingModules'] : [];
$teachingModules = is_array($teachingModulesPayload['modules'] ?? null) ? $teachingModulesPayload['modules'] : [];
$teacherUiProcessGroups = [];
foreach ($teacherUiModules as $moduleEntry) {
  if (!is_array($moduleEntry)) {
    continue;
  }

  $processName = !empty($moduleEntry['process']) ? (string) $moduleEntry['process'] : 'Unzugeordnet';
  if (!array_key_exists($processName, $teacherUiProcessGroups)) {
    $teacherUiProcessGroups[$processName] = [];
  }
  $teacherUiProcessGroups[$processName][] = $moduleEntry;
}
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

$initialExerciseLink = $exerciseLinks[0] ?? null;
$initialTaskHref = is_array($initialExerciseLink) && !empty($initialExerciseLink['href'])
  ? (string) $initialExerciseLink['href']
  : '#';
$initialTaskTitle = is_array($initialExerciseLink) && !empty($initialExerciseLink['title'])
  ? (string) $initialExerciseLink['title']
  : 'Keine Aufgabe geladen';
$initialTaskDescription = is_array($initialExerciseLink) && !empty($initialExerciseLink['description'])
  ? (string) $initialExerciseLink['description']
  : 'Beim späteren Login wird die zuletzt bearbeitete Aufgabe automatisch geladen. Bis dahin wird der lokale Arbeitsstand verwendet.';

$moduleSwitchDefinitions = [
  [
    'slug' => 'UE01_foodtrucknetz_sql_abfragen.html',
    'label' => 'SQL Abfragen Foodtrucknetz DB',
    'fallbackHref' => '/generated/uebungen/UE01_foodtrucknetz_sql_abfragen.html',
  ],
  [
    'slug' => 'UE02_stadtfahrradverleih_sql_abfragen.html',
    'label' => 'SQL Abfragen Stadtfahrradverleih DB',
    'fallbackHref' => '/generated/uebungen/UE02_stadtfahrradverleih_sql_abfragen.html',
  ],
];

$moduleSwitchOptions = [];
foreach ($moduleSwitchDefinitions as $definition) {
  $href = $definition['fallbackHref'];
  foreach ($exerciseLinks as $entry) {
    if (!is_array($entry) || empty($entry['href'])) {
      continue;
    }

    $candidateHref = (string) $entry['href'];
    if (str_contains($candidateHref, $definition['slug'])) {
      $href = $candidateHref;
      break;
    }
  }

  $moduleSwitchOptions[] = [
    'label' => $definition['label'],
    'href' => $href,
  ];
}

$selectedModuleHref = $moduleSwitchOptions[0]['href'] ?? '#';
if (str_contains($initialTaskHref, 'UE02_stadtfahrradverleih_sql_abfragen.html')) {
  $selectedModuleHref = $moduleSwitchOptions[1]['href'] ?? $selectedModuleHref;
}

if ($initialTaskHref === '#' || str_contains($initialTaskHref, 'README.md')) {
  $initialTaskHref = $selectedModuleHref;
}

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

      <section class="assistant-banner" aria-label="SQL-Assistent">
        <div class="assistant-banner-inner">
          <div class="sql-assistant-shell">
            <div class="sql-assistant-head">
              <h3>SQL-Assistent</h3>
              <p class="sql-assistant-module">Modul geladen: SQL Abfragen Foodtrucknetz DB. Aufgabe 1-14 jetzt linear bearbeiten.</p>
              <p id="workflowStatus" class="sql-assistant-note" aria-live="polite">Tippe eine Abfrage ein und starte den Test.</p>
            </div>
            <div class="footer-actions" aria-label="Kursaktionen">
              <button type="button" data-course-action="test">Abfrage testen (Ergebnis)</button>
              <button type="button" data-course-action="next">Nächster Schritt</button>
              <button type="button" data-course-action="hint">i Lernhilfe</button>
              <button type="button" data-assistant-action="solution">✔ Musterlösung</button>
              <button type="button" data-assistant-action="expected">📋 Erwartetes Ergebnis</button>
            </div>
            <div class="info-box feedback-box" id="sqlTestLogBox" data-state="warning" aria-live="polite">
              <strong>SQL-Testprotokoll</strong>
              <p id="sqlTestLog">Noch kein Test gestartet.</p>
              <p id="sqlTestHint" class="muted">Hinweise erscheinen hier mit Zeilenbezug, sobald die Abfrage getestet wird.</p>
            </div>
            <div id="assistantHintBox" class="hint-panel" hidden>
              <strong>💡 Lernhilfe</strong>
              <p id="assistantHintText">Keine Lernhilfe verfügbar.</p>
            </div>
            <div id="assistantSolutionBox" class="sol-box" hidden>
              <strong>Musterlösung</strong>
              <pre id="assistantSolutionSql"></pre>
            </div>
            <div id="assistantExpectedBox" class="res-box" hidden>
              <strong>Erwartetes Ergebnis</strong>
              <div id="assistantExpectedContent"></div>
            </div>
            <div id="sqlResultGrid" class="sql-result-grid" hidden></div>
          </div>
        </div>
      </section>

      <main class="page">
        <div class="workspace-frames">
          <section class="workspace-pane" id="left-window" aria-label="Kursfenster links">
            <section class="window-shell">
              <div class="tab-toolbar window-tabs" role="tablist" aria-label="Linke Fenster" data-tab-group="workspace-left-window">
                <button type="button" role="tab" id="tab-left-task" aria-controls="panel-left-task" aria-selected="true" data-tab-target="panel-left-task" class="tab-button is-active">Aufgabe</button>
                <button type="button" role="tab" id="tab-left-info" aria-controls="panel-left-info" aria-selected="false" data-tab-target="panel-left-info" class="tab-button">Information</button>
                <button type="button" role="tab" id="tab-left-keywords" aria-controls="panel-left-keywords" aria-selected="false" data-tab-target="panel-left-keywords" class="tab-button">Stichwortsuche</button>
              </div>

              <section class="workspace-panel is-active" id="panel-left-task" role="tabpanel" aria-labelledby="tab-left-task">
                <article class="card">
                  <p class="eyebrow" id="currentCourseName">Kurs: RDB</p>
                  <h2 id="currentTaskTitle"><?php echo htmlspecialchars($initialTaskTitle, ENT_QUOTES, 'UTF-8'); ?></h2>
                  <p class="task-meta" id="currentTaskTopic">★☆☆ Einfach · WHERE · OR · ORDER BY</p>
                  <div id="currentTaskDescription" class="task-description-rich"><?php echo htmlspecialchars($initialTaskDescription, ENT_QUOTES, 'UTF-8'); ?></div>
                  <div class="hint-panel" id="currentTaskHintPanel">
                    <strong>💡 Tipp</strong>
                    <p id="currentTaskHint">Nutze den Modulmodus und bearbeite die Aufgaben der Reihe nach.</p>
                  </div>
                  <p class="muted" id="currentModulePosition">Modul 0 von 0</p>
                  <div class="module-switcher">
                    <label for="moduleSelect" class="field-label">Modul auswählen</label>
                    <div class="module-switch-row">
                      <select id="moduleSelect" class="module-select" aria-label="SQL-Modul auswählen">
                        <?php foreach ($moduleSwitchOptions as $option): ?>
                          <option value="<?php echo htmlspecialchars($option['href'], ENT_QUOTES, 'UTF-8'); ?>"<?php echo $option['href'] === $selectedModuleHref ? ' selected' : ''; ?>><?php echo htmlspecialchars($option['label'], ENT_QUOTES, 'UTF-8'); ?></option>
                        <?php endforeach; ?>
                      </select>
                      <a class="action-link" id="moduleOpenLink" href="<?php echo htmlspecialchars($selectedModuleHref, ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener">Ausgewähltes Modul öffnen</a>
                    </div>
                  </div>
                  <a class="action-link" id="currentTaskLink" href="<?php echo htmlspecialchars($initialTaskHref, ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener">Aktueller Arbeitsstand öffnen</a>
                </article>
              </section>

              <section class="workspace-panel" id="panel-left-info" role="tabpanel" aria-labelledby="tab-left-info" hidden>
                <article class="card">
                  <h2>Information</h2>
                  <p id="currentInfoText">Zu jeder Aufgabe wird die passende Information geladen.</p>
                  <div id="currentInfoContent" class="info-rich-content"></div>
                  <div class="info-box" id="sessionBehaviorNote" data-state="warning">
                    <strong>Hinweis</strong>
                    <p>Finaler Login-Prozess folgt später. Vorbereitung ist bereits enthalten: Aufgabe, Information und Dateistand werden lokal fortgeführt.</p>
                  </div>
                </article>

                <?php if (($teacherUiMeta['source_connected'] ?? false) === true): ?>
                  <section class="section-block">
                    <div class="section-head">
                      <p class="eyebrow">Teacher-UI Strategie</p>
                      <h2><?php echo htmlspecialchars((string) ($teacherUiSource['title'] ?? 'Externe Quelle'), ENT_QUOTES, 'UTF-8'); ?></h2>
                    </div>

                    <div class="card-grid compact">
                      <article class="card module-plan-card">
                        <h3>Idee</h3>
                        <p><?php echo htmlspecialchars((string) ($teacherUiSource['idea'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>
                        <p class="muted"><?php echo htmlspecialchars((string) ($teacherUiSource['ausgangspunkt'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>
                      </article>
                      <article class="card module-plan-card">
                        <h3>Ziel</h3>
                        <p><?php echo htmlspecialchars((string) ($teacherUiSource['ziel'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>
                        <p class="muted"><?php echo htmlspecialchars((string) ($teacherUiSource['philosophie'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>
                      </article>
                      <article class="card module-plan-card">
                        <h3>Quelle</h3>
                        <p class="muted">Importiert am: <?php echo htmlspecialchars((string) ($teacherUiMeta['imported_at'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>
                        <?php if (!empty($teacherUiSource['source_url'])): ?>
                          <a class="action-link" href="<?php echo htmlspecialchars((string) $teacherUiSource['source_url'], ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener">Quell-Chat öffnen</a>
                        <?php endif; ?>
                      </article>
                    </div>

                    <?php if (!empty($teacherUiNeeds)): ?>
                      <article class="card module-plan-card">
                        <h3>Erkannte Bedürfnisse</h3>
                        <ul class="resource-list">
                          <?php foreach ($teacherUiNeeds as $needEntry): ?>
                            <li><?php echo htmlspecialchars((string) $needEntry, ENT_QUOTES, 'UTF-8'); ?></li>
                          <?php endforeach; ?>
                        </ul>
                      </article>
                    <?php endif; ?>

                    <?php if (!empty($teacherUiCurriculumRecommendations)): ?>
                      <article class="card module-plan-card">
                        <h3>Lehrplan- und Didaktik-Mapping</h3>
                        <div class="card-grid compact">
                          <?php foreach ($teacherUiCurriculumRecommendations as $curriculumEntry): ?>
                            <?php if (is_array($curriculumEntry)): ?>
                              <article class="card module-plan-nested-card">
                                <p class="eyebrow">Curriculum</p>
                                <h3><?php echo htmlspecialchars((string) ($curriculumEntry['slug'] ?? 'curriculum'), ENT_QUOTES, 'UTF-8'); ?></h3>
                                <?php if (!empty($curriculumEntry['source_pdf'])): ?>
                                  <p class="muted"><?php echo htmlspecialchars((string) $curriculumEntry['source_pdf'], ENT_QUOTES, 'UTF-8'); ?></p>
                                <?php endif; ?>
                                <?php if (!empty($curriculumEntry['recommendations']) && is_array($curriculumEntry['recommendations'])): ?>
                                  <ul class="resource-list compact-list">
                                    <?php foreach ($curriculumEntry['recommendations'] as $recommendationEntry): ?>
                                      <?php if (is_array($recommendationEntry)): ?>
                                        <li>
                                          <strong><?php echo htmlspecialchars((string) ($recommendationEntry['title'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></strong>
                                          <span class="muted"> <?php echo htmlspecialchars((string) ($recommendationEntry['summary'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></span>
                                        </li>
                                      <?php endif; ?>
                                    <?php endforeach; ?>
                                  </ul>
                                <?php endif; ?>
                              </article>
                            <?php endif; ?>
                          <?php endforeach; ?>
                        </div>
                      </article>
                    <?php endif; ?>

                    <?php foreach ($teacherUiProcessGroups as $processName => $processModules): ?>
                      <section class="process-lane">
                        <div class="section-head">
                          <p class="eyebrow">Prozess</p>
                          <h3><?php echo htmlspecialchars((string) $processName, ENT_QUOTES, 'UTF-8'); ?></h3>
                        </div>
                        <div class="card-grid compact">
                          <?php foreach ($processModules as $moduleEntry): ?>
                            <article class="card module-plan-card">
                              <div class="module-plan-head">
                                <strong><?php echo htmlspecialchars((string) ($moduleEntry['id'] ?? 'MOD'), ENT_QUOTES, 'UTF-8'); ?></strong>
                                <span class="status-pill status-<?php echo htmlspecialchars((string) ($moduleEntry['status'] ?? 'planned'), ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars((string) ($moduleEntry['status'] ?? 'planned'), ENT_QUOTES, 'UTF-8'); ?></span>
                              </div>
                              <h3><?php echo htmlspecialchars((string) ($moduleEntry['title'] ?? 'Unbenanntes Modul'), ENT_QUOTES, 'UTF-8'); ?></h3>
                              <p><?php echo htmlspecialchars((string) ($moduleEntry['goal'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>

                              <?php if (!empty($moduleEntry['backend_components']) && is_array($moduleEntry['backend_components'])): ?>
                                <p class="module-plan-label">Backend</p>
                                <ul class="resource-list compact-list">
                                  <?php foreach ($moduleEntry['backend_components'] as $backendComponent): ?>
                                    <li><?php echo htmlspecialchars((string) $backendComponent, ENT_QUOTES, 'UTF-8'); ?></li>
                                  <?php endforeach; ?>
                                </ul>
                              <?php endif; ?>

                              <?php if (!empty($moduleEntry['frontend_components']) && is_array($moduleEntry['frontend_components'])): ?>
                                <p class="module-plan-label">Frontend</p>
                                <ul class="resource-list compact-list">
                                  <?php foreach ($moduleEntry['frontend_components'] as $frontendComponent): ?>
                                    <li><?php echo htmlspecialchars((string) $frontendComponent, ENT_QUOTES, 'UTF-8'); ?></li>
                                  <?php endforeach; ?>
                                </ul>
                              <?php endif; ?>

                              <?php if (!empty($moduleEntry['tests']) && is_array($moduleEntry['tests'])): ?>
                                <p class="module-plan-label">Tests</p>
                                <ul class="resource-list compact-list">
                                  <?php foreach ($moduleEntry['tests'] as $testEntry): ?>
                                    <li><?php echo htmlspecialchars((string) $testEntry, ENT_QUOTES, 'UTF-8'); ?></li>
                                  <?php endforeach; ?>
                                </ul>
                              <?php endif; ?>
                            </article>
                          <?php endforeach; ?>
                        </div>
                      </section>
                    <?php endforeach; ?>

                    <?php if (!empty($teacherUiMilestones)): ?>
                      <article class="card module-plan-card">
                        <h3>Meilensteine</h3>
                        <ul class="resource-list">
                          <?php foreach ($teacherUiMilestones as $milestoneEntry): ?>
                            <?php if (is_array($milestoneEntry)): ?>
                              <li>
                                <strong><?php echo htmlspecialchars((string) ($milestoneEntry['id'] ?? 'MS'), ENT_QUOTES, 'UTF-8'); ?></strong>
                                : <?php echo htmlspecialchars((string) ($milestoneEntry['title'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?>
                                (<?php echo htmlspecialchars((string) ($milestoneEntry['status'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?>)
                              </li>
                            <?php endif; ?>
                          <?php endforeach; ?>
                        </ul>
                      </article>
                    <?php endif; ?>

                    <?php if (!empty($teacherUiWeeklyReport)): ?>
                      <article class="card module-plan-card weekly-report-card">
                        <h3><?php echo htmlspecialchars((string) ($teacherUiWeeklyReport['headline'] ?? 'Wochenbericht'), ENT_QUOTES, 'UTF-8'); ?></h3>
                        <p><?php echo htmlspecialchars((string) ($teacherUiWeeklyReport['current_state'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></p>

                        <?php if (!empty($teacherUiWeeklyReport['implemented_modules']) && is_array($teacherUiWeeklyReport['implemented_modules'])): ?>
                          <p class="module-plan-label">Umgesetzte Module</p>
                          <ul class="resource-list compact-list">
                            <?php foreach ($teacherUiWeeklyReport['implemented_modules'] as $implementedModule): ?>
                              <li><?php echo htmlspecialchars((string) $implementedModule, ENT_QUOTES, 'UTF-8'); ?></li>
                            <?php endforeach; ?>
                          </ul>
                        <?php endif; ?>

                        <?php if (!empty($teacherUiWeeklyReport['next_steps']) && is_array($teacherUiWeeklyReport['next_steps'])): ?>
                          <p class="module-plan-label">Nächste Schritte</p>
                          <ul class="resource-list compact-list">
                            <?php foreach ($teacherUiWeeklyReport['next_steps'] as $nextStep): ?>
                              <li><?php echo htmlspecialchars((string) $nextStep, ENT_QUOTES, 'UTF-8'); ?></li>
                            <?php endforeach; ?>
                          </ul>
                        <?php endif; ?>
                      </article>
                    <?php endif; ?>
                  </section>
                <?php endif; ?>

                <?php if (!empty($teachingModules)): ?>
                  <section class="section-block">
                    <div class="section-head">
                      <p class="eyebrow">MOD-GEN-004</p>
                      <h2>Generierte Unterrichtsmodule</h2>
                    </div>
                    <div class="card-grid compact">
                      <?php foreach ($teachingModules as $teachingModule): ?>
                        <?php if (!is_array($teachingModule)) { continue; } ?>
                        <article class="card module-plan-card">
                          <div class="module-plan-head">
                            <strong><?php echo htmlspecialchars((string) ($teachingModule['module_id'] ?? 'MOD'), ENT_QUOTES, 'UTF-8'); ?></strong>
                            <span class="status-pill status-<?php echo htmlspecialchars((string) ($teachingModule['publication_status'] ?? 'draft'), ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars((string) ($teachingModule['publication_status'] ?? 'draft'), ENT_QUOTES, 'UTF-8'); ?></span>
                          </div>
                          <h3><?php echo htmlspecialchars((string) ($teachingModule['title'] ?? 'Modul'), ENT_QUOTES, 'UTF-8'); ?></h3>

                          <?php if (!empty($teachingModule['learning_goals']) && is_array($teachingModule['learning_goals'])): ?>
                            <p class="module-plan-label">Lernziele</p>
                            <ul class="resource-list compact-list">
                              <?php foreach ($teachingModule['learning_goals'] as $goal): ?>
                                <li><?php echo htmlspecialchars((string) $goal, ENT_QUOTES, 'UTF-8'); ?></li>
                              <?php endforeach; ?>
                            </ul>
                          <?php endif; ?>

                          <?php if (!empty($teachingModule['tasks']) && is_array($teachingModule['tasks'])): ?>
                            <p class="module-plan-label">Aufgaben (<?php echo count($teachingModule['tasks']); ?>)</p>
                            <ul class="resource-list compact-list">
                              <?php foreach ($teachingModule['tasks'] as $taskItem): ?>
                                <?php if (!is_array($taskItem)) { continue; } ?>
                                <li>
                                  <?php echo htmlspecialchars((string) ($taskItem['title'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?>
                                  <span class="muted"> · <?php echo htmlspecialchars((string) ($taskItem['difficulty'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></span>
                                </li>
                              <?php endforeach; ?>
                            </ul>
                          <?php endif; ?>

                          <?php if (!empty($teachingModule['hints']) && is_array($teachingModule['hints'])): ?>
                            <p class="module-plan-label">Lernhilfen</p>
                            <ul class="resource-list compact-list">
                              <?php foreach ($teachingModule['hints'] as $hintItem): ?>
                                <li><?php echo htmlspecialchars((string) $hintItem, ENT_QUOTES, 'UTF-8'); ?></li>
                              <?php endforeach; ?>
                            </ul>
                          <?php endif; ?>
                        </article>
                      <?php endforeach; ?>
                    </div>
                  </section>
                <?php endif; ?>
              </section>

              <section class="workspace-panel" id="panel-left-keywords" role="tabpanel" aria-labelledby="tab-left-keywords" hidden>
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
                    <div id="keywordInsights" class="keyword-insights" hidden aria-live="polite"></div>
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
                    <h3 id="currentSqlEditorHeading">SQL-Editor</h3>
                    <p class="muted">Datei: <?php echo htmlspecialchars($fileName, ENT_QUOTES, 'UTF-8'); ?></p>
                    <label for="practiceEditor-<?php echo $index; ?>" class="field-label" id="currentSqlDraftLabel">Dein SQL-Entwurf:</label>
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
                  <div class="modeler-canvas" id="modelerCanvas" aria-label="EERM Zeichenfläche" tabindex="0">
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
          <div class="license-box" aria-label="Lizenzhinweise">
            <p class="license-note">Lizenzhinweis: Für diese Anwendung gelten die Bestimmungen aus LICENSE und NOTICE.</p>
            <details class="license-info">
              <summary class="license-info-toggle" aria-label="Lizenz- und Notice-Informationen anzeigen">i</summary>
              <div class="license-info-panel">
                <p><strong>Lizenz:</strong> Custom License - Christine Janischek NC School-Only 1.0</p>
                <ul>
                  <li>Sichtbare Attribution erforderlich: Christine Janischek - https://emotionalspirit.de</li>
                  <li>Nicht-kommerzielle Nutzung</li>
                  <li>Nutzung nur im Kontext staatlicher Schulsysteme</li>
                  <li>Andere Nutzungen nur mit ausdrücklicher schriftlicher Erlaubnis</li>
                </ul>
                <p><strong>Notice:</strong> Required attribution text siehe NOTICE.</p>
              </div>
            </details>
          </div>
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
