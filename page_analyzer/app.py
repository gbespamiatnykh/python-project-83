import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.url_repository import UrlRepository
from page_analyzer.url_utils import normalize_url, validate

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
repo = UrlRepository(DATABASE_URL)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["POST"])
def add_url():
    url_data = request.form.get("url")
    errors = validate(url_data)
    if errors:
        flash("Некорректный URL", "danger")
        return redirect(url_for("index"))

    normalized_url = normalize_url(url_data)
    url = repo.find_by_name(normalized_url)
    if url:
        flash("Страница уже существует", "info")
        return redirect(url_for("show_url", id=url.get("id")))
    creation_date = date.today()
    id = repo.add(normalized_url, creation_date)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url", id=id))


@app.route("/urls/<int:id>")
def show_url(id):
    url = repo.find_by_id(id)
    checks = repo.get_checks(id)
    return render_template("show.html", url=url, checks=checks)


@app.route("/urls")
def list_urls():
    urls = repo.get_all()
    return render_template("list.html", urls=urls)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def add_check(id):
    check_date = date.today()
    repo.add_check(id, check_date)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("show_url", id=id))
