from langchain_ollama import ChatOllama
from mcp_server import tools
import trafilatura

llm = ChatOllama(model="llama3")

def collector_agent(topic: str):
    """
    Collects market signals for a given topic
    """
    prompt = f"""
    You are a market intelligence collector agent.
    Find recent important developments related to: {topic}.
    """
    
    response = llm.invoke(prompt)

    # Agent decides to call tool
    results = tools.search_web(topic)

    return {
        "thought": response.content,
        "signals": results
    }
