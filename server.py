import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

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

if __name__ == "__main__":
    app.run(debug=True, port=5500)