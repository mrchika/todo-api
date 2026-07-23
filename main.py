from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Todo API")

# Database setup
conn = sqlite3.connect("todos.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, title TEXT, done INTEGER)")

class Todo(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def root():
    return {"message": "Todo API is running"}

@app.get("/todos")
def get_todos():
    cur = conn.execute("SELECT * FROM todos")
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in cur.fetchall()]

@app.post("/todos")
def create_todo(todo: Todo):
    cur = conn.execute("INSERT INTO todos (title, done) VALUES (?,?)", (todo.title, int(todo.done)))
    conn.commit()
    return {"id": cur.lastrowid, "title": todo.title, "done": todo.done}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows any website to call your API
    allow_methods=["*"],
    allow_headers=["*"],
)