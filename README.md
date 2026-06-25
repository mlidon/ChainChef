# 🚀 **FastAPI Library CRUD**  
A simple and educational CRUD application built with FastAPI, SQLite, and JWT authentication.
"Part of my personal template collection for rapid prototyping of AI-powered applications."

<p align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="180">
</p>

---

## 🏷️ **Tech Stack**

<p align="left">
  <img src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
</p>

---

## 📌 **Project Overview**

This project is a **full CRUD application** built with **FastAPI** and a lightweight **SQLite** database.  
It includes:

- User authentication with **JWT tokens**  
- CRUD operations for managing personal book collections  
- A simple **HTML + JavaScript frontend**  
- A clean, modular backend architecture  
- A fully documented learning‑oriented structure  

The goal of this project is to serve as a **learning prototype** for building real‑world FastAPI applications with authentication, routing, services, schemas, and frontend integration.

---

## ✨ **Features**

- 🔐 User registration & login  
- 🔑 JWT‑based authentication  
- 📚 CRUD for books (Create, Read, Update, Delete)  
- 🗂️ SQLite persistence  
- 🎨 Frontend with Bootstrap  
- 🔄 Fully connected frontend ↔ backend  
- 🧩 Modular architecture (routers, services, schemas, models)  

---

## 📁 **Project Structure**

```
app/
 ├── main.py
 ├── auth/
 │     └── auth.py
 ├── routers/
 │     └── book_router.py
 ├── services/
 │     └── book_service.py
 ├── schemas/
 │     └── book_schema.py
 ├── models/
 │     └── book.py
 ├── database.py
 ├── dependencies.py
frontend/
 ├── login.html
 ├── register.html
 ├── books.html
 ├── app.js
```

---

## 🚀 **How to Run the Project**

### 1. Create a virtual environment
```bash
python -m venv venv
```

### 2. Activate it
**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
uvicorn app.main:app --reload
```

### 5. Open the frontend  
Open `login.html` in your browser.

---

## 🔧 **API Endpoints**

### **Auth**
| Method | Endpoint       | Description        |
|--------|----------------|--------------------|
| POST   | `/auth/login`  | User login         |
| POST   | `/auth/register` | User registration |

### **Books**
| Method | Endpoint        | Description              |
|--------|-----------------|--------------------------|
| GET    | `/books/`       | List user books          |
| POST   | `/books/`       | Create a new book        |
| PUT    | `/books/{id}`   | Update an existing book  |
| DELETE | `/books/{id}`   | Delete a book            |

---

## 🎯 **Purpose of This Project**

This repository is part of a personal learning journey to:

- Understand FastAPI deeply  
- Build real, modular backend architectures  
- Connect frontend and backend cleanly  
- Prepare for more advanced AI‑powered applications  
- Create a solid foundation for future prototypes  

---

## 📜 **License**

MIT License — feel free to use, modify, and learn from this project.


Built by Marc Lidón — [marclidon.com](https://marclidon.com)

