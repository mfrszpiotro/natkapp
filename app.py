from flask import Flask, redirect, render_template, flash, url_for, session, request
from flask_bootstrap import Bootstrap5
from forms import LoginForm
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


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.form.__len__() > 0:
        books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()
        commit_diff_descr(db, books, request.form.items())
    books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()
    return render_template("index.html", books=books)


@app.route("/booklist", methods=["GET", "POST"])
def booklist():
    # init_books(db)
    if request.form.__len__() > 0:
        books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()
        commit_diff_check(db, books, request.form.items())
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
