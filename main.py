from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE SETUP
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: int | None = None
    title: str
    done: bool = False

@app.get("/")
def root():
    return {"message": "Todo API is running"}

@app.get("/todos")
def get_todos():
    db = SessionLocal()
    todos = db.query(TodoDB).all()
    db.close()
    return todos

@app.post("/todos")
def create_todo(todo: Todo):
    db = SessionLocal()
    db_todo = TodoDB(title=todo.title, done=todo.done)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.close()
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    db.close()
    return {"message": "Deleted"}