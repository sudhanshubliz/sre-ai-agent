import streamlit as st
import os
import json
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_change_request(change_request: str) -> dict:
    """
    Analyze a change request using Groq's Chat Completions API.

    Parameters:
        change_request (str): Description of the change request.

    Returns:
        dict: Structured response containing risk level, reasoning, and recommendations.
    """
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

# Streamlit app code
st.title("Change Risk Forecast Agent")
st.markdown("""
This tool analyzes change requests and forecasts their risk level intelligently, providing reasoning, recommendations, and explainability.
""")

# Text area for user input
change_request = st.text_area("Enter a summary of your change request or PR:")

if st.button("Analyze Risk"):
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