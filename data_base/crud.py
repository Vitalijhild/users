from sqlalchemy.orm import Session
from . import models, schemas

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name)
    
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_tracks(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    if not author_id:
        tracks = db.query(models.Track).offset(skip).limit(limit).all()
    else:
        tracks = db.query(models.Track).filter(models.Track.author_id == author_id).all()

    return tracks


def create_author_track(db: Session, track: schemas.TrackCreate, author_id: int):
    db_track = models.Track(**track.model_dump(), parent_id=author_id)

    db.add(db_track)
    db.commit()
    db.refresh(db_track)

    return db_track
