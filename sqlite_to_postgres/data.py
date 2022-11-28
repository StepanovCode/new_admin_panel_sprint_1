import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created: datetime
    modified: datetime


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created: datetime
    modified: datetime


@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    file_path: str
    rating: float
    type: str
    created: datetime
    modified: datetime


class SequenceSqlTableSaver(Enum):
    film_work = 1
    person = 2
    genre = 3
    genre_film_work = 4
    person_film_work = 5


SQLITE_TABLE_MOVIES = {
    'film_work': FilmWork,
    'person': Person,
    'genre': Genre,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork
}
