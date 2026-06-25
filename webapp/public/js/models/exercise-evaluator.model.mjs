export class ExerciseEvaluatorModel {
  constructor(requiredTokens = []) {
    this.requiredTokens = requiredTokens;
  }

  evaluate(answer) {
    const normalizedAnswer = String(answer || "").trim();

    if (!normalizedAnswer) {
      return {
        state: "warning",
        message:
          "Noch keine Loesung eingetragen. Beginne mit einem fachlich begruendeten ersten Entwurf und pruefe dann gezielt Schluesselwoerter oder Begruendungen.",
      };
    }

    const upperAnswer = normalizedAnswer.toUpperCase();
    const missingTokens = this.requiredTokens.filter(
      (token) => !upperAnswer.includes(String(token).toUpperCase())
    );

    if (missingTokens.length === 0) {
      return {
        state: "success",
        message:
          "Starke Grundlage. Die geforderten Kernbausteine sind vorhanden. Pruefe jetzt noch fachlich, ob deine JOIN-Bedingungen oder Begruendungen exakt zum Sachverhalt passen und keine unnoetigen Attribute mitschwingen.",
      };
    }

    return {
      state: "warning",
      message: `Noch unvollstaendig: ${missingTokens.join(", ")}. Ergaenze diese Bausteine und verknuepfe sie mit einer fachlichen Begruendung. Arbeite schrittweise: erst Struktur, dann Praezision.`,
    };
  }
}
