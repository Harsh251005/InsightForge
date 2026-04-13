from langgraph.graph import StateGraph, END
from agent.state import ResearchState

from agent.nodes import (
    decomposer_node,
    search_node,
    ranking_node,
    report_node
)

def build_graph():
    builder = StateGraph(ResearchState)

    # Add nodes
    builder.add_node("decomposer", decomposer_node)
    builder.add_node("search", search_node)
    builder.add_node("ranking", ranking_node)
    builder.add_node("report", report_node)

    # Define entry point
    builder.set_entry_point("decomposer")

    # Define edges (flow)
    builder.add_edge("decomposer", "search")
    builder.add_edge("search", "ranking")
    builder.add_edge("ranking", "report")
    builder.add_edge("report", END)

    # Compile graph
    return builder.compile()