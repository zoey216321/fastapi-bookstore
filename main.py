from typing import Union
from fastapi import FastAPI , HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class BOOK(BaseModel):
    titles: str
    price: float
    genre: Literal["fiction","non-fiction"]
    book_id: Optional[str] = uuid4().hex

BOOKSFILE = "books.json"

BOOKBASE=[]

if os.path.exists(BOOKSFILE):
    with open (BOOKSFILE,"r") as f:
        BOOKBASE = json.load(f)

@app.get("/")
async def home():
    return {"Message": "Welcome to my bookstore!"}

@app.get("/List_books")
async def list_books():
    return {"Books": BOOKBASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index:int):
    if index < 0 or index >= len(BOOKBASE):
        raise HTTPException(404,f" Your index {index} is out of range {len(BOOKBASE)} ")
    else:
        return {"book":BOOKBASE[index]}

@app.get("/get-random-book")
async def get_random_book():
    book = random.choice(BOOKBASE) 
    return {"book":book}

@app.post("/add-book")
async def add_book(book: BOOK):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKBASE.append(json_book)
    with open (BOOKSFILE,"w") as f:
        json.dump(BOOKBASE,f)
    return {"Messages": f"{json_book} was added","book_id": f"book_id was {book.book_id}."}

@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOKBASE:
        if book["book_id"] == book_id:
            return book
    raise HTTPException(404,f" Your book is not found ")


