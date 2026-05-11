from bottle import Bottle, request, run, static_file, template

from Services.restavracija_service import RestavracijaService

app = Bottle()
service = RestavracijaService()


@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="Presentation/static")


@app.get("/")
def index():
    iskanje = request.query.getunicode("q") or ""
    napaka = None
    restavracije = []

    try:
        restavracije = service.poisci_restavracije(iskanje=iskanje or None)
    except Exception as exc:
        napaka = str(exc)

    return template(
        "Presentation/views/index.tpl",
        restavracije=restavracije,
        iskanje=iskanje,
        napaka=napaka,
    )


if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True, reloader=True)
