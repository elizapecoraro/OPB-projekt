from bottle import Bottle, request, run, static_file, template

from Services.restavracija_service import RestavracijaService


app = Bottle()
service = RestavracijaService()


DNEVI = [
    {"id": 1, "ime": "ponedeljek"},
    {"id": 2, "ime": "torek"},
    {"id": 3, "ime": "sreda"},
    {"id": 4, "ime": "četrtek"},
    {"id": 5, "ime": "petek"},
    {"id": 6, "ime": "sobota"},
    {"id": 7, "ime": "nedelja"},
]


def v_int(vrednost):
    if vrednost is None or vrednost == "":
        return None

    try:
        return int(vrednost)
    except ValueError:
        return None


@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="Presentation/static")


@app.get("/")
def index():
    iskanje = request.query.getunicode("q") or ""
    lokacija_id = request.query.getunicode("lokacija_id") or ""
    kuhinja_id = request.query.getunicode("kuhinja_id") or ""
    dan_v_tednu = request.query.getunicode("dan_v_tednu") or ""
    ima_telefon = request.query.getunicode("ima_telefon") == "1"
    ima_spletno_stran = request.query.getunicode("ima_spletno_stran") == "1"
    ima_delovni_cas = request.query.getunicode("ima_delovni_cas") == "1"
    stran = v_int(request.query.getunicode("stran")) or 1
    na_stran = 30

    if stran < 1:
        stran = 1

    offset = (stran - 1) * na_stran

    napaka = None
    restavracije = []
    lokacije = []
    kuhinje = []

    skupno_restavracij = 0
    skupno_strani = 1

    try:
        lokacije = service.vse_lokacije()
        kuhinje = service.vse_kuhinje()

        skupno_restavracij = service.stevilo_restavracij(
            iskanje=iskanje or None,
            lokacija_id=v_int(lokacija_id),
            kuhinja_id=v_int(kuhinja_id),
            dan_v_tednu=v_int(dan_v_tednu),
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
        )

        skupno_strani = max(1, (skupno_restavracij + na_stran - 1) // na_stran)

        if stran > skupno_strani:
            stran = skupno_strani
            offset = (stran - 1) * na_stran

        restavracije = service.poisci_restavracije(
            iskanje=iskanje or None,
            lokacija_id=v_int(lokacija_id),
            kuhinja_id=v_int(kuhinja_id),
            dan_v_tednu=v_int(dan_v_tednu),
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
            limit=na_stran,
            offset=offset,
        )
    except Exception as exc:
        napaka = str(exc)

    return template(
        "Presentation/views/index.html",
        restavracije=restavracije,
        lokacije=lokacije,
        kuhinje=kuhinje,
        dnevi=DNEVI,
        iskanje=iskanje,
        izbrana_lokacija=lokacija_id,
        izbrana_kuhinja=kuhinja_id,
        izbrani_dan=dan_v_tednu,
        ima_telefon=ima_telefon,
        ima_spletno_stran=ima_spletno_stran,
        ima_delovni_cas=ima_delovni_cas,
        stran=stran,
        na_stran=na_stran,
        skupno_restavracij=skupno_restavracij,
        skupno_strani=skupno_strani,
        napaka=napaka,
    )


@app.get("/restavracije/<restavracija_id:int>")
def podrobnosti_restavracije(restavracija_id):
    napaka = None
    restavracija = None
    delovni_casi = []

    try:
        restavracija = service.podrobnosti_restavracije(restavracija_id)
        delovni_casi = service.delovni_cas_restavracije(restavracija_id)
    except Exception as exc:
        napaka = str(exc)

    if restavracija is None and napaka is None:
        napaka = "Restavracija ne obstaja."

    return template(
        "Presentation/views/podrobnosti.html",
        restavracija=restavracija,
        delovni_casi=delovni_casi,
        dnevi=DNEVI,
        napaka=napaka,
    )


if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True, reloader=True)