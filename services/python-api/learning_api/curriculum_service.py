from pathlib import Path

from .recommendations import build_recommendations
from .storage import load_curriculum_index, load_json_file


def load_curriculum_document(slug: str):
    index_data = load_curriculum_index()
    if "error" in index_data:
        return index_data

    for document in index_data.get("documents", []):
        if document.get("slug") == slug:
            document_path = Path("/app") / document["document_json"]
            curriculum_doc = load_json_file(str(document_path))
            if "error" in curriculum_doc:
                return curriculum_doc
            curriculum_doc["recommendations"] = build_recommendations(curriculum_doc.get("tag_summary", {}))
            return curriculum_doc

    return {"error": f"Lehrplan nicht gefunden: {slug}"}


def enrich_curriculum_index_documents(index_data: dict) -> dict:
    enriched_documents = []
    for document in index_data.get("documents", []):
        enriched_document = dict(document)
        enriched_document["recommendations"] = build_recommendations(document.get("tag_summary", {}))
        enriched_documents.append(enriched_document)

    return {"documents": enriched_documents}
