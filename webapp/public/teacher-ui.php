<?php
declare(strict_types=1);

require_once __DIR__ . '/../app/Repository/TeacherUiModulePlanRepository.php';
require_once __DIR__ . '/../app/Repository/TeachingModuleRepository.php';

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'");

$planRepo    = new \TeacherUiModulePlanRepository(__DIR__ . '/data/teacher-ui-module-plan.json');
$modulesRepo = new \TeachingModuleRepository(__DIR__ . '/data/teaching-modules.json');

$plan           = $planRepo->loadPlan();
$modulesPayload = $modulesRepo->loadModules();

$source         = is_array($plan['source']   ?? null) ? $plan['source']   : [];
$needs          = is_array($plan['needs']    ?? null) ? $plan['needs']    : [];
$planModules    = is_array($plan['modules']  ?? null) ? $plan['modules']  : [];
$milestones     = is_array($plan['milestones']      ?? null) ? $plan['milestones']      : [];
$weeklyReport   = is_array($plan['weekly_report']   ?? null) ? $plan['weekly_report']   : [];
$curriculumRecs = is_array($plan['curriculum_recommendations'] ?? null) ? $plan['curriculum_recommendations'] : [];
$meta           = is_array($plan['meta'] ?? null) ? $plan['meta'] : [];
$sourceConnected = ($meta['source_connected'] ?? false) === true;

$teachingModules = is_array($modulesPayload['modules'] ?? null) ? $modulesPayload['modules'] : [];

// Prozesslanes aufbauen
$processGroups = [];
foreach ($planModules as $mod) {
    if (!is_array($mod)) { continue; }
    $proc = !empty($mod['process']) ? (string) $mod['process'] : 'Unzugeordnet';
    $processGroups[$proc][] = $mod;
}

