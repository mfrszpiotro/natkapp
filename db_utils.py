from flask_sqlalchemy import SQLAlchemy
from unidecode import unidecode
import requests

db = SQLAlchemy()


class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)


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
    year = db.Column(db.Integer, nullable=True)
    runtime = db.Column(db.String, nullable=True)


def get_diff(tuple_list_db, tuple_list_form):
    return [fd for fd in tuple_list_form if fd not in tuple_list_db]


def extract_db_descr(books):
    return [(str(book.id), book.descr) for book in books]


def extract_db_check(books):
    return [(str(book.id), book.check) for book in books]


def commit_diff_descr(database, books, form_books):
    diffs = get_diff(extract_db_descr(books), list(form_books))
    for d in diffs:
        db_book = database.session.execute(
            db.select(Book).where(Book.id == int(d[0]))
        ).scalar_one()
        db_book.descr = d[1]
        database.session.commit()


def commit_diff_check(database, books, form_books):
    diffs = get_diff(extract_db_check(books), list(form_books))
    for d in diffs:
        db_book = database.session.execute(
            db.select(Book).where(Book.id == int(d[0]))
        ).scalar_one()
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


def get_movie_details(id):
    url = "https://api.themoviedb.org/3/movie/{}".format(id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmYxODNiNTU4NTk1NTAxMDU3YzRmZGNiMjdkZjM5YiIsInN1YiI6IjY0YTAyYTI0ZDUxOTFmMDBlMjYzOTRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.auBno1g8lHhknr7TwBMTGMNvsYBqViqJ3nJNK05HN0E",
    }
    response = requests.get(url, headers=headers)
    content = response.json()
    return content["release_date"][0:4], content["runtime"]


def init_movies(database):
    url = "https://api.themoviedb.org/3/person/40239/movie_credits?language=cz-CZ"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmYxODNiNTU4NTk1NTAxMDU3YzRmZGNiMjdkZjM5YiIsInN1YiI6IjY0YTAyYTI0ZDUxOTFmMDBlMjYzOTRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.auBno1g8lHhknr7TwBMTGMNvsYBqViqJ3nJNK05HN0E",
    }
    response = requests.get(url, headers=headers)
    url_content = response.json()
    for appear in eliminate_duplicates(url_content.get("cast", []), "title"):
        details = get_movie_details(appear.get("id"))
        movie = Movie(
            seen="no",
            orig_title=appear.get("original_title", ""),
            name=appear.get("title", ""),
            search=unidecode(appear.get("original_title", "")).strip().casefold(),
            img=appear.get("poster_path", "missing.jpg"),
            appear_type="cast",
            job=appear.get("job", ""),
            descr="Natka chyba jeszcze nie oglądała tego filmu!",
            year=details[0],
            runtime=details[1],
        )
        db.session.add(movie)
    for appear in eliminate_duplicates(url_content.get("crew", []), "title"):
        if not appear.get("original_title", "") == "Já truchlivý bůh":
            details = get_movie_details(appear.get("id"))
            movie = Movie(
                seen="no",
                orig_title=appear.get("original_title", ""),
                name=appear.get("title", ""),
                search=unidecode(appear.get("original_title", "")).strip().casefold(),
                img=appear.get("poster_path", "missing.jpg"),
                appear_type="crew",
                job=appear.get("job", ""),
                descr="Natka chyba jeszcze nie oglądała tego filmu!",
                year=details[0],
                runtime=details[1],
            )
            database.session.add(movie)
    database.session.commit()


def init_books(database):
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Życie jest gdzie indziej",
        search="zycie jest gdzie indziej",
        img="indziej.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Księga śmiechu i zapomnienia",
        search="ksiega smiechu i zapomnienia",
        img="ksiega.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Śmieszne miłości",
        search="smieszne milosci",
        img="milosci.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Nieśmiertelność",
        search="niesmiertelnosc",
        img="niesmiertelnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Powoloność",
        search="powolnosc",
        img="powolnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Święto nieistotności",
        search="swieto nieistotnosci",
        img="swieto.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Zdradzone testamenty",
        search="zdradzone testamenty",
        img="testamenty.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Walc pożegnalny",
        search="walc pozegnalny",
        img="walc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Żart",
        search="zart",
        img="zart.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Zasłona",
        search="zaslona",
        img="zaslona.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Sztuka powieści",
        search="sztuka",
        img="sztuka.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Tożsamość",
        search="tozsamosc",
        img="tozsamosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Kubuś i jego pan",
        search="kubus i jego pan",
        img="kubus.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Nieznośna lekkość bytu",
        search="nieznosna lekkosc bytu",
        img="nieznosna.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Spotkanie",
        search="spotkanie",
        img="spotkanie.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="no",
        name="Niewiedza",
        search="niewiedza",
        img="niewiedza.jpg",
    )
    database.session.add(book)
    database.session.commit()
