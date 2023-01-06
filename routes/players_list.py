from tinyhtml import html, h, raw

from functions.common import head
from database.players_db import get_players_from_db

all_players = get_players_from_db()


def list_all_players():
    return html()(
        h("head")(head),
        h("body")(
            h("input", type="text", id="myInput", onkeyup="filterPlayersByName()", placeholder="Nom du joueur...",
              title="Type in a name"),
            h("ul", id="myUL", klass="list-group")(
                h("li", klass="list-group-item")(
                    player.team().logo_html(),
                    " ",
                    h("a", href=f"/gamelog/{player.id}")(player.name)
                ) for player in all_players
            ),
            h("script")(filter_players_by_name_script())
        )
    ).render()


# TODO surnames (AD, KD...)
def filter_players_by_name_script() -> raw:
    return raw(
        """
            function filterPlayersByName() {
                var input, filter, ul, li, a, i, txtValue;
                input = document.getElementById("myInput");
                filter = input.value.toUpperCase();
                ul = document.getElementById("myUL");
                li = ul.getElementsByTagName("li");
                for (i = 0; i < li.length; i++) {
                    a = li[i].getElementsByTagName("a")[0];
                    txtValue = a.textContent || a.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        li[i].style.display = "";
                    } else {
                        li[i].style.display = "none";
                    }
                }
            }
        """
    )
