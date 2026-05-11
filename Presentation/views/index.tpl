<!doctype html>
<html lang="sl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Restavracije v Sloveniji</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <main class="container">
    <header>
      <h1>Restavracije v Sloveniji</h1>
      <p>Pregled restavracij, lokacij in vrst kuhinje po podatkih OpenStreetMap.</p>
    </header>

    <form method="get" action="/" class="search-form">
      <input type="search" name="q" value="{{iskanje}}" placeholder="Išči po imenu ali kraju">
      <button type="submit">Išči</button>
    </form>

    % if napaka:
      <section class="warning">
        <strong>Baza še ni povezana.</strong>
        <p>{{napaka}}</p>
        <p>Ko ustvariš PostgreSQL bazo in zaženeš <code>Data/create.sql</code>, se bodo tukaj prikazali podatki.</p>
      </section>
    % end

    <section class="cards">
      % for r in restavracije:
        <article class="card">
          <h2>{{r["ime"]}}</h2>
          <p>{{r.get("ime_lokacije") or "Lokacija ni navedena"}}</p>
          % naslov = " ".join([x for x in [r.get("ulica"), r.get("hisna_stevilka")] if x])
          % if naslov:
            <p>{{naslov}}</p>
          % end
          % if r.get("spletna_stran"):
            <a href="{{r['spletna_stran']}}" target="_blank" rel="noreferrer">Spletna stran</a>
          % end
        </article>
      % end
    </section>
  </main>
</body>
</html>
