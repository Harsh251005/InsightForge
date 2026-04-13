from langgraph.graph import StateGraph, END
from agent.state import ResearchState

from agent.nodes import (
    decomposer_node,
    search_node,
    ranking_node,
    report_node,
    reflection_node,
    expand_query_node
)


def build_graph():
    builder = StateGraph(ResearchState)

    # Nodes
    builder.add_node("decomposer", decomposer_node)
    builder.add_node("search", search_node)
    builder.add_node("ranking", ranking_node)
    builder.add_node("reflection", reflection_node)
    builder.add_node("expand", expand_query_node)
    builder.add_node("report", report_node)

    # Entry
    builder.set_entry_point("decomposer")

    # Flow
    builder.add_edge("decomposer", "search")
    builder.add_edge("search", "ranking")
    builder.add_edge("ranking", "reflection")

    # Conditional branching
    def should_continue(state):
        # BASIC mode → skip reflection loop
        if state.get("depth") == "basic":
            return "report"

        # DEEP mode → allow reflection
        if state["need_more_research"] and state["iteration"] < 2:
            return "expand"

        return "report"

    builder.add_conditional_edges(
        "reflection",
        should_continue,
        {
            "expand": "expand",
            "report": "report"
        }
    )

    # Loop back
    builder.add_edge("expand", "search")

    builder.add_edge("report", END)

    return builder.compile()