from flask import Blueprint, render_template, Response, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Games, Genres, UserGames

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/main')
@login_required
def main():
    # 1) fetch all games & genres
    games  = Games.query.all()
    genres = Genres.query.all()

    # 2) fetch this user's tags
    user_games = UserGames.query.filter_by(user_id=current_user.id).all()
    # map game_id → status string
    game_status_map = { ug.game_id: ug.status for ug in user_games }

    # 3) build lists of IDs for each status
    playing_ids = [ug.game_id for ug in user_games if ug.status == 'Playing']
    played_ids  = [ug.game_id for ug in user_games if ug.status == 'Played']

    # 4) fetch the actual Games rows for each tab
    playing_games = Games.query.filter(Games.id.in_(playing_ids)).all() if playing_ids else []
    played_games  = Games.query.filter(Games.id.in_(played_ids)).all()  if played_ids  else []

    # 5) render
    resp = Response(render_template(
        "main.html",
        user=current_user,
        games=games,
        genres=genres,
        game_status_map=game_status_map,
        playing_games=playing_games,
        played_games=played_games
    ))
    # disable caching (so back/forward works)
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"]        = "no-cache"
    resp.headers["Expires"]       = "0"
    return resp

@views.route('/add_to_playing/<int:game_id>')
@login_required
def add_to_playing(game_id):
    ug = UserGames.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    if ug:
        ug.status = 'Playing'
    else:
        ug = UserGames(user_id=current_user.id, game_id=game_id, status='Playing')
        db.session.add(ug)
    db.session.commit()
    return redirect(url_for('views.main'))

@views.route('/move_to_played/<int:game_id>')
@login_required
def move_to_played(game_id):
    ug = UserGames.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    if not ug or ug.status != 'Playing':
        flash("You can only mark a game as Played if it's currently Playing.", category='error')
    else:
        ug.status = 'Played'
        db.session.commit()
    return redirect(url_for('views.main'))
