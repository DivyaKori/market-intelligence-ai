def impact_agent(extracted_data: dict):
    """
    Analyzes extracted entities and explains business impact
    """

    insights = []

    themes = extracted_data.get("entities", {}).get("themes", [])

    if not themes:
        insights.append(
            "Regulatory tightening suggests increased compliance costs for NBFCs, "
            "favoring well-capitalized players over smaller firms."
        )

    insights.append(
        "Digital lending regulations indicate stronger consumer protection, "
        "which may slow aggressive growth but improve long-term trust."
    )

    return {
        "impact_summary": insights,
        "input_data": extracted_data
    }
