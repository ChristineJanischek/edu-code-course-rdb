<?php

declare(strict_types=1);

final class StudentPortalController
{
    private LearningContentRepository $repository;
    private string $generatedBasePath;

    public function __construct(LearningContentRepository $repository, ?string $generatedBasePath = null)
    {
        $this->repository = $repository;
        $this->generatedBasePath = $generatedBasePath ?? '/var/www/html/generated';
    }

    /**
     * @return array<string,mixed>
     */
    public function buildViewModel(): array
    {
        $catalog = $this->repository->loadCatalog();

        return [
            'learningPaths' => $this->normalizeList($catalog['learningPaths'] ?? []),
            'curriculumTopics' => $this->normalizeList($catalog['contexts'] ?? []),
            'exerciseLinks' => $this->exerciseLinks(),
            'learningPlanLinks' => $this->learningPlanLinks(),
            'indexLinks' => $this->indexLinks(),
            'catalogMeta' => is_array($catalog['meta'] ?? null) ? $catalog['meta'] : [],
        ];
    }

    /**
     * @param mixed $value
     * @return array<int,array<string,mixed>>
     */
    private function normalizeList(mixed $value): array
    {
        if (!is_array($value)) {
            return [];
        }

        $normalized = [];
        foreach ($value as $entry) {
            if (is_array($entry)) {
                $normalized[] = $entry;
            }
        }

        return $normalized;
    }

    /**
     * @return array<int,array<string,string>>
     */
    private function learningPlanLinks(): array
    {
        return [
            [
                'title' => 'Stoffverlaufsplan (3 Wochen)',
                'href' => '/generated/anleitungen/stoffverlaufsplan_rdb_3wochen.html',
                'description' => 'Zeitliche Orientierung fuer Themen, Uebungen und SQL-Fokus.',
            ],
            [
                'title' => 'Hilfsmittel Teil B (Modellierung)',
                'href' => '/generated/anleitungen/KA02_2025_2026_VERSION1_teil-b-hilfsmittel.html',
                'description' => 'Schnelle Uebersicht fuer EERM, Kardinalitaeten und 3NF-Begruendungen.',
            ],
            [
                'title' => 'Hilfsmittel Teil C (SQL)',
                'href' => '/generated/anleitungen/KA02_2025_2026_VERSION1_teil-c-hilfsmittel.html',
                'description' => 'Nachschlagehilfe fuer SQL-Abfragen, JOINs und Aggregationen.',
            ],
        ];
    }

    /**
     * @return array<int,array<string,string>>
     */
    private function exerciseLinks(): array
    {
        $links = array_merge(
            $this->discoverUeSqlLinks(),
            $this->discoverKaLinks('aufg'),
            $this->discoverKaLinks('lsg')
        );

        if (!empty($links)) {
            return $links;
        }

        return [
            [
                'title' => 'Uebungen: SQL-Abfragen',
                'href' => '/generated/uebungen/README.md',
                'description' => 'Uebungsuebersicht fuer SQL-Abfragen ueber mehrere Tabellen.',
            ],
        ];
    }

    /**
     * @return array<int,array<string,string>>
     */
    private function discoverUeSqlLinks(): array
    {
        $paths = glob($this->generatedBasePath . '/uebungen/UE*_sql_abfragen.html') ?: [];
        sort($paths, SORT_NATURAL);

        $links = [];
        foreach ($paths as $absolutePath) {
            $fileName = basename($absolutePath, '.html');
            $title = str_replace('_', ' ', $fileName);
            $title = preg_replace('/\bUE(\d+)\b/i', 'UE$1', $title) ?? $title;

            $links[] = [
                'title' => trim($title) . ': Aufgaben',
                'href' => $this->toWebPath($absolutePath),
                'description' => 'Interaktive SQL-Uebungen mit Schritt-fuer-Schritt-Assistenz.',
            ];
        }

        return $links;
    }

    /**
     * @return array<int,array<string,string>>
     */
    private function discoverKaLinks(string $kind): array
    {
        $paths = glob($this->generatedBasePath . '/klassenarbeiten/KA*_'. $kind .'.html') ?: [];
        sort($paths, SORT_NATURAL);

        $links = [];
        foreach ($paths as $absolutePath) {
            $fileName = basename($absolutePath, '.html');
            $titleBase = str_replace('_', ' ', $fileName);
            $suffix = $kind === 'aufg' ? 'Aufgaben' : 'Loesungen';

            $links[] = [
                'title' => trim($titleBase) . ': ' . $suffix,
                'href' => $this->toWebPath($absolutePath),
                'description' => $kind === 'aufg'
                    ? 'Klassenarbeit mit trainierbarem Teil-C-SQL-Assistenten.'
                    : 'Musterloesung zur fachlichen Selbstkontrolle.',
            ];
        }

        return $links;
    }

    private function toWebPath(string $absolutePath): string
    {
        $normalized = str_replace('\\', '/', $absolutePath);
        $generatedMarker = '/generated/';
        $markerPosition = strpos($normalized, $generatedMarker);
        if ($markerPosition === false) {
            return '/generated/';
        }

        return substr($normalized, $markerPosition);
    }

    /**
     * @return array<int,array<string,string>>
     */
    private function indexLinks(): array
    {
        return [
            [
                'topic' => 'Modellierung',
                'title' => 'EERM und Grundbegriffe',
                'href' => '/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html',
            ],
            [
                'topic' => 'Normalisierung',
                'title' => '3NF und Abhaengigkeiten',
                'href' => '/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html',
            ],
            [
                'topic' => 'SQL',
                'title' => 'SQL-Klausel-Kompass',
                'href' => '/generated/informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html',
            ],
        ];
    }
}
