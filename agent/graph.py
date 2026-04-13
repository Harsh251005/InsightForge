from agent.nodes import *
from langgraph.graph import StateGraph, END
from agent.state import ResearchState


def build_graph():

    builder = StateGraph(ResearchState)

    builder.add_node("decomposer", decomposer_node)
    builder.add_node("search", search_node)
    builder.add_node("filter", filter_node)
    builder.add_node("report", report_node)

    builder.set_entry_point("decomposer")

    builder.add_edge("decomposer", "search")
    builder.add_edge("search", "filter")
    builder.add_edge("filter", "report")
    builder.add_edge("report", END)

    return builder.compile()