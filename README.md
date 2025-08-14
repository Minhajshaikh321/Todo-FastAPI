# FastAPI Todo App 📝

A simple **Todo CRUD API** built with **FastAPI** and **SQLAlchemy**, created to practice and improve FastAPI skills.

---
## 1️⃣ Features and project structure

- Create a new Todo
- Get all Todos
- Get Todo by ID
- Update a Todo (partial or full)
- Delete a Todo
- SQLite database for simplicity

## 📂 Project Structure
│── app.py # Main FastAPI application

│── database.db # SQLite database file (auto-generated)

│── requirements.txt # Python dependencies

│── README.md # Project documentation

2️⃣ Create virtual environment & activate it
python -m venv venv
venv\Scripts\activate

## ⚙️ Tech Stack
- **FastAPI** - API framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **SQLite** - Database

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Run the application

uvicorn app:app --reload

## 📚 Learning Goals

1)Understanding FastAPI request/response flow

2)Using Pydantic models for validation

3)Working with SQLAlchemy ORM

4)Handling CRUD operations

5)Returning proper HTTP status codes & exceptions

5️⃣ Access Swagger UI
Swagger UI is an interactive API documentation that FastAPI provides by default.  
It allows you to test all endpoints directly in your browser without needing Postman.

**URL:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Can execute API requests (GET, POST, PUT, DELETE) and view responses in real time.
