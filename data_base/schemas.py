from typing import Union
from pydantic import BaseModel
# from settings import AUDIOS_PATH
# import os

class TrackBase(BaseModel):
    title: str
    description: Union[str, None] = None

    path: str
    year: int


class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    tracks: list[Track] = []

    class Config:
        from_attributes = True