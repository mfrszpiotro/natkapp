from flask import Flask, redirect, render_template, flash, url_for, session, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config[
    "SECRET_KEY"
] = 'h+u5-sNA2%Fr&3"y"9nQEn==rfLjfKB{$RGShJ"$2I`d&j[5-J79:RJZoQJ('
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///natkapp.db"
app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "lux"
db.init_app(app)
bootstrap = Bootstrap5(app)


# api google books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


# api imdb movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    descr = db.Column(db.String, nullable=True)


with app.app_context():
    db.create_all()


def init_books():
    book = Book(

        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Życie jest gdzie indziej",
        img="indziej.jfif",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Księga śmiechu i zapomnienia",
        img="ksiega.jpeg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Śmieszne miłości",
        img="milosci.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Nieśmiertelność",
        img="niesmiertelnosc.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Powolność",
        img="powolnosc.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Święto nieistotności",
        img="swieto.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Zdradzone testamenty",
        img="testamenty.jfif",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Walc pożegnalny",
        img="walc.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Żart",
        img="zart.jpg",
    )
    db.session.add(book)
    book = Book(
        descr="Jak poprosisz ładnie Natkę, to ci tu napisze opinię o tym Kunderze...",
        check=True,
        name="Zasłona",
        img="zaslona.jpg",
    )
    db.session.add(book)
    db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()
    if request.form.get("descriptions"):
        flash("ok", "success")
    return render_template("index.html", books=books)


@app.route("/booklist")
def booklist():
    #init_books()
    books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()
    return render_template("booklist.html", books=books)


@app.route("/movies")
def movies():
    return render_template("movies.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged", False):
        return redirect(url_for("logout"))

    else:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            if login_form.password.data == "test" and login_form.login.data == True:
                session["logged"] = True
                flash("Zalogowałaś się!", "success")
                return redirect(url_for("index"))

            flash("Niepoprawne hasło", "error")

    return render_template("login.html", login_form=login_form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if session.get("logged", False):
        session.pop("logged")
        flash("Wylogowałaś się!", "success")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/secret")
def secret():
    return render_template("secret.html")


if __name__ == "__main__":
    app.run(debug=True)
