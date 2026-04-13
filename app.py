import streamlit as st
from agent.simple_research import generate_report

st.title("InsightForge")

query = st.text_input("Enter your research topic:")

if st.button("Research") and query:
    with st.spinner("Researching..."):
        report, sources = generate_report(query)

    st.markdown(report)

    st.subheader("Sources")
    for s in sources:
        st.write(f"- {s['title']} ({s['url']})")