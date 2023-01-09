from tinyhtml import html, h

from data.caches import Caches
from database.player_repository import PlayerRepository
from functions import gamelog
from functions.common import head


def gamelog_for_player(player_id: str, repository: PlayerRepository, caches: Caches):
    gl = caches.get_gamelog_of_player(player_id) or gamelog.player_gamelog(player_id, repository)
    caches.add_to_gamelog_cache(player_id, gl)

    return html()(
        h("head")(head),
        h("body")(
            h("div")(
                h("h2")(gl.team.logo_html(), " ", gl.player, " ", f"[moyenne TTFL: {gl.ttfl_average}]"),
                h("table", klass="table table-sm table-responsive table-bordered")(
                    h("thead", klass="table-light")(
                        h("tr")(
                            h("th", scope="col")("#"),
                            h("th", scope="col", klass="text-center")("Date"),
                            h("th", scope="col")("Adversaire"),
                            h("th", scope="col", klass="text-center")("Lieu"),
                            h("th", scope="col", klass="text-center")("Minutes jouées"),
                            h("th", scope="col", klass="text-center")("Score TTFL")
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        h("tr")(
                            h("th", scope="row")(index + 1),
                            h("td", klass="text-center")(result.date.strftime("%d-%m-%Y")),
                            h("td")(result.opponent.html_with_nickname()),
                            h("td", klass="text-center")(result.location.html_with_emoji()),
                            h("td", klass="text-center")(result.minutes_played_html()),
                            h("td", klass="text-center")(result.ttfl_stats.html())
                        ) for (index, result) in enumerate(gl.games)
                    )
                )
            )
        )
    ).render()
