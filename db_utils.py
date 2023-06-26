from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# api google books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


# api imdb movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


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
        img="indziej.jfif",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Księga śmiechu i zapomnienia",
        img="ksiega.jpeg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Śmieszne miłości",
        img="milosci.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Nieśmiertelność",
        img="niesmiertelnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Powolność",
        img="powolnosc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Święto nieistotności",
        img="swieto.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Zdradzone testamenty",
        img="testamenty.jfif",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Walc pożegnalny",
        img="walc.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Żart",
        img="zart.jpg",
    )
    database.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check="yes",
        name="Zasłona",
        img="zaslona.jpg",
    )
    database.session.add(book)
    database.session.commit()
