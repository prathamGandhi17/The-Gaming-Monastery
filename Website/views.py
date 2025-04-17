from flask import Blueprint, render_template, Response
from flask_login import login_user, login_required, logout_user, current_user
from .models import Games, Genres

#urls
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")


#root
@views.route('/main')
@login_required
def main():
    games = Games.query.all()
    genres = Genres.query.all()
    response = Response(render_template("main.html", user=current_user, games=games, genres=genres))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
    
