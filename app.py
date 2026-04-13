import streamlit as st
from agent.graph import build_graph

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightForge",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:        #0e0d0b;
    --surface:   #161411;
    --surface-2: #1d1a16;
    --border:    #2a2520;
    --border-2:  #332e28;
    --ink:       #f0ece4;
    --ink-2:     #a8a098;
    --ink-3:     #5a5450;
    --accent:    #d4581a;
    --accent-dim: rgba(212, 88, 26, 0.12);
    --accent-glow: rgba(212, 88, 26, 0.06);
    --green:     #3ab870;
    --green-dim: rgba(58, 184, 112, 0.12);
    --mono:      'JetBrains Mono', monospace;
    --serif:     'Instrument Serif', Georgia, serif;
    --sans:      'Outfit', sans-serif;
}

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: var(--bg) !important;
    font-family: var(--sans) !important;
    color: var(--ink) !important;
}

[data-testid="block-container"] {
    padding: 3.5rem 1.5rem 5rem !important;
    max-width: 760px !important;
    margin: 0 auto !important;
}

/* ── Hide chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }

/* ── Labels ── */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
    font-family: var(--sans) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: var(--ink-3) !important;
    margin-bottom: 0.3rem !important;
}

/* ── Query input ── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: var(--sans) !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-dim) !important;
    outline: none !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: var(--ink-3) !important;
    font-weight: 300 !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: var(--sans) !important;
    font-weight: 400 !important;
}

[data-testid="stSelectbox"] svg { fill: var(--ink-3) !important; }

/* selectbox dropdown */
[data-baseweb="popover"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: 8px !important;
}

[data-baseweb="menu"] {
    background: var(--surface-2) !important;
}

[role="option"] {
    background: var(--surface-2) !important;
    color: var(--ink) !important;
    font-family: var(--sans) !important;
}

[role="option"]:hover {
    background: var(--border) !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.72rem 1.6rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: filter 0.15s, transform 0.1s !important;
}

[data-testid="stButton"] > button:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
    filter: brightness(0.95) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #443e38; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _log_html(logs: list[str], live: bool) -> str:
    if not logs:
        return ""

    rows = ""
    for i, msg in enumerate(logs):
        is_last = i == len(logs) - 1

        if not live or not is_last:
            dot = (
                '<span style="width:8px;height:8px;border-radius:50%;'
                'background:var(--green);flex-shrink:0;margin-top:4px;'
                'display:inline-block;box-shadow:0 0 6px rgba(58,184,112,0.3);"></span>'
            )
            text_col = "var(--ink-2)"
        else:
            dot = (
                '<span style="width:8px;height:8px;border-radius:50%;'
                'background:var(--accent);flex-shrink:0;margin-top:4px;'
                'display:inline-block;'
                'animation:pulse 1.2s ease-in-out infinite;"></span>'
            )
            text_col = "var(--ink)"

        show_line = "block" if i < len(logs) - 1 else "none"
        connector = (
            f'<span style="width:1px;background:var(--border-2);'
            f'flex-shrink:0;margin:3px 3.5px 3px;min-height:10px;'
            f'display:{show_line};"></span>'
        )

        rows += f"""
<div style="display:flex;gap:0.9rem;align-items:flex-start;">
    <div style="display:flex;flex-direction:column;align-items:center;padding-top:2px;">
        {dot}
        {connector}
    </div>
    <p style="font-family:var(--mono);font-size:0.78rem;color:{text_col};
              line-height:1.65;margin:0 0 0.55rem;padding-bottom:0.25rem;">{msg}</p>
</div>"""

    header_color = "var(--accent)" if live else "var(--green)"
    status_dot   = "⬤" if live else "✓"
    status_text  = "Agent activity" if live else "Completed"

    return f"""
<style>
@keyframes pulse {{
    0%,100% {{ box-shadow: 0 0 0 3px rgba(212,88,26,0.2), 0 0 8px rgba(212,88,26,0.1); }}
    50%      {{ box-shadow: 0 0 0 6px rgba(212,88,26,0.06), 0 0 14px rgba(212,88,26,0.06); }}
}}
</style>
<div style="background:var(--surface);border:1px solid var(--border-2);
            border-radius:10px;padding:1.4rem 1.5rem 0.9rem;margin-bottom:1.6rem;">
    <p style="font-family:var(--sans);font-size:0.72rem;font-weight:600;
              letter-spacing:0.07em;text-transform:uppercase;margin:0 0 1.2rem;
              color:{header_color};">{status_dot} &nbsp;{status_text}</p>
    {rows}
</div>"""


