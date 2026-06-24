<?php

declare(strict_types=1);

final class StudentPortalController
{
    private LearningContentRepository $repository;

    public function __construct(LearningContentRepository $repository)
    {
        $this->repository = $repository;
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
        return [
            [
                'title' => 'UE01 Foodtrucknetz: Aufgaben',
                'href' => '/generated/uebungen/UE01_foodtrucknetz_sql_abfragen.html',
                'description' => 'SQL-Aufgaben mit Bezug auf JOIN, Filter und Auswertung.',
            ],
            [
                'title' => 'UE02 Stadtfahrradverleih: Aufgaben',
                'href' => '/generated/uebungen/UE02_stadtfahrradverleih_sql_abfragen.html',
                'description' => 'Uebungsserie fuer SELECT, GROUP BY und fachliche Interpretation.',
            ],
            [
                'title' => 'Klassenarbeit V1: Aufgaben',
                'href' => '/generated/klassenarbeiten/KA02_2025_2026_VERSION1_aufg.html',
                'description' => 'Kompletter Aufgabenblock fuer Modellierung und SQL.',
            ],
            [
                'title' => 'Klassenarbeit V1: Loesungen',
                'href' => '/generated/klassenarbeiten/KA02_2025_2026_VERSION1_lsg.html',
                'description' => 'Musterloesung zur Selbstkontrolle und Nachbereitung.',
            ],
        ];
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
