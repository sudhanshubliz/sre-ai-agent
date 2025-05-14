import streamlit as st
from agent.agent_runner import run_risk_agent

st.title("Change Risk Forecasting Agent")
pr_summary = st.text_area("Enter a summary of your change / PR")

if st.button("Run Analysis"):
    with st.spinner("Analyzing risk..."):
        result = run_risk_agent(pr_summary)
        st.markdown("### 🧠 Risk Forecast:")
        st.write(result)
