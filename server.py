import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import json
from tavily import TavilyClient

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

tavily_client = TavilyClient(os.environ.get("TAVILY_API_KEY"))

@app.route("/")
def home():
     return render_template("index.html")

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


@app.route("/prioritize", methods=["POST"])
def prioritize():
    data = request.get_json()
    get_tasks = data.get("tasks", [])

    response = client.chat.completions.create(
        model="nvidia/Nemotron-3_5-Lightning",
        messages=[
            {
                "role": "system",
                "content": "You are a productivity assistant that helps prioritize "
                "Respond with ONLY a valid JSON object. Do not include any explanation, markdown formatting or text outside the JSON."
                "tasks and identify scheduling conflicts. Order tasks primarily by urgency"
                "and any deadline/time references in the task text as secondary signals. "
                "A conflict exists when two or more tasks reference overlapping or same-day timing,"
                "or when completing one task would reasonably prevent completing another on time."
                "Fields: ordered_tasks (array of objects, in priority order, where each object has exactly "
                "these fields copied from the input data: task, urgency, category), conflicts "
                "(array of short strings describing each conflict, empty array if none),"
                "summary (one or two sentence overview). If there are no conflicts, return an empty"
                "array for conflicts. Do no invent conflicts that aren't supported by the task data."
            },
            {
                "role": "user",
                "content": "Here is the list of sorted tasks with urgency and category: " + json.dumps(get_tasks)
            }
        ]
    )

    return jsonify({"result": response.choices[0].message.content})


@app.route("/search-context", methods=["POST"])
def search_context():
    data = request.get_json()
    receive_task = data.get("task", "")

    response = tavily_client.search(
        query=receive_task,
        search_depth="basic"
    )

    if not response["results"]:
            return jsonify({
                "title": "",
                "url": "",
                "content": "No results found."
            })

    top_result = response["results"][0]
    context_text = top_result["content"][:300]

    return jsonify({
        "title": top_result["title"],
        "url": top_result["url"],
        "content": context_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)