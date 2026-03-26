from flask import Flask, request, jsonify
import jwt
import datetime
import requests
from functools import wraps
import os

app = Flask(__name__)

# CONFIG

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret")

# ใส่ URL ของกลุ่มเพื่อน
# ตัวอย่าง: FRIEND_API_URL = "https://friend-group-api.onrender.com/tasks"
FRIEND_API_URL = ""

# user สำหรับ demo login
USER_DATA = {
    "username": "student",
    "password": "1234"
}

# task เก็บแบบง่าย ๆ ในหน่วยความจำก่อน
tasks = [
    {
        "id": 1,
        "title": "Do homework",
        "status": "pending"
    }
]


# HELPER: ERROR RESPONSE
def error_response(code, message):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), code


# HELPER: JWT REQUIRED
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # ตรวจว่ามี Authorization header ไหม
        if not auth_header:
            return error_response(401, "Authorization header is missing")

        # ตรวจ format ว่าเป็น Bearer <token> ไหม
        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            return error_response(401, "Invalid authorization format")

        token = parts[1]

        try:
            decoded = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return error_response(401, "Token has expired")
        except jwt.InvalidTokenError:
            return error_response(401, "Invalid token")

        return f(*args, **kwargs)

    return decorated


# ROOT
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Mini Task Management API is running"
    }), 200


# LOGIN API
# POST /login
@app.route("/login", methods=["POST"])
def login():
    # ต้องรับ JSON เท่านั้น
    if not request.is_json:
        return error_response(400, "Only JSON is allowed")

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # เช็ค field ว่าครบไหม
    if not username:
        return error_response(400, "Username is required")

    if not password:
        return error_response(400, "Password is required")

    # เช็ค username / password
    if username != USER_DATA["username"] or password != USER_DATA["password"]:
        return error_response(401, "Invalid username or password")

    # สร้าง JWT token
    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "token": token
    }), 200


# GET /tasks
# ต้องใช้ JWT
@app.route("/tasks", methods=["GET"])
@token_required
def get_tasks():
    return jsonify({
        "tasks": tasks
    }), 200


# POST /tasks
# ใช้ JWT
@app.route("/tasks", methods=["POST"])
@token_required
def create_task():
    # ต้องรับ JSON เท่านั้น
    if not request.is_json:
        return error_response(400, "Only JSON is allowed")

    data = request.get_json()

    title = data.get("title")
    status = data.get("status")

    # เช็ค field
    if not title:
        return error_response(400, "Title is required")

    if not status:
        return error_response(400, "Status is required")

    # กัน status แปลก ๆ
    allowed_status = ["pending", "done"]
    if status not in allowed_status:
        return error_response(400, "Status must be 'pending' or 'done'")

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": status
    }

    tasks.append(new_task)

    return jsonify({
        "message": "Task created",
        "task": new_task
    }), 201


# GET /external-tasks
# เรียก API ของกลุ่มเพื่อนแล้วรวมกับ task ของเรา
@app.route("/external-tasks", methods=["GET"])
@token_required
def get_external_tasks():
    # ถ้ายังไม่ได้ใส่ URL ของเพื่อน
    if not FRIEND_API_URL:
        return error_response(500, "Friend API URL is not configured yet")

    try:
        response = requests.get(FRIEND_API_URL, timeout=5)

        # ถ้า API เพื่อนตอบกลับไม่สำเร็จ
        if response.status_code != 200:
            return error_response(502, "Failed to fetch external tasks")

        # แปลง response เป็น JSON
        external_data = response.json()

        # รองรับทั้งกรณีเพื่อนส่ง {"tasks": [...]} หรือส่ง list มาเลย
        if isinstance(external_data, dict) and "tasks" in external_data:
            external_tasks = external_data["tasks"]
        elif isinstance(external_data, list):
            external_tasks = external_data
        else:
            return error_response(502, "External API returned invalid JSON structure")

        return jsonify({
            "my_tasks": tasks,
            "external_tasks": external_tasks
        }), 200

    except requests.exceptions.RequestException:
        return error_response(502, "Could not connect to external API")
    except ValueError:
        return error_response(502, "External API did not return valid JSON")


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
