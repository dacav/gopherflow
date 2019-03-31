from html2text import html2text
import pituophis
import stackexchange
import sys

BIND = "127.0.0.1"
PORT = 9070
DEFAULT_PARAMS = dict(host="localhost", port=PORT, tls=False)
COLUMNS = 74
SITE = stackexchange.StackOverflow

BREAK = COLUMNS * '-'
TYPE_TEXT = '0'
TYPE_MENU = '1'
TYPE_ERROR = '3'
TYPE_INFO = 'i'
TYPE_HTML = 'h'


def selector(type, text, path):
    return pituophis.Selector(
        itype=type, text=text, path=path, **DEFAULT_PARAMS
    )


def info(text):
    return selector(TYPE_INFO, text, "")


def error(text):
    return selector(TYPE_ERROR, text, "")


def sep():
    return pituophis.Selector()


def menu(text, path):
    return selector(TYPE_MENU, text, path)


def format_h1(text):
    yield sep()
    yield sep()
    yield info(text.center(COLUMNS))
    yield info(("=" * len(text)).center(COLUMNS))
    yield sep()


def format_h2(text):
    yield sep()
    yield sep()
    yield info(text.center(COLUMNS))
    yield info(("-" * len(text)).center(COLUMNS))
    yield sep()


def format_table(*items):
    yield info(BREAK)
    for item in items:
        yield info("%-20s %s" % item)
    yield info(BREAK)


def format_user(user):
    yield menu(
        "USER @%s (reputation %d)" % (
            user.display_name,
            user.reputation),
        "/u/%s"   % user.id
    )


def handle_question(site, data):
    question = site.question(data[0])

    yield from format_h1(question.title.upper())

    yield sep()
    body = html2text(question.body, bodywidth=COLUMNS)
    yield from map(info, body.splitlines())
    yield from format_user(question.owner)
    yield sep()

    yield from format_table(
        ("Creation date",   question.creation_date),
        ("Last Activity",   question.last_activity_date),
        ("Score",           question.score),
        ("View Count",      question.view_count),
        ("Tags",            ", ".join(question.tags)),
    )


    for ansnr, ans in enumerate(question.answers):

        yield from format_h2(
            "Answer %d%s" % (ansnr, " (accepted)" if ans.is_accepted else "")
        )

        yield from map(info, html2text(ans.body).splitlines())
        yield from format_user(ans.owner)



if __name__ == "__main__":
    handlers = dict(
        question=handle_question,
        q=handle_question,
    )

    site = stackexchange.Site(SITE)
    site.be_inclusive()

    def handle(request):
        kind, *data = (x for x in request.path.split("/") if x)
        handler = handlers.get(kind)
        if handler is None:
            return [error("I don't know how to handle %r" % kind)]
        return list(handler(site, data))

    pituophis.serve(BIND, PORT, handle, tls=False)
