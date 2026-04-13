import streamlit as st

st.title("InsightForge")

query = st.text_input("Enter your research topic:")

if st.button("Research"):
    st.write(f"Researching: {query}")