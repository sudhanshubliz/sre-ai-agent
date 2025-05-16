from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configure OpenAI API Key
openai.api_key = "your_openai_api_key"

@app.route('/analyze-risk', methods=['POST'])
def analyze_risk():
    """
    Analyze the risk of a given description using AI.

    Input:
        JSON payload containing the 'description'.

    Output:
        JSON response with 'risk_score', 'reasons', and 'recommendations'.
    """
    try:
        data = request.get_json()
        description = data.get("description")

        if not description:
            return jsonify({"error": "Description is required"}), 400

        # Use OpenAI API to analyze the description
        prompt = (
            f"Analyze the following description for risks:\n\n"
            f"{description}\n\n"
            f"Provide a risk score (low, medium, high), reasons for the score, "
            f"and recommendations to mitigate the risks."
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )

        # Parse the AI response
        analysis = response.choices[0].text.strip()

        # Return the analysis as JSON
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)