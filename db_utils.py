from flask_sqlalchemy import SQLAlchemy
import requests, urllib3

db = SQLAlchemy()


# api google books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    search = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


# api imdb movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seen = db.Column(db.String, nullable=False)
    orig_title = name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    search = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    appear_type = db.Column(db.String, nullable=False)
    job = db.Column(db.String, nullable=False)
    descr = db.Column(db.String, nullable=True)


def correct_polish_letters(st):
    pol = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z"}
    return "".join([pol[c] if c in pol else c for c in st])


def get_diff(tuple_list_db, tuple_list_form):
    return [fd for fd in tuple_list_form if fd not in tuple_list_db]


def extract_db_descr(books):
    return [(str(book.id), book.descr) for book in books]


def extract_db_check(books):
    return [(str(book.id), book.check) for book in books]


def commit_diff_descr(database, books, form_books):
    diffs = get_diff(extract_db_descr(books), list(form_books))
    for d in diffs:
        db_book = database.session.execute(db.select(Book).where(Book.id == int(d[0]))).scalar_one()
        db_book.descr = d[1]
        database.session.commit()


def commit_diff_check(database, books, form_books):
    diffs = get_diff(extract_db_check(books), list(form_books))
    for d in diffs:
        db_book = database.session.execute(db.select(Book).where(Book.id == int(d[0]))).scalar_one()
        db_book.check = d[1]
        database.session.commit()

def eliminate_duplicates(list_of_dicts, key):
    unique_dicts = []
    keys_set = set()

    for dictionary in list_of_dicts:
        if dictionary[key] not in keys_set:
            keys_set.add(dictionary[key])
            unique_dicts.append(dictionary)

    return unique_dicts

def init_movies(database):
    url = "https://api.themoviedb.org/3/person/40239/movie_credits?language=cz-CZ"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmYxODNiNTU4NTk1NTAxMDU3YzRmZGNiMjdkZjM5YiIsInN1YiI6IjY0YTAyYTI0ZDUxOTFmMDBlMjYzOTRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.auBno1g8lHhknr7TwBMTGMNvsYBqViqJ3nJNK05HN0E"
    }
    response = requests.get(url, headers=headers)
    url_content = response.json()
    for appear in eliminate_duplicates(url_content.get("cast", []), "title"):
        movie = Movie(
            seen = "no",
            orig_title = appear.get("original_title", ""),
            name = appear.get("title", ""),
            search = str(appear.get("title", "")).strip().casefold(),
            img = appear.get("poster_path", "placeholder.png"),
            appear_type = "cast",
            job = appear.get("job", ""),
            descr = "",
        )
        db.session.add(movie)
    for appear in eliminate_duplicates(url_content.get("crew", []), "title"):
        movie = Movie(
            seen = "no",
            orig_title = appear.get("original_title", ""),
            name = appear.get("title", ""),
            search = str(appear.get("title", "")).strip().casefold(),
            img = appear.get("poster_path", "placeholder.png"),
            appear_type = "crew",
            job = appear.get("job", ""),
            descr = "",
        )
        database.session.add(movie)
    database.session.commit()

def init_books(database):
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Życie jest gdzie indziej",
        search="zycie jest gdzie indziej",
        img="indziej.jfif",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Księga śmiechu i zapomnienia",
        search="ksiega smiechu i zapomnienia",
        img="ksiega.jpeg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Śmieszne miłości",
        search="smieszne milosci",
        img="milosci.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Nieśmiertelność",
        search="niesmiertelnosc",
        img="niesmiertelnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Powoloność",
        search="powolnosc",
        img="powolnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Święto nieistotności",
        search="swieto nieistotnosci",
        img="swieto.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Zdradzone testamenty",
        search="zdradzone testamenty",
        img="testamenty.jfif",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Walc pożegnalny",
        search="walc pozegnalny",
        img="walc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Żart",
        search="zart",
        img="zart.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Zasłona",
        search="zaslona",
        img="zaslona.jpg",
    )
    database.session.add(book)
    database.session.commit()
