from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services.book_service import (
    create_book, get_books_by_user, get_book_by_id,
    update_book, delete_book
)
from app.dependencies import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse)
def create_new_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_book(db, book_data, current_user.id)


@router.get("/", response_model=list[BookResponse])
def list_books(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_books_by_user(db, current_user.id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book_data(
    book_id: int,
    book_data: BookUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    book = get_book_by_id(db, book_id)
    if not book or book.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    updated = update_book(db, book_id, book_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return updated


@router.delete("/{book_id}")
def delete_book_data(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    book = get_book_by_id(db, book_id)
    if not book or book.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    delete_book(db, book_id)
    return {"message": "Libro eliminado"}
