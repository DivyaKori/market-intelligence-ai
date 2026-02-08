from mcp_server import tools
from utils.logger import logger

def extractor_agent(collected_data: dict) -> dict:
    """
    Extractor Agent
    - Extracts entities & themes
    """

    logger.info("[Extractor] Started")

    documents = collected_data.get("documents", [])

    themes = []
    competitors = []
    extracted_docs = []

    for doc in documents:
        text = doc.get("content", "")
        entities = tools.extract_entities(text)

        extracted_docs.append({
            "url": doc.get("url"),
            "entities": entities
        })

        themes.extend(entities.get("themes", []))
        competitors.extend(entities.get("competitors", []))

    logger.info("[Extractor] Entity extraction completed")

    return {
        "topic": collected_data.get("topic"),
        "themes": tools.dedupe_items(themes),
        "competitors": tools.dedupe_items(competitors),
        "documents": extracted_docs
    }
