def writer_agent(impact_data: dict) -> dict:
    """
    Converts analysis into final required JSON schema
    """

    return {
        "summary": impact_data.get("summary", "Executive overview of recent market developments."),

        "drivers": impact_data.get("drivers", [
            "Regulatory tightening",
            "Increased compliance requirements"
        ]),

        "competitors": impact_data.get("competitors", [
            "Bajaj Finance",
            "HDFC Ltd",
            "Shriram Finance",
            "Muthoot Finance",
            "Manappuram Finance"
        ]),

        "impact_radar": impact_data.get("impact_radar", [
            {
                "event": "RBI releases new NBFC compliance guidelines",
                "impact_level": "High",
                "score": 85,
                "why": [
                    "Direct increase in compliance cost",
                    "Mandatory operational changes"
                ],
                "actions": [
                    "Conduct internal audit",
                    "Update compliance workflows"
                ],
                "url": "https://rbi.org.in"
            }
        ]),

        "opportunities": impact_data.get("opportunities", [
            "Consolidation of smaller NBFCs",
            "Growth in compliance-tech solutions",
            "Stronger customer trust",
            "Improved risk profiling",
            "Digital governance tools"
        ]),

        "risks": impact_data.get("risks", [
            "Higher operational costs",
            "Delayed product launches",
            "Regulatory penalties",
            "Liquidity stress",
            "Reduced short-term growth"
        ]),

        "90_day_plan": {
            "0_30": [
                "Review regulatory changes",
                "Assign compliance owners"
            ],
            "30_60": [
                "Update internal processes",
                "Train staff on new norms"
            ],
            "60_90": [
                "Automate compliance checks",
                "Engage external auditors"
            ]
        },

        "sources": impact_data.get("sources", [
            "https://rbi.org.in",
            "https://sebi.gov.in"
        ])
    }
