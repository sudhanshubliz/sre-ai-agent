import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables from the .env file
load_dotenv()

# Initialize the Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not set. Please set it in your .env file.")
    st.stop()

client = Groq(api_key=api_key)

FEEDBACK_FILE = "data/feedback.jsonl"
os.makedirs("data", exist_ok=True)

def analyze_change_request(change_request: str) -> dict:
    system_prompt = """
    You are a risk analysis assistant. Your task is to analyze change requests and forecast the risk level.
    Respond only with JSON using this format:
    {
        "risk_level": "low|medium|high",
        "reasoning": "Explain the reasoning behind the risk level.",
        "recommendations": ["List actionable recommendations to mitigate risks."]
    }
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": change_request}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse the response as JSON."}
    except Exception as e:
        return {"error": str(e)}

def save_feedback(change_request, result, user_feedback):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "change_request": change_request,
        "result": result,
        "user_feedback": user_feedback
    }
    with open(FEEDBACK_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    feedbacks = []
    with open(FEEDBACK_FILE, "r") as f:
        for line in f:
            try:
                feedbacks.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return feedbacks

def plot_risk_levels():
    feedbacks = load_feedback()
    if not feedbacks:
        st.info("No feedback data available to plot risk levels over time.")
        return

    # Extract timestamp and risk level
    records = []
    for fb in feedbacks:
        timestamp = fb.get("timestamp")
        risk = fb.get("result", {}).get("risk_level")
        if timestamp and risk:
            records.append({"timestamp": timestamp, "risk_level": risk})
    if not records:
        st.info("No valid risk level data to plot.")
        return

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Map risk_level to numeric values for plotting
    risk_map = {"low": 1, "medium": 2, "high": 3}
    df["risk_num"] = df["risk_level"].map(risk_map)

    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["risk_num"], marker='o')
    plt.yticks([1, 2, 3], ["Low", "Medium", "High"])
    plt.xlabel("Time")
    plt.ylabel("Risk Level")
    plt.title("Risk Level Trend Over Time (User Feedback)")
    plt.grid(True)
    st.pyplot(plt)

def fine_tune_model_with_feedback():
    # Placeholder function for training with collected feedback
    # In practice, this would:
    # - Load feedback dataset
    # - Prepare it for fine-tuning (format inputs/outputs)
    # - Run LoRA or other fine-tuning with Llama 3 model locally or in cloud
    st.info("Fine-tuning with feedback is not yet implemented.")
    # Example: print number of feedback records
    feedbacks = load_feedback()
    st.write(f"Total feedback entries available for fine-tuning: {len(feedbacks)}")

# Streamlit app code
st.title("🔮Change Risk Forecast Agentic AI with Feedback & Trends")
st.markdown("""
This tool analyzes change requests and forecasts their risk level intelligently, providing reasoning, recommendations, and explainability.

You can also provide feedback on the accuracy of the forecast and see risk trends over time.
""")

change_request = st.text_area("Enter a summary of your change request, Jenkins log, or PR details:")

if st.button("Analyze Risk"):
    if not change_request.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing the change request..."):
            result = analyze_change_request(change_request)

        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### 🧠 Risk Forecast:")
            st.write(result.get("risk_level", "N/A"))
            st.markdown("### 📋 Reasoning:")
            st.write(result.get("reasoning", "N/A"))
            st.markdown("### ✅ Recommendations:")
            recommendations = result.get("recommendations", [])
            if recommendations:
                for idx, rec in enumerate(recommendations, start=1):
                    st.markdown(f"{idx}. {rec}")
            else:
                st.write("No recommendations provided.")

            # Feedback UI
            st.markdown("---")
            st.markdown("### 📝 Feedback")
            feedback = st.radio(
                "Was the risk forecast accurate?",
                options=["Yes", "No"],
                index=0
            )
            if st.button("Submit Feedback"):
                save_feedback(change_request, result, feedback)
                st.success("Thank you for your feedback! It has been saved.")

st.markdown("---")
st.markdown("## 📊 Risk Level Trends Over Time")
plot_risk_levels()

st.markdown("---")
if st.button("Trigger Fine-Tuning with Feedback"):
    fine_tune_model_with_feedback()
