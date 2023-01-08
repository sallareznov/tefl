import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from nba_api.stats.endpoints import PlayerGameLog

from data.caches import Caches
from database.players_db import get_players_from_db
from routes import injury_report_html, player_gamelog, live_scores_html, home, players_list

app = Flask(__name__)

all_players = get_players_from_db()

caches = Caches()
scheduler = BackgroundScheduler()
scheduler.add_job(caches.clear_latest_injury_report, "cron", minute="*/10")
scheduler.add_job(caches.clear_gamelog_cache, "cron", hour="8", minute="0")
scheduler.add_job(caches.clear_teams_gamelog_cache, "cron", hour="8", minute="0")
scheduler.start()


@app.route("/")
def homepage(): return home.homepage()


@app.route("/players")
def list_all_players(): return players_list.list_all_players()


@app.route("/gamelog/<player_id>")
def gamelog_for_player(player_id: str): return player_gamelog.gamelog_for_player(player_id, caches)


@app.route("/live")
def live_ttfl_scores(): return live_scores_html.live_ttfl_scores()


@app.route("/injuries")
def injury_report(): return injury_report_html.injury_report(caches)


@app.route("/test")
def test():
    time.sleep(1)
    return PlayerGameLog(player_id=203937).get_json()
