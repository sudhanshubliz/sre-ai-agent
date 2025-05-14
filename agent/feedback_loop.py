import json
import os

def save_feedback(summary, score, user_feedback):
    feedback_path = "data/feedback.json"
    feedback = {
        "summary": summary,
        "score": score,
        "user_feedback": user_feedback
    }
    os.makedirs("data", exist_ok=True)
    if os.path.exists(feedback_path):
        data = json.load(open(feedback_path))
    else:
        data = []
    data.append(feedback)
    json.dump(data, open(feedback_path, "w"), indent=2)
