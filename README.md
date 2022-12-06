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

### TTFL scores of a player against a team for the two-three last years


