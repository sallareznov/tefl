# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, run

from tefl.teams import teams_dict


@route('/')
def hello_world():
    return teams_dict


run(host='localhost', port=8080)
