from typing import List, Dict
from typing_extensions import TypedDict


class ResearchState(TypedDict):
    query: str
    sub_queries: List[str]
    results: List[Dict]
    filtered_results: List[Dict]
    report: str
    sources: List[Dict]
    iteration: int
    need_more_research: bool
    logs: List[str]
    depth: str