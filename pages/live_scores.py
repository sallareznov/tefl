from tinyhtml import html, h, raw

from functions import live_scores
from functions.common import head


def live_ttfl_scores():
    all_scores = live_scores.live_ttfl_scores()

    return html()(
        h("head")(head),
        h("body")(
            h("div", klass="container-fluid")(
                h("div")(
                    h("nav", klass="navbar navbar-expand-lg navbar-light bg-light")(
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
                    )
                ),
                h("div", klass="col-sm-4")(
                    h("input", klass="form-control m-5", type="text", id="search",
                      onkeyup="filterPlayersByName()",
                      placeholder="Rechercher un joueur")
                ),
                h("div", klass="row")(
                    h("table", klass="table table-sm table-responsive table-bordered", id="liveTable")(
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
            ),
            h("script")(filter_players_by_name_script())
        )
    ).render()


def filter_players_by_name_script() -> raw:
    return raw(
        """
            function filterPlayersByName() {
                var input, filter, table, tr, td, i, txtValue;
                input = document.getElementById("search");
                filter = input.value.toUpperCase();
                table = document.getElementById("liveTable");
                tr = table.getElementsByTagName("tr");
                for (i = 0; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[0];
                    if (td) {
                        txtValue = td.getElementsByTagName("span")[0].getAttribute("title");
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        } else {
                        tr[i].style.display = "none";
                        }
                    }       
                }
            }
        """
    )
