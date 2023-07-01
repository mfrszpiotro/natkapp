from flask_sqlalchemy import SQLAlchemy

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
    name = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
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
