from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookUpdate

def create_book(db:Session, book_data:BookCreate,owner_id:int):
    new_book=Book(
        title = book_data.title,
        author= book_data.author,
        year = book_data.year,
        image_url= book_data.image_url,
        owner_id = owner_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books_by_user(db: Session, user_id: int):
    return db.query(Book).filter(Book.owner_id == user_id).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = get_book_by_id(db, book_id)
    if not book:
        return None

    book.title = book_data.title
    book.author = book_data.author
    book.year = book_data.year
    book.image_url = book_data.image_url

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book_by_id(db, book_id)
    if not book:
        return None

    db.delete(book)
    db.commit()
    return True