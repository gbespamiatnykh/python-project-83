import os
from datetime import date

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.url_repository import UrlRepository
from page_analyzer.url_utils import normalize_url, parse_html, validate

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
    id = repo.add(normalized_url, date.today())
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url", id=id))


@app.route("/urls/<int:id>")
def show_url(id):
    url = repo.find_by_id(id)
    if not url:
        abort(404)
    checks = repo.get_checks(id)
    return render_template("show.html", url=url, checks=checks)


@app.route("/urls")
def list_urls():
    urls = repo.get_all()
    return render_template("list.html", urls=urls)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def add_check(id):
    url = repo.find_by_id(id)
    try:
        response = requests.get(url.get("name"))
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url", id=id))
    html_data = parse_html(response.text)
    repo.add_check(id, response.status_code, html_data, date.today())
    flash("Страница успешно проверена", "success")
    return redirect(url_for("show_url", id=id))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")
