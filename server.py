import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

@app.route("/triage", methods=["POST"])
def triage():
    data = request.get_json()
    text = data.get("text", "")

    response = client.chat.completions.create(
        model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        messages=[
            {
                "role": "system",
                "content": "Split this text into a JSON array of individual tasks. Respond with JSON only."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return jsonify({"result": response.choices[0].message.content})

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    tasks = data.get("tasks", [])

    response = client.chat.completions.create(
        model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        messages=[
            {
                "role": "system",
                "content": "Respond with ONLY a valid JSON array. Do not "
                "include any explanation, markdown formatting or text outside the JSON."
                "Each object in the array must have exactly these fields: task "
                "(string, the original task text), urgency (one of: 'high', 'medium', 'low'),"
                "category (one of: 'work', 'personal', 'health', 'other'). Infer urgency from any "
                "deadlines, time pressure, or tone in the task text. If no urgency is indicated, "
                "default to 'medium'."
            },
            {
                "role": "user",
                "content": "Here is the list of tasks: " + json.dumps(tasks)
            }
        ]
    )

    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True, port=5500)