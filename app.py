from flask import Flask, redirect, render_template, flash, url_for, session, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from forms import LoginForm, SearchForm
from db_utils import *

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
ckeditor = CKEditor(app)


with app.app_context():
    db.drop_all()
    db.create_all()
    init_books(db)
    init_movies(db)


@app.route("/", methods=["GET", "POST"])
def index():
    search_form = SearchForm()
    books = []

    # Form submitting logic:
    if request.form.get("search_submit"):
        return redirect(url_for("index", search=request.form.get("search_text")))

    elif request.form.get("search_reset"):
        return redirect(url_for("index"))

    else:
        books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
        commit_diff_descr(db, books, request.form.items())

    # View:
    search = unidecode(request.args.get("search", "")).strip().casefold()
    if search != "":
        books = db.session.execute(
            db.select(Book)
            .order_by(Book.search)
            .where(Book.search.like("%" + search + "%"))
        ).scalars()
    else:
        books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
    return render_template("index.html", books=list(books), search_form=search_form)


@app.route("/booklist", methods=["GET", "POST"])
def booklist():
    if request.form.__len__() > 0:
        books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
        commit_diff_check(db, books, request.form.items())
    books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
    return render_template("booklist.html", books=list(books))


@app.route("/movies", methods=["GET", "POST"])
def movies():
    search_form = SearchForm()
    films = []

    # Form submitting logic:
    if request.form.get("search_submit"):
        return redirect(url_for("movies", search=request.form.get("search_text")))

    elif request.form.get("search_reset"):
        return redirect(url_for("movies"))

    else:
        films = db.session.execute(db.select(Movie).order_by(Movie.search)).scalars()
        commit_diff_descr(db, films, request.form.items())

    # View:
    search = unidecode(request.args.get("search", "")).strip().casefold()
    if search != "":
        films = db.session.execute(
            db.select(Movie)
            .order_by(Movie.search)
            .where(Movie.search.like("%" + search + "%"))
        ).scalars()
    else:
        films = db.session.execute(db.select(Movie).order_by(Movie.search)).scalars()
    return render_template("movies.html", films=list(films), search_form=search_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged", False):
        return redirect(url_for("logout"))

    else:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            if login_form.password.data == "test" and login_form.login.data == True:
                session["logged"] = True
                return redirect(url_for("index"))

            flash("Niepoprawne hasło", "error")

    return render_template("login.html", login_form=login_form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if session.get("logged", False):
        session.pop("logged")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/secret")
def secret():
    return render_template("secret.html")


if __name__ == "__main__":
    app.run(debug=True)
