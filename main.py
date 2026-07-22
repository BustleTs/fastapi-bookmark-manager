"""
FastAPI Personal Bookmark & Note Manager
Author: Your Name
Description: A RESTful API providing CRUD operations for web bookmarks,
             persisting data in a local SQLite database.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
import sqlite3

app = FastAPI(
    title="Bookmark Manager API",
    description="REST API for saving, categorizing, and searching web bookmarks.",
    version="1.0.0",
)

DB_FILE = "bookmarks.db"


def init_db():
    """Initializes the SQLite database table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                notes TEXT
            )
            """
        )
        conn.commit()


# Initialize database on startup
init_db()


# Pydantic models for request/response validation
class BookmarkCreate(BaseModel):
    title: str
    url: str
    category: Optional[str] = "General"
    notes: Optional[str] = None


class Bookmark(BookmarkCreate):
    id: int


@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "message": "Bookmark Manager API is running"}


@app.post("/bookmarks", response_model=Bookmark, status_code=201, tags=["Bookmarks"])
def create_bookmark(bookmark: BookmarkCreate):
    """Create a new bookmark."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookmarks (title, url, category, notes) VALUES (?, ?, ?, ?)",
            (bookmark.title, bookmark.url, bookmark.category, bookmark.notes),
        )
        conn.commit()
        new_id = cursor.lastrowid

    return Bookmark(id=new_id, **bookmark.model_dump())


@app.get("/bookmarks", response_model=List[Bookmark], tags=["Bookmarks"])
def get_bookmarks(category: Optional[str] = None):
    """Retrieve all bookmarks, with optional category filtering."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if category:
            cursor.execute("SELECT * FROM bookmarks WHERE category = ?", (category,))
        else:
            cursor.execute("SELECT * FROM bookmarks")
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


@app.delete("/bookmarks/{bookmark_id}", status_code=204, tags=["Bookmarks"])
def delete_bookmark(bookmark_id: int):
    """Delete a bookmark by ID."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bookmark not found")
    return None
