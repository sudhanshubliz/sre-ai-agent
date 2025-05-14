import streamlit as st
from agent.agent_runner import run_risk_agent
from agent.scoring import score_risk
from agent.feedback_loop import save_feedback
from agent.timeline_predictor import predict_timeline

st.title("Change Risk Forecast Agent")

pr_summary = st.text_area("Enter a summary of your change / PR")

if st.button("Run Analysis"):
    with st.spinner("Analyzing risk..."):
        result = run_risk_agent(pr_summary)
        score_result = score_risk(pr_summary, result)
        timeline = predict_timeline(pr_summary, result)

        st.markdown("### 🧠 Risk Forecast:")
        st.write(result)
        st.markdown("### 📊 Risk Score & Reasoning:")
        st.code(score_result)
        st.markdown("### ⏳ Timeline Prediction:")
        st.code(timeline)

        feedback = st.text_input("Was this useful? Any feedback?")
        if st.button("Submit Feedback"):
            save_feedback(pr_summary, score_result, feedback)
            st.success("Feedback saved ✅")
