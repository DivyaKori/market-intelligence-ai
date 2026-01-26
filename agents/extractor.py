from mcp_server import tools

def extractor_agent(collected_data: dict):
    """
    Takes collector output and extracts structured entities
    """

    raw_data = tools.fetch_url("dummy_url")

    # 🔑 THIS LINE IS CRITICAL
    raw_text = str(raw_data)

    clean_text = tools.clean_extract(raw_text)
    entities = tools.extract_entities(clean_text)

    return {
        "entities": entities,
        "source_data": collected_data
    }