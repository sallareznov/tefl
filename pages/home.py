from tinyhtml import html, h, _h

from pages import common


def homepage():
    return html()(
        h("head")(common.head),
        h("body")(
            h("div", klass="list-group")(
                homepage_entry("/live", "Scores en live", "Scores TTFL en live de la soirée"),
                homepage_entry("/injuries", "Injury report", "Injury report le plus récent des matchs de la soirée"),
                homepage_entry("/players", "Stats joueurs", "Stats TTFL de tous les joueurs qui ont joué cette saison")
            ),
            common.bootstrap_js_script
        )
    ).render()


def homepage_entry(route: str, title: str, description: str) -> _h:
    return h("a", href=route, klass="list-group-item list-group-item-action flex-column align-items-start")(
        h("div", klass="d-flex w-100 justify-content-between")(
            h("h5", klass="mb-1")(title)
        ),
        h("p", klass="mb-1")(description)
    )
