from langgraph.graph import StateGraph
from typing import TypedDict

from agents.collector import collector_agent
from agents.extractor import extractor_agent
from agents.impact import impact_agent
from agents.writer import writer_agent


# 1️⃣ Define shared state (data flowing between agents)
class MarketState(TypedDict):
    topic: str
    collected: dict
    extracted: dict
    impact: dict
    final: dict


# 2️⃣ Wrap each agent so LangGraph understands it
def collector_node(state: MarketState):
    collected = collector_agent(state["topic"])
    return {"collected": collected}


def extractor_node(state: MarketState):
    extracted = extractor_agent(state["collected"])
    return {"extracted": extracted}


def impact_node(state: MarketState):
    impact = impact_agent(state["extracted"])
    return {"impact": impact}


def writer_node(state: MarketState):
    final = writer_agent(state["impact"])
    return {"final": final}


# 3️⃣ Build the graph
graph = StateGraph(MarketState)

graph.add_node("collector", collector_node)
graph.add_node("extractor", extractor_node)
graph.add_node("impact", impact_node)
graph.add_node("writer", writer_node)

# 4️⃣ Define execution order
graph.set_entry_point("collector")
graph.add_edge("collector", "extractor")
graph.add_edge("extractor", "impact")
graph.add_edge("impact", "writer")

# 5️⃣ Compile graph
market_graph = graph.compile()

# orchestration/graph.py

def run_graph(topic: str):
    """
    Orchestrates all agents in sequence
    """

    # 1️⃣ Collector Agent
    collected_data = collector_agent(topic)

    # 2️⃣ Extractor Agent
    extracted_data = extractor_agent(collected_data)

    # 3️⃣ Impact Agent
    impact_result = impact_agent(extracted_data)

    return {
        "topic": topic,
        "analysis": impact_result
    }