def _report_html(report_md: str) -> str:
    return f"""
<style>
.rpt {{ color:var(--ink-2);line-height:1.82;font-size:0.96rem;font-family:var(--sans); }}
.rpt h1,.rpt h2,.rpt h3 {{
    font-family:var(--serif) !important;
    color:var(--ink) !important;
    font-weight:400 !important;
    margin-top:1.6rem !important;
    letter-spacing:-0.01em !important;
}}
.rpt h1 {{ font-size:1.9rem !important; margin-top:0 !important; font-style:italic; }}
.rpt h2 {{ font-size:1.45rem !important; }}
.rpt h3 {{ font-size:1.15rem !important; }}
.rpt p  {{ margin:0 0 1rem !important; }}
.rpt a  {{ color:var(--accent) !important; text-underline-offset:3px; }}
.rpt strong {{ color:var(--ink) !important; font-weight:600 !important; }}
.rpt code {{
    font-family:var(--mono) !important;
    font-size:0.82rem !important;
    background:var(--surface-2) !important;
    padding:0.1em 0.4em !important;
    border-radius:4px !important;
    color:var(--ink) !important;
    border:1px solid var(--border-2) !important;
}}
.rpt blockquote {{
    border-left:2px solid var(--accent);
    margin:1rem 0;
    padding:0.5rem 1rem;
    background:var(--accent-dim);
    border-radius:0 6px 6px 0;
    color:var(--ink-2);
}}
.rpt ul,.rpt ol {{ padding-left:1.4rem;margin:0 0 1rem; }}
.rpt li {{ margin-bottom:0.35rem; }}
.rpt hr {{ border:none;border-top:1px solid var(--border-2);margin:1.4rem 0; }}
</style>
<div style="background:var(--surface);border:1px solid var(--border-2);
            border-radius:10px;padding:2rem 2.2rem;margin-bottom:1.6rem;">
    <p style="font-family:var(--sans);font-size:0.72rem;font-weight:600;
              letter-spacing:0.07em;text-transform:uppercase;
              color:var(--ink-3);margin:0 0 1.4rem;">Research Report</p>
    <div class="rpt">{report_md}</div>
</div>"""


def _sources_html(sources: list[dict]) -> str:
    items = ""
    for i, s in enumerate(sources):
        border = "border-bottom:none;" if i == len(sources) - 1 else ""
        items += f"""
<div style="display:flex;gap:1rem;align-items:baseline;
            padding:0.72rem 0;border-bottom:1px solid var(--border);{border}">
    <span style="font-family:var(--mono);font-size:0.7rem;color:var(--accent);
                 background:var(--accent-dim);border-radius:4px;
                 padding:0.15rem 0.5rem;flex-shrink:0;font-weight:500;">{s['id']}</span>
    <a href="{s['url']}" target="_blank"
       style="font-size:0.87rem;color:var(--ink-2);text-decoration:none;
              line-height:1.5;transition:color 0.15s;"
       onmouseover="this.style.color='var(--ink)'"
       onmouseout="this.style.color='var(--ink-2)'">{s['title']}</a>
</div>"""

    return f"""
<div style="background:var(--surface);border:1px solid var(--border-2);
            border-radius:10px;padding:1.6rem 1.8rem;">
    <p style="font-family:var(--sans);font-size:0.72rem;font-weight:600;
              letter-spacing:0.07em;text-transform:uppercase;
              color:var(--ink-3);margin:0 0 0.3rem;">Sources</p>
    {items}
</div>"""


# ── Layout ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero {
    text-align: center;
    padding-bottom: 2.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.2rem;
}
.hero-wordmark {
    font-family: var(--serif);
    font-size: 2.8rem;
    font-style: italic;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 0.6rem;
}
.hero-wordmark span {
    color: var(--accent);
    font-style: normal;
}
.hero-sub {
    font-size: 0.8rem;
    color: var(--ink-3);
    font-weight: 400;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}
</style>
<div class="hero">
    <div class="hero-wordmark">Insight<span>Forge</span></div>
    <div class="hero-sub">Agentic research &nbsp;·&nbsp; Powered by AI</div>
</div>
""", unsafe_allow_html=True)

query = st.text_input(
    "Research topic",
    placeholder="e.g. How does RAG work in production systems?",
)

col_depth, col_gap, col_btn = st.columns([1, 0.1, 1.8])
with col_depth:
    depth = st.selectbox("Depth", ["basic", "deep"])
with col_btn:
    st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
    run = st.button("Run Research →")

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ── Run ────────────────────────────────────────────────────────────────────────
if run and query:
    graph = build_graph()

    log_ph    = st.empty()
    report_ph = st.empty()
    src_ph    = st.empty()

    logs: list[str] = []
    final_state = None

    with st.spinner(""):
        for step in graph.stream({
            "query":     query,
            "logs":      [],
            "iteration": 0,
            "depth":     depth,
        }):
            for _, state in step.items():
                final_state = state
                if "logs" in state:
                    logs = state["logs"]
                log_ph.markdown(_log_html(logs, live=True), unsafe_allow_html=True)

    log_ph.markdown(_log_html(logs, live=False), unsafe_allow_html=True)

    if final_state:
        if final_state.get("report"):
            report_ph.markdown(
                _report_html(final_state["report"]),
                unsafe_allow_html=True,
            )
        if final_state.get("sources"):
            src_ph.markdown(
                _sources_html(final_state["sources"]),
                unsafe_allow_html=True,
            )