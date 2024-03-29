from flask import (
    Flask,
    redirect,
    render_template,
    flash,
    url_for,
    session,
    request,
    send_file,
)
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from forms import LoginForm, SearchForm
from db_utils import commit_diff_check, commit_diff_descr, init_czech, init_books, init_movies
from models import Book, Kniha, Movie, Pass, db
from config import Config
from unidecode import unidecode

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)

with app.app_context():
    pass
    # NOTE: deploying correctly on free render.com requires turning off db drop/init with every initialization:
    # db.drop_all()
    # db.create_all()
    # init_books(db)
    # init_movies(db)
    # init_czech(db)



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
    # todo - not too elegant imo
    if request.form.get("search_submit"):
        books = db.session.execute(
            db.select(Book).order_by(Book.search).where(Book.check == "no")
        ).scalars()
        if len(list(books)) > 0:
            flash("Natka nie ma jeszcze kilku książek...", "error")
            books = db.session.execute(
                db.select(Book).order_by(Book.search).where(Book.check == "no")
            ).scalars()
            return render_template("booklist.html", books=list(books))
        flash("Natka ma już wszystkie ksiązki!", "success")

    # todo - not too elegant imo
    elif request.form.get("search_reset"):
        books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
        return render_template("booklist.html", books=list(books))

    elif request.form.__len__() > 0:
        books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
        commit_diff_check(db, books, request.form.items())
    books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
    return render_template("booklist.html", books=list(books))


@app.route("/czech", methods=["GET", "POST"])
def czech():
    search_form = SearchForm()
    books = []

    # Form submitting logic:
    if request.form.get("search_submit"):
        return redirect(url_for("czech", search=request.form.get("search_text")))

    elif request.form.get("search_reset"):
        return redirect(url_for("czech"))

    else:
        books = db.session.execute(db.select(Kniha).order_by(Kniha.search)).scalars()
        commit_diff_descr(db, books, request.form.items(), True)

    # View:
    search = unidecode(request.args.get("search", "")).strip().casefold()
    if search != "":
        books = db.session.execute(
            db.select(Kniha)
            .order_by(Kniha.search)
            .where(Kniha.search.like("%" + search + "%"))
        ).scalars()
    else:
        books = db.session.execute(db.select(Kniha).order_by(Kniha.search)).scalars()
    return render_template("czech.html", books=list(books), search_form=search_form)


@app.route("/czechlist", methods=["GET", "POST"])
def czechlist():
    # todo - not too elegant imo
    if request.form.get("search_submit"):
        books = db.session.execute(
            db.select(Kniha).order_by(Kniha.search).where(Kniha.check == "no")
        ).scalars()
        if len(list(books)) > 0:
            flash("Natce stále chybí několik knih...", "error")
            books = db.session.execute(
                db.select(Kniha).order_by(Kniha.search).where(Kniha.check == "no")
            ).scalars()
            return render_template("czechlist.html", books=list(books))
        flash("Natka už má všechny knihy!", "success")

    # todo - not too elegant imo
    elif request.form.get("search_reset"):
        books = db.session.execute(db.select(Kniha).order_by(Kniha.search)).scalars()
        return render_template("czechlist.html", books=list(books))

    elif request.form.__len__() > 0:
        books = db.session.execute(db.select(Kniha).order_by(Kniha.search)).scalars()
        commit_diff_check(db, books, request.form.items(), True)
    books = db.session.execute(db.select(Kniha).order_by(Kniha.search)).scalars()
    return render_template("czechlist.html", books=list(books))


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
            pass_check = db.session.execute(db.select(Pass)).scalar_one_or_none()
            if (
                login_form.password.data == pass_check.password
                and login_form.login.data == True
            ):
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
    # PASSWORD SETUP/RESET
    # db.session.add(Pass(password="wdupietrzaslo"))
    # db.session.commit()
    return send_file(
        "instance/natkapp.db", download_name="natkapp.db", as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
