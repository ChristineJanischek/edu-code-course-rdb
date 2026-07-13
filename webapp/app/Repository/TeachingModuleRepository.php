<?php

declare(strict_types=1);

final class TeachingModuleRepository
{
    private string $modulesPath;

    public function __construct(string $modulesPath)
    {
        $this->modulesPath = $modulesPath;
    }

    /**
     * @return array<string,mixed>
     */
    public function loadModules(): array
    {
        if (!is_file($this->modulesPath)) {
            return $this->defaultPayload();
        }

        $raw = file_get_contents($this->modulesPath);
        if ($raw === false) {
            return $this->defaultPayload();
        }

        try {
            $decoded = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        } catch (Throwable) {
            return $this->defaultPayload();
        }

        return is_array($decoded) ? $decoded : $this->defaultPayload();
    }

    /**
     * @return array<string,mixed>
     */
    private function defaultPayload(): array
    {
        return [
            'meta' => ['managed_by' => 'scripts/generate_teaching_module.py', 'module_count' => 0],
            'modules' => [],
        ];
    }
}
