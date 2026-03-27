# Mini Task Management API

## 📌 Overview

โปรเจคนี้เป็น REST API ที่พัฒนาด้วย Python Flask สำหรับจัดการ Task แบบพื้นฐาน โดยมีระบบ Login และ Authentication ด้วย JWT
สามารถใช้งานผ่าน HTTP และ Deploy บน Internet ได้จริง

---

## ⚙️ Tech Stack

* Python
* Flask
* PyJWT
* requests
* Postman (สำหรับทดสอบ API)

---

## 🚀 How to Run

### 1. Clone Project

```bash
git clone <your-repo-url>
cd mini-task-api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
python app.py
```

Server จะรันที่:

```text
http://127.0.0.1:5000
```

---

## 🔐 Authentication (JWT)

### วิธีใช้งาน

1. เรียก `POST /login` เพื่อรับ token
2. นำ token ไปใส่ใน Header ของ request อื่น

### ตัวอย่าง Header

```text
Authorization: Bearer <token>
```

---

## 📡 API Endpoints

---

### 1. Login

**POST /login**

#### Request

```json
{
  "username": "student",
  "password": "1234"
}
```

#### Response

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### 2. Get Tasks

**GET /tasks**

#### Header

```text
Authorization: Bearer <token>
```

#### Response

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Do homework",
      "status": "pending"
    }
  ]
}
```

---

### 3. Create Task

**POST /tasks**

#### Header

```text
Authorization: Bearer <token>
Content-Type: application/json
```

#### Request

```json
{
  "title": "Finish assignment",
  "status": "pending"
}
```

#### Response

```json
{
  "message": "Task created",
  "task": {
    "id": 2,
    "title": "Finish assignment",
    "status": "pending"
  }
}
```

---

### 4. External Tasks

**GET /external-tasks**

Endpoint นี้ใช้สำหรับเรียก API ของกลุ่มเพื่อน และรวมข้อมูลกับ task ของตัวเอง

#### Header

```text
Authorization: Bearer <token>
```

#### Response (ตัวอย่าง)

```json
{
  "my_tasks": [...],
  "external_tasks": [...]
}
```

#### หมายเหตุ

* ต้องใส่ URL ของเพื่อนในตัวแปร `FRIEND_API_URL` ในไฟล์ `app.py`
* หากยังไม่ได้ตั้งค่า จะเกิด error

---

## ❗ Error Handling

ระบบรองรับ error หลัก ๆ เช่น

### Missing Field

```json
{
  "error": {
    "code": 400,
    "message": "Title is required"
  }
}
```

### Unauthorized

```json
{
  "error": {
    "code": 401,
    "message": "Invalid token"
  }
}
```

### External API Error

```json
{
  "error": {
    "code": 502,
    "message": "Failed to fetch external tasks"
  }
}
```

---

## 🌐 Deployment

ระบบสามารถ Deploy บน platform เช่น:

* Render
* Railway
* PythonAnywhere

### URL (ใส่ของจริง)

```
https://your-api-url.com
```

---

## 🧪 Postman

ต้องมีไฟล์:

```
postman_collection.json
```

ใช้สำหรับ import และทดสอบ API ได้ทันที

---

## 🔗 External API (สำคัญสำหรับคนทำต่อ)

### สิ่งที่ต้องทำต่อ:

1. ใส่ URL ของเพื่อนใน:

```python
FRIEND_API_URL = "https://friend-api.com/tasks"
```

2. ทดสอบ `/external-tasks`

3. ถ้า API เพื่อนต้องใช้ JWT → ต้องเพิ่ม header ใน requests.get

---

## 📦 Project Structure

```
mini-task-api/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🎥 Video Requirement

วิดีโอต้องมี:

* อธิบายระบบ
* Demo API (login, tasks, external)
* อธิบายโค้ดสำคัญ (JWT, error, external)

---

## 👥 Team

1660902881 นายอภิรัตน์ แจ่มใส
1660903699 นายณภัทร รัตนบุรี

---

## 📝 Notes

* ใช้ JSON เท่านั้น (ห้ามใช้ form-data)
* API ต้องใช้งานได้จริง
* ต้อง Deploy ก่อนส่งงาน
* ต้องมีหลักฐานเรียก API ของเพื่อน

---
