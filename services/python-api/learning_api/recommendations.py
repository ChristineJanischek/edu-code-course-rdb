def build_recommendations(tag_summary: dict):
    recommendations = []

    if tag_summary.get("eerm", 0):
        recommendations.append(
            {
                "type": "learning-path",
                "title": "EERM vom Sachverhalt ableiten",
                "summary": "Starte mit fachlichen Objekten, Kardinalitaeten und Schluesselbeziehungen und sichere die Modellierung mit einem Begruendungsschritt ab.",
            }
        )
    if tag_summary.get("normalisierung", 0) or tag_summary.get("datenintegritaet", 0):
        recommendations.append(
            {
                "type": "exercise",
                "title": "3NF begruenden",
                "summary": "Ergaenze Uebungen, in denen Lernende Redundanzen erkennen, funktionale Abhaengigkeiten benennen und ihr Zielmodell fachlich begruenden.",
            }
        )
    if tag_summary.get("sql-select", 0) or tag_summary.get("sql-join", 0) or tag_summary.get("sql-group-by", 0):
        recommendations.append(
            {
                "type": "practice",
                "title": "SQL stufenweise trainieren",
                "summary": "Baue Aufgabenketten von einfacher SELECT-Abfrage ueber JOIN bis zu Aggregation und fachlicher Auswertung auf.",
            }
        )
    if tag_summary.get("begruendung", 0):
        recommendations.append(
            {
                "type": "feedback",
                "title": "Begruendung explizit einfordern",
                "summary": "Selbstkontrolle und Musterloesung sollen nicht nur Syntax, sondern auch fachliche Entscheidungen und Modellkritik sichtbar machen.",
            }
        )

    return recommendations
