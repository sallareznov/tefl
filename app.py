import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from data.caches import Caches
from database.player_repository import PlayerRepository
from pages import player_gamelog, home, players, live_scores, injury_report

app = Flask(__name__)

connection = sqlite3.connect("database/players.db", check_same_thread=False)
player_repository = PlayerRepository(connection)
all_players = player_repository.get_players_from_db()

caches = Caches()
scheduler = BackgroundScheduler()
scheduler.add_job(caches.clear_latest_injury_report, "cron", minute="*/10")
scheduler.add_job(caches.clear_gamelog_cache, "cron", hour="8", minute="0")
scheduler.add_job(caches.clear_teams_gamelog_cache, "cron", hour="8", minute="0")
scheduler.start()


@app.route("/")
def homepage(): return home.homepage()


@app.route("/players")
def list_all_players(): return players.all(all_players)


@app.route("/players/<player_id>/gamelog")
def gamelog_for_player(player_id: str): return player_gamelog.gamelog_for_player(player_id, player_repository, caches)


@app.route("/live")
def live_ttfl_scores(): return live_scores.live_ttfl_scores()


@app.route("/injuries")
def latest_injury_report(): return injury_report.injury_report(caches)
