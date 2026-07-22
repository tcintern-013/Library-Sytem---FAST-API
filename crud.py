from sqlalchemy.orm import Session
from models import Book


def get_books(db: Session):
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, title: str, author: str):
    book = get_book(db, book_id)

    if not book:
        return None

    book.title = title
    book.author = author

    db.commit()
    db.refresh(book)

    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)

    if not book:
        return None

    db.delete(book)
    db.commit()

    return book