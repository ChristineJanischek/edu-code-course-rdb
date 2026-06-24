<?php

declare(strict_types=1);

final class LearningContentRepository
{
    private string $catalogPath;

    public function __construct(string $catalogPath)
    {
        $this->catalogPath = $catalogPath;
    }

    /**
     * @return array<string,mixed>
     */
    public function loadCatalog(): array
    {
        if (!is_file($this->catalogPath)) {
            return $this->defaultCatalog();
        }

        $raw = file_get_contents($this->catalogPath);
        if ($raw === false) {
            return $this->defaultCatalog();
        }

        try {
            $decoded = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        } catch (Throwable) {
            return $this->defaultCatalog();
        }

        if (!is_array($decoded)) {
            return $this->defaultCatalog();
        }

        return array_merge($this->defaultCatalog(), $decoded);
    }

    /**
     * @return array<string,mixed>
     */
    private function defaultCatalog(): array
    {
        return [
            'learningPaths' => [],
            'practiceCards' => [],
            'interactiveExercises' => [],
            'contexts' => [],
            'meta' => [
                'schema' => 'content-db-3nf-v1',
                'managed_by' => 'scripts/content_db_pipeline.py',
            ],
        ];
    }
}
