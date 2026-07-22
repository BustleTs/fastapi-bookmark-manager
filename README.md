# FastAPI Bookmark & Note Manager API

A high-performance RESTful backend service built with **FastAPI** and **SQLite**. This API provides structured CRUD functionality for managing web bookmarks, complete with data validation and dynamic endpoint documentation.

---

## Key Features

- **CRUD Operations:** Create, retrieve, filter, and delete user bookmarks.
- **Data Validation:** Enforces strict data structure schemas using **Pydantic**.
- **Database Persistence:** Stores records locally using SQLite via standard `sqlite3` library bindings.
- **Interactive API Docs:** Automatic Swagger UI endpoint docs generated at `/docs`.

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check route |
| `POST` | `/bookmarks` | Create a new bookmark entry |
| `GET` | `/bookmarks` | Retrieve all bookmarks (optional `?category=` filter) |
| `DELETE` | `/bookmarks/{id}` | Delete a specific bookmark entry |

---

## Getting Started

### Prerequisites
- Python 3.8+

### Installation & Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/fastapi-bookmark-manager.git](https://github.com/YOUR_USERNAME/fastapi-bookmark-manager.git)
   cd fastapi-bookmark-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser to `http://127.0.0.1:8000/docs` to test the endpoints interactively via Swagger UI.
