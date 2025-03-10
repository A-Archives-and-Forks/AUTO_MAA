from flask import Flask, request, jsonify, abort
import json
import os
import base64

app = Flask(__name__)

data_file = "data.json"
exception_file = "exceptions.json"
image_dir = "images"

valid_task_types = {
    "LinkStart-Base", "LinkStart-WakeUp", "LinkStart-Combat", "LinkStart-Recruiting", "LinkStart-Mall",
    "LinkStart-Mission", "LinkStart-AutoRoguelike", "LinkStart-ReclamationAlgorithm",
    "CaptureImage", "LinkStart", "Toolbox-GachaOnce",
    "Settings-ConnectionAddress", "CaptureImageNow", "StopTask", "HeartBeat"
}


def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"devices": {}, "tasks": [], "reports": []}


def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_exceptions():
    if os.path.exists(exception_file):
        with open(exception_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"failed_reports": []}


def save_exceptions(data):
    with open(exception_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_image(task_id, payload):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    try:
        image_data = base64.b64decode(payload)
        image_path = os.path.join(image_dir, f"{task_id}.png")
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)
        print(f"Saved image: {image_path}")
    except Exception as e:
        print(f"Error saving image for task {task_id}: {e}")

def is_local_request():
    if request.remote_addr != "127.0.0.1" and request.remote_addr != "::1":
        abort(403, description="Access forbidden: Only local requests are allowed.")

@app.route("/maa/getTask", methods=["POST"])
def get_task():
    is_local_request()
    data = load_data()
    req = request.json
    print("Received request at /maa/getTask:", req)

    user = req.get("user")
    device = req.get("device")

    if user not in data["devices"]:
        data["devices"][user] = device
        save_data(data)

    response = {"tasks": data["tasks"]}
    print("Response:", response)
    return jsonify(response)


@app.route("/maa/reportStatus", methods=["POST"])
def report_status():
    is_local_request()
    data = load_data()
    req = request.json
    print("Received request at /maa/reportStatus:", req)

    task_id = req.get("task")
    status = req.get("status")
    payload = req.get("payload", "")

    if task_id:
        data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
        if payload:
            save_image(task_id, payload)
        if status == "FAILED":
            exceptions = load_exceptions()
            exceptions["failed_reports"].append(req)
            save_exceptions(exceptions)
            print(f"Task {task_id} failed, moved to exceptions.json")

    save_data(data)
    print("Updated tasks after reporting status")
    return jsonify({"message": "Report received"}), 200


@app.route("/maa/addTask", methods=["POST"])
def add_task():
    is_local_request()
    data = load_data()
    new_task = request.json
    print("Received request at /maa/addTask:", new_task)

    if "id" not in new_task or "type" not in new_task:
        return jsonify({"error": "Invalid task format"}), 400

    if new_task["type"] not in valid_task_types:
        return jsonify({"error": "Invalid task type"}), 400

    data["tasks"].append(new_task)
    save_data(data)
    print("Task added:", new_task)
    return jsonify({"message": "Task added successfully"}), 200


@app.route("/maa/clearTasks", methods=["POST"])
def clear_tasks():
    is_local_request()
    data = load_data()
    print("Received request at /maa/clearTasks")

    data["tasks"] = []
    save_data(data)
    print("Tasks cleared")
    return jsonify({"message": "Tasks cleared"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
