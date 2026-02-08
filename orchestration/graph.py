from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from agents.collector import collector_agent
from agents.extractor import extractor_agent
from agents.impact import impact_agent
from agents.writer import writer_agent


# =====================================================
# 1️⃣ Shared State Definition
# =====================================================

class MarketState(TypedDict, total=False):
    topic: str
    collected: Dict[str, Any]
    extracted: Dict[str, Any]
    impact: Dict[str, Any]
    final: Dict[str, Any]


# ======================================================
# 2️⃣ LangGraph Nodes (each wraps ONE agent)
# =========================================================

def collector_node(state: MarketState) -> MarketState:
    collected = collector_agent(state["topic"])
    return {"collected": collected}


def extractor_node(state: MarketState) -> MarketState:
    extracted = extractor_agent(state["collected"])
    return {"extracted": extracted}


def impact_node(state: MarketState) -> MarketState:
    impact = impact_agent(state["extracted"])
    return {"impact": impact}


def writer_node(state: MarketState) -> MarketState:
    final_report = writer_agent(state["impact"])
    return {"final": final_report}


# =========================================================
# 3️⃣ Build the LangGraph
# =========================================================

graph = StateGraph(MarketState)

graph.add_node("collector", collector_node)
graph.add_node("extractor", extractor_node)
graph.add_node("impact", impact_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("collector")

graph.add_edge("collector", "extractor")
graph.add_edge("extractor", "impact")
graph.add_edge("impact", "writer")
graph.add_edge("writer", END)

market_graph = graph.compile()


# =========================================================
# 4️⃣ Public Runner (USED BY FastAPI / app.py)
# =========================================================

def run_graph(topic: str) -> Dict[str, Any]:
    """
    Executes the full Agentic Market Intelligence pipeline
    using LangGraph orchestration.
    """

    initial_state: MarketState = {"topic": topic}

    result = market_graph.invoke(initial_state)

    return {
        "topic": topic,
        "report": result.get("final"),
        "debug": {
            "collected": result.get("collected"),
            "extracted": result.get("extracted"),
            "impact": result.get("impact"),
        }
    }