function esc(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

function statusClass(string $status): string {
    return match ($status) {
        'implemented', 'done' => 'status-implemented',
        'next', 'planned'     => 'status-planned',
        default               => '',
    };
}
?>
<!doctype html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Teacher UI – Modulplan & Unterrichtsmodule</title>
  <link rel="stylesheet" href="style.css" />
  <style>
    .tui-header { padding: 1.5rem 1rem 1rem; max-width: 1100px; margin: 0 auto; }
    .tui-header h1 { margin: 0.4rem 0 0.3rem; font-size: clamp(1.3rem, 2.2vw, 1.8rem); }
    .tui-header p  { margin: 0; color: var(--student-muted); max-width: 72ch; }
    .tui-nav { display: flex; gap: 0.5rem; flex-wrap: wrap; max-width: 1100px;
               margin: 0 auto 0.5rem; padding: 0 1rem; }
    .tui-nav a { color: var(--student-accent); background: #e9f1f8;
                 border: 1px solid #c9d7e6; border-radius: 999px;
                 padding: 0.35rem 0.75rem; font-weight: 700; font-size: 0.88rem;
                 text-decoration: none; }
    .tui-nav a:hover { background: var(--student-accent); color: #fff; border-color: transparent; }
    .tui-body { max-width: 1100px; margin: 0 auto; padding: 0 1rem 3rem; display: grid; gap: 2rem; }
    .tui-section-title { display: flex; align-items: center; gap: 0.6rem; }
    .tui-section-title .eyebrow { margin: 0; }
    .tui-section-title h2 { margin: 0.25rem 0 0; }
    .no-source { padding: 2rem 1rem; text-align: center; color: var(--student-muted); }
    pre.hint-code { background: #f5f8fb; border: 1px solid #d6e1ec; border-radius: 10px;
                    padding: 0.75rem 1rem; font-size: 0.88rem; overflow-x: auto;
                    margin: 0.5rem 0 0; white-space: pre-wrap; }
  </style>
</head>
<body>
<div class="app-shell">

  <header class="app-header">
    <div class="hero-surface" style="max-width:1100px">
      <p class="eyebrow">Teacher UI</p>
      <h1>Modulplan &amp; Unterrichtsmodule</h1>
      <p>Strategieplan der importierten Ideen-Quelle, abgeleitete Module, Meilensteine, Wochenbericht und generierte Unterrichtsmodule.</p>
    </div>
    <div style="max-width:1100px;margin:0 auto;padding:0 1rem 0.9rem;">
      <nav class="tui-nav" aria-label="Abschnitte">
        <a href="#strategie">Strategie</a>
        <a href="#curriculum">Lehrplan-Mapping</a>
        <a href="#prozesse">Prozesse &amp; Module</a>
        <a href="#meilensteine">Meilensteine</a>
        <a href="#wochenbericht">Wochenbericht</a>
        <a href="#unterrichtsmodule">Unterrichtsmodule</a>
        <a href="index.php">← Schülerportal</a>
      </nav>
    </div>
  </header>

  <main class="tui-body">

    <?php if (!$sourceConnected): ?>
      <div class="no-source card">
        <p>Noch keine externe Quelle importiert.</p>
        <pre class="hint-code">python3 scripts/import_teacher_ui_share.py 'https://chatgpt.com/share/...'</pre>
      </div>
    <?php else: ?>

    <!-- ══ STRATEGIE ════════════════════════════════════════════════ -->
    <section id="strategie">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">Importiert: <?php echo esc((string)($meta['imported_at'] ?? '-')); ?></p>
          <h2><?php echo esc((string)($source['title'] ?? 'Quelle')); ?></h2>
        </div>
        <?php if (!empty($source['source_url'])): ?>
          <a class="action-link" style="margin-left:auto;white-space:nowrap;"
             href="<?php echo esc((string)$source['source_url']); ?>" target="_blank" rel="noopener">
            Quell-Chat öffnen ↗
          </a>
        <?php endif; ?>
      </div>

      <div class="card-grid compact" style="margin-top:0.8rem;">
        <article class="card module-plan-card">
          <h3>Idee</h3>
          <p><?php echo esc((string)($source['idea'] ?? '-')); ?></p>
        </article>
        <article class="card module-plan-card">
          <h3>Ausgangspunkt</h3>
          <p class="muted"><?php echo esc((string)($source['ausgangspunkt'] ?? '-')); ?></p>
        </article>
        <article class="card module-plan-card">
          <h3>Ziel</h3>
          <p><?php echo esc((string)($source['ziel'] ?? '-')); ?></p>
        </article>
        <article class="card module-plan-card">
          <h3>Philosophie</h3>
          <p class="muted"><?php echo esc((string)($source['philosophie'] ?? '-')); ?></p>
        </article>
      </div>

      <?php if (!empty($needs)): ?>
      <article class="card module-plan-card" style="margin-top:1rem;">
        <h3>Erkannte Bedürfnisse</h3>
        <ul class="resource-list compact-list">
          <?php foreach ($needs as $need): ?>
            <li><?php echo esc((string)$need); ?></li>
          <?php endforeach; ?>
        </ul>
      </article>
      <?php endif; ?>
    </section>

    <!-- ══ CURRICULUM-MAPPING ════════════════════════════════════════ -->
    <?php if (!empty($curriculumRecs)): ?>
    <section id="curriculum">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">MOD-DID-003</p>
          <h2>Lehrplan- und Didaktik-Mapping</h2>
        </div>
      </div>
      <div class="card-grid compact" style="margin-top:0.8rem;">
        <?php foreach ($curriculumRecs as $rec): ?>
          <?php if (!is_array($rec)) { continue; } ?>
          <article class="card module-plan-nested-card">
            <p class="eyebrow">Curriculum</p>
            <h3><?php echo esc((string)($rec['slug'] ?? '-')); ?></h3>
            <p class="muted"><?php echo esc((string)($rec['source_pdf'] ?? '')); ?></p>
            <?php if (!empty($rec['recommendations']) && is_array($rec['recommendations'])): ?>
              <ul class="resource-list compact-list">
                <?php foreach ($rec['recommendations'] as $r): ?>
                  <?php if (!is_array($r)) { continue; } ?>
                  <li>
                    <strong><?php echo esc((string)($r['title'] ?? '-')); ?></strong>
                    <span class="muted"> – <?php echo esc((string)($r['summary'] ?? '')); ?></span>
                  </li>
                <?php endforeach; ?>
              </ul>
            <?php endif; ?>
          </article>
        <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>

    <!-- ══ PROZESSE & MODULE ══════════════════════════════════════════ -->
    <section id="prozesse">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">Marschplan</p>
          <h2>Prozesse &amp; Module</h2>
        </div>
      </div>
      <?php foreach ($processGroups as $procName => $procMods): ?>
        <div class="process-lane">
          <div class="section-head" style="margin-top:1rem;">
            <p class="eyebrow">Prozess</p>
            <h3><?php echo esc((string)$procName); ?></h3>
          </div>
          <div class="card-grid compact">
            <?php foreach ($procMods as $mod): ?>
              <article class="card module-plan-card">
                <div class="module-plan-head">
                  <strong><?php echo esc((string)($mod['id'] ?? 'MOD')); ?></strong>
                  <span class="status-pill <?php echo esc(statusClass((string)($mod['status'] ?? ''))); ?>">
                    <?php echo esc((string)($mod['status'] ?? '-')); ?>
                  </span>
                </div>
                <h3><?php echo esc((string)($mod['title'] ?? '-')); ?></h3>
                <p><?php echo esc((string)($mod['goal'] ?? '')); ?></p>

                <?php if (!empty($mod['backend_components']) && is_array($mod['backend_components'])): ?>
                  <p class="module-plan-label">Backend</p>
                  <ul class="resource-list compact-list">
                    <?php foreach ($mod['backend_components'] as $bc): ?>
                      <li><?php echo esc((string)$bc); ?></li>
                    <?php endforeach; ?>
                  </ul>
                <?php endif; ?>

                <?php if (!empty($mod['frontend_components']) && is_array($mod['frontend_components'])): ?>
                  <p class="module-plan-label">Frontend</p>
                  <ul class="resource-list compact-list">
                    <?php foreach ($mod['frontend_components'] as $fc): ?>
                      <li><?php echo esc((string)$fc); ?></li>
                    <?php endforeach; ?>
                  </ul>
                <?php endif; ?>

                <?php if (!empty($mod['tests']) && is_array($mod['tests'])): ?>
                  <p class="module-plan-label">Tests</p>
                  <ul class="resource-list compact-list">
                    <?php foreach ($mod['tests'] as $t): ?>
                      <li><?php echo esc((string)$t); ?></li>
                    <?php endforeach; ?>
                  </ul>
                <?php endif; ?>
              </article>
            <?php endforeach; ?>
          </div>
        </div>
      <?php endforeach; ?>
    </section>

    <!-- ══ MEILENSTEINE ════════════════════════════════════════════════ -->
    <?php if (!empty($milestones)): ?>
    <section id="meilensteine">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">Marschplan</p>
          <h2>Meilensteine</h2>
        </div>
      </div>
      <div class="card-grid compact" style="margin-top:0.8rem;">
        <?php foreach ($milestones as $ms): ?>
          <?php if (!is_array($ms)) { continue; } ?>
          <article class="card module-plan-card">
            <div class="module-plan-head">
              <strong><?php echo esc((string)($ms['id'] ?? 'MS')); ?></strong>
              <span class="status-pill <?php echo esc(statusClass((string)($ms['status'] ?? ''))); ?>">
                <?php echo esc((string)($ms['status'] ?? '-')); ?>
              </span>
            </div>
            <p><?php echo esc((string)($ms['title'] ?? '-')); ?></p>
            <?php if (!empty($ms['tests']) && is_array($ms['tests'])): ?>
              <p class="module-plan-label">Tests</p>
              <ul class="resource-list compact-list">
                <?php foreach ($ms['tests'] as $t): ?>
                  <li><?php echo esc((string)$t); ?></li>
                <?php endforeach; ?>
              </ul>
            <?php endif; ?>
          </article>
        <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>

    <!-- ══ WOCHENBERICHT ═══════════════════════════════════════════════ -->
    <?php if (!empty($weeklyReport)): ?>
    <section id="wochenbericht">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">MOD-REP-006</p>
          <h2><?php echo esc((string)($weeklyReport['headline'] ?? 'Wochenbericht')); ?></h2>
        </div>
      </div>
      <article class="card module-plan-card weekly-report-card" style="margin-top:0.8rem;">
        <p><?php echo esc((string)($weeklyReport['current_state'] ?? '')); ?></p>

        <?php if (!empty($weeklyReport['implemented_modules']) && is_array($weeklyReport['implemented_modules'])): ?>
          <p class="module-plan-label">Umgesetzte Module</p>
          <ul class="resource-list compact-list">
            <?php foreach ($weeklyReport['implemented_modules'] as $im): ?>
              <li><?php echo esc((string)$im); ?></li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>

        <?php if (!empty($weeklyReport['next_steps']) && is_array($weeklyReport['next_steps'])): ?>
          <p class="module-plan-label">Nächste Schritte</p>
          <ul class="resource-list compact-list">
            <?php foreach ($weeklyReport['next_steps'] as $ns): ?>
              <li><?php echo esc((string)$ns); ?></li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>
      </article>
    </section>
    <?php endif; ?>

    <!-- ══ GENERIERTE UNTERRICHTSMODULE ═══════════════════════════════ -->
    <section id="unterrichtsmodule">
      <div class="tui-section-title">
        <div>
          <p class="eyebrow">MOD-GEN-004</p>
          <h2>Generierte Unterrichtsmodule</h2>
        </div>
        <span class="muted" style="margin-left:auto;font-size:0.85rem;">
          <?php echo count($teachingModules); ?> Modul<?php echo count($teachingModules) !== 1 ? 'e' : ''; ?>
        </span>
      </div>

      <?php if (empty($teachingModules)): ?>
        <article class="card" style="margin-top:0.8rem;">
          <p class="muted">Keine Module vorhanden.</p>
          <pre class="hint-code">python3 scripts/generate_teaching_module.py</pre>
        </article>
      <?php else: ?>
      <div class="card-grid" style="margin-top:0.8rem;">
        <?php foreach ($teachingModules as $tm): ?>
          <?php if (!is_array($tm)) { continue; } ?>
          <article class="card module-plan-card">
            <div class="module-plan-head">
              <strong><?php echo esc((string)($tm['module_id'] ?? 'MOD')); ?></strong>
              <span class="status-pill <?php echo esc(statusClass((string)($tm['publication_status'] ?? 'draft'))); ?>">
                <?php echo esc((string)($tm['publication_status'] ?? 'draft')); ?>
              </span>
            </div>
            <h3><?php echo esc((string)($tm['title'] ?? 'Modul')); ?></h3>
            <p class="muted">Kontext: <?php echo esc((string)($tm['context_title'] ?? '-')); ?></p>

            <?php if (!empty($tm['learning_goals']) && is_array($tm['learning_goals'])): ?>
              <p class="module-plan-label">Lernziele</p>
              <ol style="padding-left:1.2rem;margin:0.3rem 0 0;">
                <?php foreach ($tm['learning_goals'] as $g): ?>
                  <li style="margin-bottom:0.25rem;"><?php echo esc((string)$g); ?></li>
                <?php endforeach; ?>
              </ol>
            <?php endif; ?>

            <?php if (!empty($tm['tasks']) && is_array($tm['tasks'])): ?>
              <p class="module-plan-label" style="margin-top:0.75rem;">
                Aufgaben (<?php echo count($tm['tasks']); ?>)
              </p>
              <?php foreach ($tm['tasks'] as $task): ?>
                <?php if (!is_array($task)) { continue; } ?>
                <div style="border:1px solid var(--student-line);border-radius:10px;
                            padding:0.6rem 0.75rem;margin-top:0.45rem;background:#fafcfe;">
                  <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
                    <strong><?php echo esc((string)($task['title'] ?? '-')); ?></strong>
                    <span class="topic-pill"><?php echo esc((string)($task['difficulty'] ?? '-')); ?></span>
                  </div>
                  <p style="margin:0;color:var(--student-muted);font-size:0.9rem;">
                    <?php echo esc((string)($task['prompt'] ?? '')); ?>
                  </p>
                </div>
              <?php endforeach; ?>
            <?php endif; ?>

            <?php if (!empty($tm['evaluation_criteria']) && is_array($tm['evaluation_criteria'])): ?>
              <p class="module-plan-label" style="margin-top:0.75rem;">Bewertungskriterien</p>
              <ul class="resource-list compact-list">
                <?php foreach ($tm['evaluation_criteria'] as $ec): ?>
                  <li><?php echo esc((string)$ec); ?></li>
                <?php endforeach; ?>
              </ul>
            <?php endif; ?>

            <?php if (!empty($tm['hints']) && is_array($tm['hints'])): ?>
              <p class="module-plan-label" style="margin-top:0.75rem;">Lernhilfen</p>
              <ul class="resource-list compact-list">
                <?php foreach ($tm['hints'] as $h): ?>
                  <li><?php echo esc((string)$h); ?></li>
                <?php endforeach; ?>
              </ul>
            <?php endif; ?>
          </article>
        <?php endforeach; ?>
      </div>
      <?php endif; ?>
    </section>

    <?php endif; // source_connected ?>

  </main>

  <footer style="border-top:1px solid var(--student-line);padding:0.8rem 1rem;
                 max-width:1100px;margin:0 auto;color:var(--student-muted);font-size:0.82rem;">
    Daten: <code>webapp/public/data/teacher-ui-module-plan.json</code> &amp;
    <code>webapp/public/data/teaching-modules.json</code> ·
    Generator: <code>python3 scripts/generate_teaching_module.py</code>
  </footer>

</div>
</body>
</html>
