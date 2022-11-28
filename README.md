# Thiapathioly ES Fantasy League (TEFL)

## Use cases

- save players to database (one-time thing)

```plantuml
@startuml
loop for each NBA team
ThiapzFL->BasketballReference: get team roster
end loop
ThiapzFL->PlayersDatabase: save all players info
note right
  name
  bb reference profile uri
end note
@enduml
```

- get gamelog for player with TTFL scores

```plantuml
@startuml 
User->ThiapzFL: search gamelog for players 
ThiapzFL->PlayersDatabase: find players which name contains the user input
loop for each matching player
  ThiapzFL->BasketballReference: get player gamelog
  loop for each game played
    ThiapzFL->ThiapzFL: extract game stats
    ThiapzFL->ThiapzFL: calculate TTFL score for the game
  end loop 
  ThiapzFL->ThiapzFL: calculate TTFL average score
end loop
ThiapzFL-->User: HTML page with TTFL gamelog for each matching player
@enduml
```

- get live TTFL scores

```plantuml
@startuml
User->ThiapzFL: get live scores
ThiapzFL->ESPN: get scoreboard
activate ESPN
loop for each live or finished game
  ThiapzFL->ESPN: get game boxscore
  deactivate ESPN
  loop for each player involved in the game
    ThiapzFL->ThiapzFL: extract player info
    ThiapzFL->ThiapzFL: calculate TTFL score
  end loop
end loop
ThiapzFL->ThiapzFL: sort all players' TTFL scores descending
ThiapzFL-->User: HTML page with a table containing all players involved in a game, and their TTFL scores
note right 
player name
team
ttfl score
minutes played
game location
opponent
end note 
@enduml
```

### Top TTFL averages
- for each player, calculate TTFL average
- sort and display as a list, for each element:
    - player name
    - player TTFL average

### Injury report of a team

if __name__ == '__main__':
    today = datetime.now().strftime("%Y%m%d")
    tomorrow = datetime.now().strftime("%Y%m%d")

### TTFL scores of a player against a team for the two-three last years

    scoreboard_page = BeautifulSoup(requests.get(f"https://www.espn.com/nba/scoreboard").text, "html.parser")
    games = scoreboard_page.select("div[class~=ScoreboardScoreCell] ul[class~=ScoreboardScoreCell__Competitors]")
    team_names = [g.select("div[class~=ScoreCell__TeamName]") for g in games]
    competitors = [(home, away) for home, away in team_names]

    injuries_page = BeautifulSoup(requests.get(f"https://www.espn.com/nba/injuries").text, "html.parser")

    injuries_per_team = injuries_page.select("div[class~=Table__league-injuries]")

    team_injuries = injuries_per_team[0]

    team_name = team_injuries.select_one("div[class~=Table__Title] span[class~=injuries__teamName]").text

    players = team_injuries.select("tbody > tr")

    first_player = players[0]

    print(first_player.select_one("td[class~=col-name] > a").text)
    print(first_player.select_one("td[class~=col-stat] > span").text)
    print(first_player.select_one("td[class~=col-desc]").text)

    session: HTMLSession = HTMLSession()
    r = session.get("https://www.espn.com/nba/scoreboard")

    r.html.render()
    print(r.html.search('<div class="ScoreCell__Time ScoreboardScoreCell__Time h9 clr-negative">{}</div>'))

    #print([(home.text, away.text) for home, away in competitors])





    #self.entries = sorted(entries, key=lambda entry: entry.date, reverse=True)

