import streamlit as st
from agent.graph import build_graph

graph = build_graph()

st.title("InsightForge")

query = st.text_input("Enter your research topic:")

if st.button("Research") and query:
    with st.spinner("Researching..."):
        result = graph.invoke({"query": query})

    st.markdown(result["report"])

    st.subheader("Sources")
    for s in result["filtered_results"]:
        st.write(f"- {s['title']} ({s['url']})")