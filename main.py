from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from auth import (
    Token,
    UserCreate,
    UserLogin,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    users_db,
)
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to the Book API"}


@app.post("/signup", status_code=201)
def signup(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_db[user.username] = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
    }

    return {"message": "User created successfully", "username": user.username}


@app.post("/login", response_model=Token)
def login(user: UserLogin):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": authenticated_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}


@app.post("/books", response_model=schemas.BookResponse, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing = crud.get_book(db, book.id)

    if existing:
        existing.title = book.title
        existing.author = book.author
        db.commit()
        db.refresh(existing)
        return existing

    new_book = models.Book(**book.model_dump())
    return crud.create_book(db, new_book)


@app.get("/books", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id, book.title, book.author)

    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}
