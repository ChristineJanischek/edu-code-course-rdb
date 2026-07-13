<?php

declare(strict_types=1);

final class TeacherUiModulePlanRepository
{
    private string $planPath;

    public function __construct(string $planPath)
    {
        $this->planPath = $planPath;
    }

    /**
     * @return array<string,mixed>
     */
    public function loadPlan(): array
    {
        if (!is_file($this->planPath)) {
            return $this->defaultPlan();
        }

        $raw = file_get_contents($this->planPath);
        if ($raw === false) {
            return $this->defaultPlan();
        }

        try {
            $decoded = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        } catch (Throwable) {
            return $this->defaultPlan();
        }

        if (!is_array($decoded)) {
            return $this->defaultPlan();
        }

        return array_merge($this->defaultPlan(), $decoded);
    }

    /**
     * @return array<string,mixed>
     */
    private function defaultPlan(): array
    {
        return [
            'meta' => [
                'managed_by' => 'scripts/import_teacher_ui_share.py',
                'source_connected' => false,
            ],
            'source' => [],
            'needs' => [],
            'modules' => [],
            'milestones' => [],
            'weekly_report' => [],
        ];
    }
}