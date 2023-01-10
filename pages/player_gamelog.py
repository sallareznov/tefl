from tinyhtml import html, h

from data.caches import Caches
from database.player_repository import PlayerRepository
from emojis import Emoji
from functions import player_gamelog
from functions.common import head


def gamelog_for_player(player_id: str, repository: PlayerRepository, caches: Caches):
    player = repository.get_player_by_id(player_id)
    team = player.team()
    gl = caches.get_gamelog_of_player(player_id) or player_gamelog.player_gamelog(player)
    caches.add_to_gamelog_cache(player_id, gl)

    return html()(
        h("head")(
            head,
            h("style")(
                f"""
                    th, nav {{
                        background-color: {team.primary_color()} !important;
                        color: {team.secondary_color()} !important;
                    }}
                    
                    a {{
                        color: {team.secondary_color()} !important;
                    }}
                """
            )
        ),
        h("body")(
            # TODO container-fluid
            h("nav", klass="navbar navbar-expand-lg")(
                h("button", klass="navbar-toggler", type="button", data_toggle="collapse",
                  data_target="#navbarNavAltMarkup", aria_controls="navbarNavAltMarkup", aria_expanded="false",
                  aria_label="Toggle navigation"
                  )(
                    h("span", klass="navbar-toggler-icon")
                ),
                h("div", klass="collapse navbar-collapse", id="navbarNavAltMarkup")(
                    h("div", klass="navbar-nav")(
                        h("a", klass="nav-item nav-link", href="/")("Home"),
                        h("a", klass="nav-item nav-link", href="/live")("Live scores"),
                        h("a", klass="nav-item nav-link", href="/injuries")("Injury Report"),
                        h("a", klass="nav-item nav-link", href="/players")("Stats joueurs")
                    )
                )
            ),
            h("div", klass="container-fluid")(
                h("div", klass="row", style=f"background-color: {team.primary_color()}")(
                    h("div", klass="col-sm-9 align-self-center",
                      style=f"text-align:center; color:{team.secondary_color()};")(
                        h("h1", klass="fw-bolder text-5xl")(gl.player),
                        h("h3", klass="fw-light")(team.logo3535_html(), " ", team.full_name()),
                        h("h3")(f"Moyenne TTFL: {gl.ttfl_average}")
                    ),
                    h("img", klass="col-sm-3 align-self-center mt-2", src=player.illustration)
                ),
                h("div", klass="row")(
                    h("table", klass="table table-sm table-responsive table-bordered")(
                        h("thead", klass="table-light")(
                            h("tr")(
                                h("th", scope="col")("#"),
                                h("th", scope="col", klass="text-center")(table_header("Date", Emoji.calendar)),
                                h("th", scope="col")(table_header("Adversaire", Emoji.punch)),
                                h("th", scope="col", klass="text-center")(table_header("Lieu", Emoji.position)),
                                h("th", scope="col", klass="text-center")(table_header("Minutes", Emoji.stopwatch)),
                                h("th", scope="col", klass="text-center")(
                                    table_header("Score TTFL", Emoji.chart_with_upwards_trend))
                            )
                        ),
                        h("tbody", klass="table-group-divider")(
                            h("tr")(
                                h("th", scope="row")(index + 1),
                                h("td", klass="text-center")(result.date.strftime("%d-%m-%Y")),
                                h("td")(result.opponent.html_with_nickname()),
                                h("td", klass="text-center")(result.location.html_with_emoji()),
                                h("td", klass="text-center")(result.minutes_played),
                                h("td", klass="text-center")(result.ttfl_stats.html())
                            ) for (index, result) in enumerate(gl.games)
                        )
                    )
                )
            )
        )
    ).render()


def table_header(title: str, emoji: Emoji): return emoji.html(), " ", title
