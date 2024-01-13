from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


from sqlalchemy.orm import Session
from data_base import crud, models, schemas
from data_base.db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

# Залежність
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Статичні файли
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблони
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": authors})


@app.get("/authors/add")
def get_form_add_author(request: Request):
    return templates.TemplateResponse("add_author.html", {"request": request})

@app.post("/authors/add", response_model=schemas.Author)
def create_author(author: str = Form(), db: Session = Depends(get_db), request: Request = None):
    
    crud.create_author(db=db, author=author)

    return RedirectResponse("/", status_code=303)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/tracks/", response_model=schemas.Track)
def create_track_for_author(author_id: int, track: schemas.TrackCreate, db: Session = Depends(get_db)):
    return crud.create_author_track(db=db, track=track, author_id=author_id)


@app.get("/tracks/{author_id}", response_model=list[schemas.Track])
def read_tracks(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), author_id: int = None):
    tracks = crud.get_tracks(db, author_id, skip=skip, limit=limit)
    return templates.TemplateResponse("tracks.html", {"request": request, "tracks": tracks})
