from tinyhtml import html, h

from functions import live_scores
from functions.common import head


def live_ttfl_scores():
    all_scores = live_scores.live_ttfl_scores()

    return html()(
        h("head")(head),
        h("body")(
            h("div")(
                h("h2")("Meilleurs scores TTFL de la nuit"),
                h("table", klass="table table-sm table-responsive table-bordered")(
                    h("thead", klass="table-light")(
                        h("tr")(
                            h("th", scope="col")("#"),
                            h("th", scope="col")("Joueur"),
                            h("th", scope="col", klass="text-center")("Score TTFL"),
                            h("th", scope="col")("Adversaire"),
                            h("th", scope="col", klass="text-center")("Minutes"),
                            h("th", scope="col", klass="text-center")("Terrain/Banc?"),
                            h("th", scope="col", klass="text-center")("Fautes (Tech.)"),
                            h("th", scope="col", klass="text-center")("Temps du match"),
                            h("th", scope="col", klass="text-center")("Score du match")
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        h("tr")(
                            h("th", scope="row")(index + 1),
                            h("td")(player_score.name_html()),
                            h("td", klass="text-center")(player_score.ttfl_score_html()),
                            h("td")(player_score.opponent_team_html()),
                            h("td", klass="text-center")(player_score.minutes_played_html()),
                            h("td", klass="text-center")(player_score.status.html()),
                            h("td", klass="text-center")(player_score.fouls_html()),
                            h("td", klass="text-center")(player_score.game_status),
                            h("td", klass="text-center")(player_score.game_score_html())
                        ) for index, player_score in enumerate(all_scores)
                    )
                )
            )
        )
    ).render()
