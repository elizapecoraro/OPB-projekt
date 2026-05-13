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
    lokacija_id = request.query.getunicode("lokacija_id") or ""
    kuhinja_id = request.query.getunicode("kuhinja_id") or ""

    napaka = None
    restavracije = []
    lokacije = []
    kuhinje = []

    try:
        restavracije = service.poisci_restavracije(
            iskanje=iskanje or None,
            lokacija_id=int(lokacija_id) if lokacija_id else None,
            kuhinja_id=int(kuhinja_id) if kuhinja_id else None,
        )
        lokacije = service.vse_lokacije()
        kuhinje = service.vse_kuhinje()
    except Exception as exc:
        napaka = str(exc)

    return template(
        "Presentation/views/index.html",
        restavracije=restavracije,
        lokacije=lokacije,
        kuhinje=kuhinje,
        iskanje=iskanje,
        izbrana_lokacija=lokacija_id,
        izbrana_kuhinja=kuhinja_id,
        napaka=napaka,
    )


if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True, reloader=True)
