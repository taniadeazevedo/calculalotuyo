# Genera las páginas SEO del calendario 2027 a partir de festivos-2027.js (datos del BOE)
import datetime as dt, glob, json, os, re, html as H
S = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.expanduser('~/Desktop/calculalotuyo'))
HOY = '2026-10-18'
CSS = re.search(r'styles(?:\.min)?\.css\?v=[0-9a-z]+', open('index.html', encoding='utf-8').read()).group(0)
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
SEM = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
D = dt.date
fecha = lambda k: D.fromisoformat(k)
larga = lambda d: f'{SEM[d.weekday()]} {d.day} de {MESES[d.month - 1]}'          # "jueves 25 de marzo"
cap = lambda t: t[0].upper() + t[1:]

# ---------------------------------------------------------------- datos
js = open('festivos-2027.js', encoding='utf-8').read()
CCAA = {}
for slug, nombre, cuerpo in re.findall(r"'([a-z-]+)':\{nombre:'([^']+)',festivos:\[(.*?)\]\}", js, re.S):
    CCAA[slug] = {'nombre': nombre, 'festivos': dict(re.findall(r"\['(\d{4}-\d\d-\d\d)','((?:[^'\\]|\\.)*)'\]", cuerpo))}
NOTAS = dict(re.findall(r"\n\s+(\w+):'((?:[^'\\]|\\.)*)'", js[js.index('NOTAS_2027'):]))
boe = json.load(open(f'{S}/boe/f2027.json'))
boe_slug = {'Andalucía': 'andalucia', 'Aragón': 'aragon', 'Asturias': 'asturias', 'Illes Balears': 'baleares', 'Canarias': 'canarias', 'Cantabria': 'cantabria', 'Castilla-La Mancha': 'castilla-la-mancha', 'Castilla y León': 'castilla-y-leon', 'Cataluña': 'cataluna', 'Extremadura': 'extremadura', 'Galicia': 'galicia', 'Com. de Madrid': 'madrid', 'Región Murcia': 'murcia', 'C. Foral Navarra': 'navarra', 'País Vasco': 'pais-vasco', 'La Rioja': 'la-rioja', 'Comunitat Valenciana': 'valencia', 'Ciudad de Ceuta': 'ceuta', 'Ciudad de Melilla': 'melilla'}
for k, v in boe.items():
    CCAA[boe_slug[k]]['propios'] = {f for f, n, m in v if m == '***'}   # fiestas propias de la comunidad
ORDEN = sorted(CCAA, key=lambda s: CCAA[s]['nombre'])
COMUNES = {k: n for k, n in CCAA['madrid']['festivos'].items() if all(k in CCAA[s]['festivos'] for s in CCAA)}
assert len(COMUNES) == 9, COMUNES
# nombre corto para enlaces y títulos ("Madrid" en vez de "Comunidad de Madrid")
CORTO = {s: CCAA[s]['nombre'].replace('Comunidad de ', '').replace('Región de ', '') for s in CCAA}

entre_semana = lambda fest: [k for k in fest if fecha(k).weekday() < 5]
def laborables_mes(fest, m):
    n = 0
    d = D(2027, m, 1)
    while d.month == m:
        if d.weekday() < 5 and d.isoformat() not in fest: n += 1
        d += dt.timedelta(days=1)
    return n

# ---------------------------------------------------------------- puentes (misma lógica que la calculadora)
def puentes(fest):
    dias = []
    d = D(2026, 12, 26)
    while d <= D(2028, 1, 6):
        k = d.isoformat(); f = fest.get(k)
        dias.append({'d': d, 'libre': d.weekday() >= 5 or bool(f), 'fest': f, 'es': bool(f) and d.weekday() < 5})
        d += dt.timedelta(days=1)
    bloques = []
    for i, x in enumerate(dias):
        if not x['libre']: continue
        if bloques and bloques[-1][1] == i - 1: bloques[-1][1] = i
        else: bloques.append([i, i])
    cand = []
    for a in range(len(bloques)):
        coger = []
        for b in range(a, len(bloques)):
            if b > a: coger += list(range(bloques[b - 1][1] + 1, bloques[b][0]))
            if len(coger) > 4: break
            tramo = dias[bloques[a][0]:bloques[b][1] + 1]
            nombres = list(dict.fromkeys(x['fest'] for x in tramo if x['es']))
            if not nombres: continue
            if tramo[0]['d'].year != 2027 and tramo[-1]['d'].year != 2027: continue
            if not coger and len(tramo) < 3: continue
            if coger and len(tramo) < 2.5 * len(coger): continue
            cand.append({'ini': tramo[0]['d'], 'fin': tramo[-1]['d'], 'dias': len(tramo), 'coger': [dias[i]['d'] for i in coger], 'nombre': ' y '.join(nombres), 'a': bloques[a][0], 'b': bloques[b][1]})
    sol = lambda x, y: x['a'] <= y['b'] and y['a'] <= x['b']
    mejor = lambda x, y: len(x['coger']) <= len(y['coger']) and x['dias'] >= y['dias'] and (len(x['coger']) < len(y['coger']) or x['dias'] > y['dias'])
    r = [c for c in cand if not any(o is not c and sol(o, c) and mejor(o, c) for o in cand)]
    return sorted(r, key=lambda c: (c['ini'], len(c['coger'])))

def tarjeta(p, fest):
    tira = ''
    d = p['ini']
    coger = {x.isoformat() for x in p['coger']}
    while d <= p['fin']:
        k = d.isoformat()
        clase = 'cal-festivo' if k in fest else 'cal-puente' if k in coger else 'cal-finde'
        tira += f'<span class="tira-dia {clase}"><small>{"LMXJVSD"[d.weekday()]}</small>{d.day}</span>'
        d += dt.timedelta(days=1)
    n = len(p['coger'])
    pides = f'Si pides <strong>{n} {"día" if n == 1 else "días"}</strong> de vacaciones' if n else '<strong>Sin gastar vacaciones</strong>'
    return f'<div class="puente{"" if n else " puente-gratis"}"><div class="puente-dias"><strong>{p["dias"]}</strong><span>días libres</span></div><div class="puente-info"><p class="puente-nombre">{H.escape(p["nombre"])}</p><p>{pides}</p></div><div class="tira">{tira}</div></div>'

# ---------------------------------------------------------------- calendario estático
def calendario(fest, puente=set(), meses=range(1, 13)):
    out = []
    for m in meses:
        primero = D(2027, m, 1)
        celdas = ''.join(f'<span class="cal-dia cal-cab">{l}</span>' for l in 'LMXJVSD')
        celdas += '<span class="cal-dia"></span>' * primero.weekday()
        d = primero
        while d.month == m:
            k = d.isoformat()
            clase = 'cal-festivo' if k in fest else 'cal-puente' if k in puente else 'cal-finde' if d.weekday() >= 5 else ''
            t = f' title="{H.escape(fest[k])}"' if k in fest else ''
            celdas += f'<span class="cal-dia {clase}"{t}>{d.day}</span>'
            d += dt.timedelta(days=1)
        out.append(f'<div class="cal-mes"><h4>{cap(MESES[m - 1])}</h4><div class="cal-grid">{celdas}</div></div>')
    return '<div class="cal-anual">' + ''.join(out) + '</div>'
LEYENDA = '<div class="cal-leyenda"><span><i class="cal-festivo"></i>Festivo</span><span><i class="cal-puente"></i>Día puente: si lo pides, enlazas días libres</span><span><i class="cal-finde"></i>Fin de semana</span></div>'

# ---------------------------------------------------------------- plantilla
v = open('vacaciones.html', encoding='utf-8').read()
NAV = v[v.index('<body>') + len('<body>\n'):v.index('<main>')]
NAV = NAV.replace(' aria-current="page"', '').replace('class="nav-link active" data-dropdown-btn>Nómina', 'class="nav-link" data-dropdown-btn>Nómina')
NAV = NAV.replace('class="nav-link" data-dropdown-btn>📅 Calendario', 'class="nav-link active" data-dropdown-btn>📅 Calendario')
FOOT = v[v.index('<footer'):v.index('<script src="site.js')]
FAQ_HTML = lambda faqs: ''.join(f'<div class="faq-item"><button class="faq-q"><span>{q}</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faqs)
limpio = lambda t: re.sub(r'<[^>]+>', '', t)

def pagina(slug, titulo, desc, keywords, miga, cuerpo, faqs, fuente):
    ld_faq = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': limpio(q), 'acceptedAnswer': {'@type': 'Answer', 'text': limpio(a)}} for q, a in faqs]}, ensure_ascii=False, indent=1)
    migas = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': 'https://calculalotuyo.es/'}]
    if slug != 'calendario-laboral-2027':
        migas.append({'@type': 'ListItem', 'position': 2, 'name': 'Calendario laboral 2027', 'item': 'https://calculalotuyo.es/calendario-laboral-2027'})
    migas.append({'@type': 'ListItem', 'position': len(migas) + 1, 'name': miga})
    ld_miga = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': migas}, ensure_ascii=False, indent=1)
    t, dsc = H.escape(titulo), H.escape(desc)
    head = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-4853214655991551">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4853214655991551" crossorigin="anonymous"></script>
    <meta name="description" content="{dsc}">
    <meta name="keywords" content="{H.escape(keywords)}">
    <title>{t}</title>
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://calculalotuyo.es/{slug}">
    <meta property="og:title" content="{t}">
    <meta property="og:description" content="{dsc}">
    <meta property="og:site_name" content="CalculaLoTuyo">
    <meta property="og:locale" content="es_ES">
    <meta name="twitter:card" content="summary_large_image">
    <meta property="og:image" content="https://calculalotuyo.es/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:image" content="https://calculalotuyo.es/og-image.png">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <meta name="theme-color" content="#0F766E">
    <link rel="canonical" href="https://calculalotuyo.es/{slug}">
    <link rel="stylesheet" href="{CSS}">
    <script type="application/ld+json">
{ld_faq}
    </script>
    <script type="application/ld+json">
{ld_miga}
    </script>
</head>
<body class="tema-calendario">
'''
    nav = NAV.replace(f'<a href="{slug}">', f'<a href="{slug}" aria-current="page">').replace(f'<a href="{slug}" class="mobile-nav-link">', f'<a href="{slug}" class="mobile-nav-link" aria-current="page">')
    migas_html = '<a href="./">Inicio</a> <span class="breadcrumb-sep">›</span> '
    if slug != 'calendario-laboral-2027':
        migas_html += '<a href="calendario-laboral-2027">Calendario laboral 2027</a> <span class="breadcrumb-sep">›</span> '
    cuerpo = cuerpo.replace('{{MIGAS}}', f'<nav class="breadcrumb" aria-label="Estás en">{migas_html}<span aria-current="page">{miga}</span></nav>')
    faq = f'''
    <section class="section section-alt"><div class="container"><h2 class="section-title">❓ Preguntas frecuentes</h2>
        <div class="faq-list">{FAQ_HTML(faqs)}</div>
    </div></section>
    <section class="section"><div class="container"><div class="source-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg><div><strong>Fuente:</strong><p>{fuente}</p></div></div></div></section>
</main>
'''
    todo = head + nav + '<main>\n' + cuerpo + faq + '\n' + FOOT + '<script src="site.js?v=20261019a"></script>\n</body>\n</html>\n'
    todo = todo.replace(' de el ', ' del ').replace(' a el ', ' al ').replace('En 2027, la ', 'En 2027, la ').replace('>En 2027, el ', '>En 2027, el ')
    open(f'{slug}.html', 'w', encoding='utf-8').write(todo)
    return slug

FUENTE_BOE = '<a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-21254" target="_blank">Resolución de 8 de octubre de 2026</a> de la Dirección General de Trabajo, por la que se publica la relación de fiestas laborales para el año 2027 (BOE núm. 254, de 13 de octubre de 2026).'
REVISADO = '<p class="hero-meta">📅 Revisado el 18 de octubre de 2026 · ✍️ <a href="sobre-el-proyecto">CalculaLoTuyo</a></p>'
def hero(miga_html_placeholder, h1, sub, p):
    return f'    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📅 Calendario 2027</div><h1>{h1}<br><span class="highlight">{sub}</span></h1><p>{p}</p>\n            {REVISADO}</div></section>\n'
def resumen(cifras):
    return '<div class="cal-resumen">' + ''.join(f'<div><strong>{n}</strong><span>{t}</span></div>' for n, t in cifras) + '</div>'
def tarjetas(lista):
    return '<div class="puentes-lista">' + ''.join(lista) + '</div>'
ENLACES_CAL = lambda excluir='': '<div class="enlaces-ccaa">' + ''.join(f'<a href="calendario-laboral-2027-{s}">{CORTO[s]}</a>' for s in ORDEN if s != excluir) + '</div>'
AD = '\n    <div class="container"><div class="ad"></div></div>\n'
generadas = []

# ================================================================ 1) PÁGINA PRINCIPAL
fest_es = COMUNES
lab_es = sum(laborables_mes(fest_es, m) for m in range(1, 13))
p_es = puentes(fest_es)
filas_ccaa = ''.join(f'<tr><td><a href="calendario-laboral-2027-{s}">{CCAA[s]["nombre"]}</a></td><td>{len(CCAA[s]["festivos"])}</td><td>{len(entre_semana(CCAA[s]["festivos"]))}</td><td>{sum(laborables_mes(CCAA[s]["festivos"], m) for m in range(1, 13))}</td></tr>' for s in ORDEN)
filas_nac = ''.join(f'<tr><td>{cap(larga(fecha(k)))}</td><td>{H.escape(n)}</td></tr>' for k, n in sorted(COMUNES.items()))
cuerpo = hero('', 'Calendario laboral 2027', 'festivos de toda España', 'Los festivos oficiales de 2027 de un vistazo. Elige tu comunidad para ver los tuyos.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        <h2 class="puentes-titulo" style="margin-top:0">📍 Elige tu comunidad</h2>
        {ENLACES_CAL()}
        {resumen([(len(fest_es), 'festivos en toda España'), (len(entre_semana(fest_es)), 'entre semana'), (lab_es, 'días laborables*')])}
        <h2 class="puentes-titulo">🗓️ Festivos comunes a toda España en 2027</h2>
        {LEYENDA}
        {calendario(fest_es, {d.isoformat() for p in p_es if len(p['coger']) == 1 for d in p['coger']})}
        <p class="nota-corta">* De lunes a viernes, sin contar los festivos propios de cada comunidad ni las 2 fiestas locales.</p>
        <div class="result-actions"><a href="puentes-2027" class="btn">🏖️ Calcular mis puentes de 2027</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📋 Los 9 festivos que hay en toda España en 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Fecha</th><th>Festivo</th></tr></thead><tbody>{filas_nac}</tbody></table></div>
<p>Además, cada comunidad tiene sus propios festivos (hasta completar 12) y cada municipio <strong>2 fiestas locales</strong>. El 1 de mayo y el 25 de diciembre caen en sábado, y el 15 de agosto en domingo.</p>
<h2>🗺️ Festivos y días laborables de 2027 por comunidad</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Comunidad</th><th>Festivos</th><th>Entre semana</th><th>Días laborables*</th></tr></thead><tbody>{filas_ccaa}</tbody></table></div>
<p class="nota-corta">* De lunes a viernes, sin contar las 2 fiestas locales de cada municipio.</p>
<h2>🏖️ Los mejores puentes de 2027</h2>
{tarjetas([tarjeta(p, fest_es) for p in p_es if len(p['coger']) <= 3 and p['dias'] >= 4])}
<h2>📚 Más sobre el calendario de 2027</h2>
<ul>
<li><a href="semana-santa-2027">Semana Santa 2027</a>: fechas y qué días son festivos en cada comunidad.</li>
<li><a href="dias-laborables-2027">Días laborables de 2027</a>: cuántos hay cada mes y en cada comunidad.</li>
<li><a href="trabajar-en-festivo">Trabajar un festivo</a>: cuándo te lo pueden pedir y cómo se paga.</li>
<li><a href="puentes-2027">Calculadora de puentes 2027</a> y <a href="dias-laborables">calculadora de días laborables</a>.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Cuándo se publicó el calendario laboral de 2027?', 'El Ministerio de Trabajo lo publicó en el <strong>BOE del 13 de octubre de 2026</strong>, con los festivos nacionales y los de cada comunidad autónoma. Las 2 fiestas locales de cada municipio se publican después en los boletines de cada comunidad o provincia.'),
    ('¿Cuántos festivos hay en 2027?', f'Hay <strong>9 festivos en toda España</strong> y cada comunidad completa hasta <strong>12</strong> con los suyos. A ellos se suman las 2 fiestas locales: en total, como máximo, 14 al año.'),
    ('¿Qué festivos caen en fin de semana en 2027?', 'El <strong>1 de mayo</strong> y el <strong>25 de diciembre</strong> caen en sábado, y el <strong>15 de agosto</strong> en domingo. Por eso varias comunidades pasan el 15 de agosto al lunes 16.'),
    ('¿Cuál es el mejor puente de 2027?', 'El de diciembre: el 6 cae en lunes y el 8 en miércoles. Si pides el martes 7, descansas del sábado 4 al miércoles 8; si pides también el jueves 9 y el viernes 10, son <strong>9 días seguidos</strong>.'),
]
generadas.append(pagina('calendario-laboral-2027', 'Calendario laboral 2027: festivos de España y por comunidad', 'Calendario laboral 2027 con los festivos oficiales del BOE: los 9 comunes a toda España, los de cada comunidad autónoma, los puentes y los días laborables.', 'calendario laboral 2027, festivos 2027, festivos nacionales 2027, calendario 2027 España', 'Calendario laboral 2027', cuerpo, faqs, FUENTE_BOE))

# ================================================================ 2) UNA PÁGINA POR COMUNIDAD
SS = {'2027-03-25': 'Jueves Santo', '2027-03-29': 'Lunes de Pascua'}
for s in ORDEN:
    c = CCAA[s]; fest = c['festivos']; nom = c['nombre']; corto = CORTO[s]
    nom = {'madrid': 'la Comunidad de Madrid', 'murcia': 'la Región de Murcia', 'valencia': 'la Comunitat Valenciana', 'pais-vasco': 'el País Vasco'}.get(s, nom)   # con artículo dentro de las frases
    ps = puentes(fest)
    lab = [laborables_mes(fest, m) for m in range(1, 13)]
    propios = sorted(k for k in fest if k in c['propios'])
    nac_extra = sorted(k for k in fest if k not in COMUNES and k not in c['propios'])   # nacionales que la comunidad mantiene (Jueves Santo, San José, 16 de agosto…)
    lista_propios = '; '.join(f'{H.escape(fest[k])} ({larga(fecha(k))})' for k in propios)
    lista_extra = '; '.join(f'{H.escape(fest[k])} ({larga(fecha(k))})' for k in nac_extra)
    ss_tiene = [SS[k] for k in SS if k in fest]
    ss_txt = ('el ' + ' y el '.join(ss_tiene) + ' también son festivos' if len(ss_tiene) == 2 else f'el {ss_tiene[0]} también es festivo' if ss_tiene else 'solo es festivo el Viernes Santo')
    ss_dias = {('Jueves Santo', 'Lunes de Pascua'): 'del jueves 25 al lunes 29 de marzo (5 días seguidos)', ('Jueves Santo',): 'del jueves 25 al domingo 28 de marzo (4 días seguidos)', ('Lunes de Pascua',): 'del viernes 26 al lunes 29 de marzo (4 días seguidos)', (): 'del viernes 26 al domingo 28 de marzo (3 días)'}[tuple(ss_tiene)]
    mejor = max(ps, key=lambda p: (p['dias'] / max(1, len(p['coger'])) if p['coger'] else 0, p['dias'])) if any(p['coger'] for p in ps) else None
    finde = [k for k in fest if fecha(k).weekday() >= 5]
    # Puente gracias a una fiesta propia de la comunidad (lo que hace única a cada página)
    pp = [p for p in ps if any((p['ini'] + dt.timedelta(days=i)).isoformat() in {k for k in c['propios'] if fecha(k).weekday() < 5} - {'2027-03-29'} for i in range(p['dias']))]   # solo fiestas propias entre semana   # sin Semana Santa, que ya se cuenta antes
    frase_propio = ''
    if pp:
        p0 = min(pp, key=lambda p: (len(p['coger']), -p['dias']))
        n0 = len(p0['coger'])
        como = f'si pides {n0} {"día" if n0 == 1 else "días"} de vacaciones' if n0 else 'sin gastar vacaciones'
        frase_propio = f' Y gracias a {"sus fiestas propias" if len(c["propios"]) > 1 else "su fiesta propia"}, {como} tienes otro puente de {p0["dias"]} días, del {larga(p0["ini"])} al {larga(p0["fin"])}.'
    filas = ''.join(f'<tr><td>{cap(larga(fecha(k)))}</td><td>{H.escape(n)}</td><td>{"Propio de " + corto if k in c["propios"] else "Nacional"}</td></tr>' for k, n in sorted(fest.items()))
    filas_lab = ''.join(f'<tr><td>{cap(MESES[m])}</td><td>{lab[m]}</td></tr>' for m in range(12))
    mas = max(range(12), key=lambda m: lab[m]); menos = min(range(12), key=lambda m: lab[m])
    nota = f'<div class="aviso-ccaa">ℹ️ {NOTAS[s]}</div>' if s in NOTAS else ''
    sin_paren = lambda t: t.replace(' (15 de agosto)', '')        # evita paréntesis dentro de paréntesis
    extras = [f'{H.escape(sin_paren(fest[k]))} ({larga(fecha(k))})' for k in sorted(set(propios) | set(nac_extra))]
    lista_y = ', '.join(extras[:-1]) + ' y ' + extras[-1] if len(extras) > 1 else (extras[0] if extras else '')
    intro = f'<p>En 2027, {nom} tiene <strong>{len(fest)} festivos</strong>: los {len([k for k in fest if k in COMUNES])} comunes a toda España'
    intro += f' y, además, {lista_y}' if extras else ''
    intro += f'. <strong>{len(entre_semana(fest))} caen entre semana</strong>'
    intro += f' y {len(finde)} en fin de semana' if finde else ''
    intro += '.</p>'
    cuerpo = hero('', f'Calendario laboral 2027 {corto}', 'festivos y puentes', f'Los {len(fest)} festivos de {nom} en 2027, según el BOE, y los puentes que puedes aprovechar.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        {resumen([(len(fest), 'festivos'), (len(entre_semana(fest)), 'entre semana'), (sum(lab), 'días laborables*')])}
        {nota}
        <h2 class="puentes-titulo">🗓️ Calendario 2027 · {c['nombre']}</h2>
        {LEYENDA}
        {calendario(fest, {d.isoformat() for p in ps if len(p['coger']) == 1 for d in p['coger']})}
        <p class="nota-corta">* De lunes a viernes, sin contar las 2 fiestas locales de tu municipio.</p>
        <div class="result-actions"><a href="puentes-2027?ccaa={s}" class="btn">🏖️ Añadir mis fiestas locales y ver mis puentes</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🎉 Festivos de {nom} en 2027</h2>
{intro}
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Fecha</th><th>Festivo</th><th>Tipo</th></tr></thead><tbody>{filas}</tbody></table></div>
<p>A estos se suman las <strong>2 fiestas locales</strong> de cada municipio, que se publican en el boletín oficial de la comunidad o de la provincia.</p>
<h2>🏖️ Puentes de 2027 en {nom}</h2>
<p>{"El puente que más compensa es <strong>" + H.escape(mejor["nombre"]) + "</strong>: si pides " + str(len(mejor["coger"])) + (" día" if len(mejor["coger"]) == 1 else " días") + " de vacaciones, descansas " + str(mejor["dias"]) + " días seguidos." if mejor else ""} En Semana Santa {ss_txt}, así que descansas {ss_dias}.{frase_propio}</p>
{tarjetas([tarjeta(p, fest) for p in ps])}
<h2>💼 Días laborables por mes en {nom}</h2>
<p>En 2027 hay <strong>{sum(lab)} días laborables</strong> de lunes a viernes en {nom}. El mes con más es {MESES[mas]} ({lab[mas]}) y el que menos, {MESES[menos]} ({lab[menos]}). Si tu municipio tiene sus 2 fiestas locales entre semana, resta 2.</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Mes</th><th>Días laborables</th></tr></thead><tbody>{filas_lab}</tbody></table></div>
<h2>🗺️ Calendario laboral 2027 de otras comunidades</h2>
{ENLACES_CAL(s)}
<p>¿Necesitas contar días entre dos fechas? Usa la <a href="dias-laborables">calculadora de días laborables</a>. Y si tienes que trabajar un festivo, mira <a href="trabajar-en-festivo">cómo se paga</a>.</p>
</article></div></section>
'''
    faqs = [
        (f'¿Cuántos festivos hay en {nom} en 2027?', f'Hay <strong>{len(fest)} festivos</strong> en {nom} en 2027, más las 2 fiestas locales de cada municipio. {len(entre_semana(fest))} de los {len(fest)} caen entre semana.'),
        (f'¿Es festivo el Jueves Santo de 2027 en {nom}?', ('Sí. ' if '2027-03-25' in fest else 'No. ') + f'En {nom}, en Semana Santa {ss_txt}, así que descansas {ss_dias}.'),
        (f'¿Cuántos días laborables tiene 2027 en {nom}?', f'<strong>{sum(lab)} días</strong> de lunes a viernes, quitando los festivos de la comunidad. Si las 2 fiestas locales de tu municipio caen entre semana, quedan {sum(lab) - 2}.'),
    ]
    if propios:
        faqs.insert(1, (f'¿Cuál es la fiesta propia de {nom} en 2027?', f'{cap(lista_propios)}.'))
    generadas.append(pagina(f'calendario-laboral-2027-{s}', f'Calendario laboral 2027 {corto}: festivos y puentes' if len(corto) < 18 else f'Calendario laboral 2027 {corto}: festivos', f'Festivos de {nom} en 2027 según el BOE ({len(fest)} días), puentes que puedes aprovechar y días laborables por mes. Con calendario visual.', f'calendario laboral 2027 {corto.lower()}, festivos 2027 {corto.lower()}, puentes 2027 {corto.lower()}, días laborables 2027 {corto.lower()}', corto, cuerpo, faqs, FUENTE_BOE))

# ================================================================ 3) SEMANA SANTA 2027
filas_ss = ''
for s in ORDEN:
    f = CCAA[s]['festivos']
    j, l = '2027-03-25' in f, '2027-03-29' in f
    seguidos = 3 + (1 if j else 0) + (1 if l else 0)
    filas_ss += f'<tr><td><a href="calendario-laboral-2027-{s}">{CCAA[s]["nombre"]}</a></td><td>{"✅" if j else "—"}</td><td>✅</td><td>{"✅" if l else "—"}</td><td><strong>{seguidos}</strong></td></tr>'
ss_fest = {'2027-03-25': 'Jueves Santo', '2027-03-26': 'Viernes Santo', '2027-03-29': 'Lunes de Pascua'}
ej = tarjetas([
    tarjeta({'ini': D(2027, 3, 25), 'fin': D(2027, 3, 28), 'dias': 4, 'coger': [], 'nombre': 'Casi toda España'}, ss_fest),
    tarjeta({'ini': D(2027, 3, 25), 'fin': D(2027, 3, 29), 'dias': 5, 'coger': [], 'nombre': 'Baleares, Navarra, País Vasco y La Rioja'}, ss_fest),
    tarjeta({'ini': D(2027, 3, 20), 'fin': D(2027, 3, 28), 'dias': 9, 'coger': [D(2027, 3, 22), D(2027, 3, 23), D(2027, 3, 24)], 'nombre': 'Semana entera antes de Pascua'}, ss_fest),
])
cuerpo = hero('', 'Semana Santa 2027', 'del 25 al 28 de marzo', 'Qué días son festivos en cada comunidad y cuántos días seguidos puedes descansar.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        {resumen([('25', 'Jueves Santo'), ('26', 'Viernes Santo'), ('29', 'Lunes de Pascua')])}
        <h2 class="puentes-titulo">🗓️ Marzo y abril de 2027</h2>
        <div class="cal-leyenda"><span><i class="cal-festivo"></i>Festivo (en casi toda España)</span><span><i class="cal-puente"></i>Lunes de Pascua (solo en algunas comunidades)</span><span><i class="cal-finde"></i>Fin de semana</span></div>
        {calendario({'2027-03-25': 'Jueves Santo', '2027-03-26': 'Viernes Santo'}, {'2027-03-29'}, range(3, 5))}
        <h2 class="puentes-titulo">🏖️ Cuántos días seguidos puedes descansar</h2>
        {ej}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📅 Fechas de la Semana Santa de 2027</h2>
<p>En 2027 la Semana Santa cae pronto, en <strong>marzo</strong>: el Domingo de Ramos es el 21, el <strong>Jueves Santo el 25</strong>, el <strong>Viernes Santo el 26</strong>, el Domingo de Resurrección el 28 y el <strong>Lunes de Pascua el 29</strong>. En 2026 fue a principios de abril.</p>
<h2>🗺️ Qué días son festivos en cada comunidad</h2>
<p>El Viernes Santo es festivo en toda España. El Jueves Santo lo es en todas las comunidades menos Cataluña y la Comunitat Valenciana, que en su lugar tienen el Lunes de Pascua.</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-ss"><thead><tr><th>Comunidad</th><th>Jueves 25</th><th>Viernes 26</th><th>Lunes 29</th><th>Días seguidos</th></tr></thead><tbody>{filas_ss}</tbody></table></div>
<p class="nota-corta">Días seguidos de descanso contando el fin de semana, sin pedir vacaciones. Algunos municipios tienen además una fiesta local en Semana Santa.</p>
<h2>❔ Por qué la Semana Santa cambia cada año</h2>
<p>El Domingo de Resurrección es el primer domingo después de la primera luna llena de primavera. Por eso puede caer entre el 22 de marzo y el 25 de abril, y con él se mueven el Jueves y el Viernes Santo.</p>
<p>Consulta todos los festivos en el <a href="calendario-laboral-2027">calendario laboral 2027</a> o calcula tus puentes del año en la <a href="puentes-2027">calculadora de puentes</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿Cuándo es Semana Santa en 2027?', 'Del <strong>domingo 21 al domingo 28 de marzo</strong> de 2027. El Jueves Santo es el 25, el Viernes Santo el 26 y el Lunes de Pascua el 29.'),
    ('¿Es festivo el Jueves Santo de 2027?', 'Sí en todas las comunidades <strong>menos Cataluña y la Comunitat Valenciana</strong>.'),
    ('¿Dónde es festivo el Lunes de Pascua de 2027?', 'En <strong>Baleares, Cataluña, Navarra, País Vasco, La Rioja y la Comunitat Valenciana</strong>.'),
    ('¿Cuántos días de vacaciones hay que pedir para tener la Semana Santa entera?', 'En casi toda España, pidiendo el <strong>lunes 22, el martes 23 y el miércoles 24</strong> enlazas 9 días seguidos, del sábado 20 al domingo 28.'),
]
generadas.append(pagina('semana-santa-2027', 'Semana Santa 2027: fechas y festivos por comunidad', 'Semana Santa 2027: Jueves Santo 25 de marzo, Viernes Santo 26 y Lunes de Pascua 29. Qué días son festivos en cada comunidad y cuántos días seguidos descansas.', 'semana santa 2027, cuándo es semana santa 2027, jueves santo 2027, lunes de pascua 2027 festivo', 'Semana Santa 2027', cuerpo, faqs, FUENTE_BOE))

# ================================================================ 4) DÍAS LABORABLES 2027
lab_es_mes = [laborables_mes(COMUNES, m) for m in range(1, 13)]
dias_lv = [sum(1 for i in range(31) if (D(2027, m, 1) + dt.timedelta(days=i)).month == m and (D(2027, m, 1) + dt.timedelta(days=i)).weekday() < 5) for m in range(1, 13)]
filas_mes = ''.join(f'<tr><td>{cap(MESES[m])}</td><td>{dias_lv[m]}</td><td><strong>{lab_es_mes[m]}</strong></td></tr>' for m in range(12))
tot = {s: sum(laborables_mes(CCAA[s]['festivos'], m) for m in range(1, 13)) for s in ORDEN}
maxc = max(tot.values()); minc = min(tot.values())
barras = ''.join(f'<div class="barra-fila"><span class="barra-nombre">{cap(MESES[m][:3])}</span><span class="barra" style="width:{lab_es_mes[m] / 23 * 100:.0f}%">{lab_es_mes[m]}</span></div>' for m in range(12))
cuerpo = hero('', 'Días laborables 2027', f'{lab_es} en toda España', 'Cuántos días se trabaja cada mes de 2027 y en cada comunidad autónoma.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        {resumen([(sum(dias_lv), 'días de lunes a viernes'), (len(entre_semana(COMUNES)), 'festivos comunes entre semana'), (lab_es, 'días laborables')])}
        <h2 class="puentes-titulo">📊 Días laborables por mes (toda España)</h2>
        <div class="barras">{barras}</div>
        <p class="nota-corta">Solo se descuentan los festivos comunes a toda España. Cada comunidad tiene entre {minc} y {maxc}: mira la tabla de abajo.</p>
        <div class="result-actions"><a href="dias-laborables" class="btn">📅 Contar días laborables entre dos fechas</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📅 Días laborables de cada mes de 2027</h2>
<p>2027 empieza en viernes y no es bisiesto, así que tiene <strong>{sum(dias_lv)} días de lunes a viernes</strong>. Si quitamos los {len(entre_semana(COMUNES))} festivos comunes que caen entre semana, quedan <strong>{lab_es}</strong>. Después, cada comunidad resta los suyos.</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Mes</th><th>Lunes a viernes</th><th>Laborables</th></tr></thead><tbody>{filas_mes}</tbody></table></div>
<h2>🗺️ Días laborables de 2027 en cada comunidad</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Comunidad</th><th>Días laborables</th></tr></thead><tbody>{"".join(f'<tr><td><a href="calendario-laboral-2027-{s}">{CCAA[s]["nombre"]}</a></td><td>{tot[s]}</td></tr>' for s in ORDEN)}</tbody></table></div>
<p class="nota-corta">Sin contar las 2 fiestas locales de cada municipio: si caen entre semana, resta 2.</p>
<h2>❔ Si trabajas los sábados</h2>
<p>En comercio, hostelería y otros sectores el sábado es laborable. En ese caso suma los sábados del año ({sum(1 for i in range(365) if (D(2027, 1, 1) + dt.timedelta(days=i)).weekday() == 5)} en 2027) y vuelve a restar los festivos que caen en sábado. La <a href="dias-laborables">calculadora de días laborables</a> lo hace sola si eliges «de lunes a sábado».</p>
</article></div></section>
'''
faqs = [
    ('¿Cuántos días laborables tiene 2027?', f'<strong>{lab_es}</strong> de lunes a viernes quitando los festivos comunes a toda España. Con los festivos de cada comunidad quedan entre <strong>{minc} y {maxc}</strong>, y luego hay que restar las 2 fiestas locales.'),
    ('¿Qué mes de 2027 tiene más días laborables?', f'{cap(MESES[max(range(12), key=lambda m: lab_es_mes[m])])}, con {max(lab_es_mes)} días laborables. El que menos tiene es {MESES[min(range(12), key=lambda m: lab_es_mes[m])]}, con {min(lab_es_mes)}.'),
    ('¿El sábado es día laborable?', 'Depende de tu calendario de trabajo. Para los plazos con la Administración, el sábado es <strong>inhábil</strong> (Ley 39/2015). Para tu empresa, es laborable si tu horario o tu convenio lo incluyen.'),
]
generadas.append(pagina('dias-laborables-2027', 'Días laborables 2027: por meses y por comunidad', f'2027 tiene {lab_es} días laborables en toda España. Cuántos hay en cada mes y en cada comunidad autónoma, según los festivos del BOE.', 'días laborables 2027, cuántos días laborables tiene 2027, días laborables por mes 2027, días hábiles 2027', 'Días laborables 2027', cuerpo, faqs, FUENTE_BOE + ' Para los días hábiles administrativos: art. 30 de la <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565" target="_blank">Ley 39/2015</a>.'))

# ================================================================ 5) TRABAJAR EN FESTIVO
cuerpo = hero('', 'Trabajar un festivo', '¿cómo se paga?', 'Cuándo te lo pueden pedir, cuánto se cobra y qué pasa si el festivo cae en tu día libre.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        {resumen([('+75 %', 'de recargo mínimo por hora'), ('o 1 día', 'de descanso a cambio')])}
        <h2 class="puentes-titulo">🧮 Ejemplo: 8 horas un festivo</h2>
        <div class="calc-steps">
            <div class="calc-step"><span class="step-num">1</span><div><strong>Precio de tu hora normal:</strong><p>12 € la hora</p></div></div>
            <div class="calc-step"><span class="step-num">2</span><div><strong>Con el 75 % de recargo:</strong><p>12 € × 1,75 = <strong>21 € la hora</strong></p></div></div>
            <div class="calc-step"><span class="step-num">3</span><div><strong>Por las 8 horas:</strong><p>21 € × 8 = <strong>168 €</strong>, además de tu sueldo de esa semana</p></div></div>
        </div>
        <p class="nota-corta">O, en lugar de cobrarlo, te dan otro día de descanso. Tu convenio puede concretar cómo se compensa.</p>
        <div class="result-actions"><a href="horas-extra" class="btn">⏰ Calcular el precio de tu hora</a></div>
    </div></div></section>
''' + AD + '''
    <section class="section"><div class="container"><article class="seo-section">
<h2>⚖️ Qué dice la ley</h2>
<p>Los festivos son días de descanso <strong>pagados y que no se recuperan</strong> (art. 37.2 del Estatuto de los Trabajadores). Si por razones técnicas u organizativas no puedes descansar un festivo, el art. 47 del Real Decreto 2001/1983 obliga a la empresa a una de estas dos cosas:</p>
<ul><li><strong>Pagarte las horas trabajadas con un recargo de al menos el 75 %</strong>, además del sueldo normal de esa semana.</li><li><strong>Darte un descanso compensatorio</strong>: otro día libre en su lugar.</li></ul>
<p>Muchos convenios concretan cuánto se paga o cuándo se disfruta ese descanso. Mira el tuyo antes de hacer cuentas.</p>
<h2>🏨 ¿Te pueden obligar a trabajar un festivo?</h2>
<p>En sectores que funcionan todos los días, como hostelería, comercio, sanidad o transporte, trabajar algunos festivos suele formar parte de la jornada pactada en el contrato o en el convenio. En el resto, la empresa solo puede pedirlo de forma excepcional y, en todo caso, tiene que compensarlo.</p>
<h2>📅 Festivos en tu día libre, en domingo o en vacaciones</h2>
<ul><li><strong>Si un festivo cae en domingo:</strong> la comunidad autónoma puede pasarlo al lunes o cambiarlo por otra fiesta. Mira el <a href="calendario-laboral-2027">calendario laboral 2027</a> de tu comunidad.</li><li><strong>Si cae en tu día libre</strong> (por ejemplo, si trabajas a turnos): depende de tu convenio. Muchos dan un día de descanso a cambio, pero la ley no lo exige en todos los casos.</li><li><strong>Si cae durante tus vacaciones:</strong> si tus vacaciones se cuentan en días laborables, el festivo no te gasta un día. Si se cuentan en días naturales, sí cuenta. Lo explicamos en la <a href="vacaciones">calculadora de vacaciones</a>.</li></ul>
<h2>🧾 Festivo trabajado y horas extra</h2>
<p>Trabajar un festivo no es lo mismo que hacer horas extra. Las horas extra son las que pasan de tu jornada; el festivo trabajado se paga aparte con su propio recargo. Si además superas tu jornada, esas horas pueden ser también extraordinarias. Calcula cuánto valen en la <a href="horas-extra">calculadora de horas extra</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿Cómo se paga un festivo trabajado?', 'Con un recargo de <strong>al menos el 75 %</strong> sobre el precio de tu hora normal, además del sueldo de esa semana, salvo que la empresa te dé otro día de descanso a cambio (art. 47 del Real Decreto 2001/1983). Tu convenio puede concretarlo.'),
    ('¿Se cobra el doble por trabajar un festivo?', 'No necesariamente. La norma fija un recargo mínimo del 75 %, no del 100 %. Algunos convenios pagan más: revisa el tuyo.'),
    ('¿Pueden darme un día libre en vez de pagarme el festivo?', 'Sí. La ley permite compensar el festivo trabajado con un <strong>descanso compensatorio</strong> en lugar de pagarlo con recargo.'),
    ('¿Qué pasa si un festivo cae en domingo?', 'La comunidad autónoma puede trasladarlo al lunes o sustituirlo por otra fiesta propia. En 2027 pasa con el 15 de agosto: varias comunidades lo mueven al lunes 16.'),
]
generadas.append(pagina('trabajar-en-festivo', 'Trabajar un festivo: cómo se paga y tus derechos', 'Si trabajas un festivo, la empresa debe pagarte las horas con al menos un 75 % de recargo o darte otro día libre. Qué dice la ley, ejemplos y casos especiales.', 'trabajar en festivo, festivo trabajado cómo se paga, cobrar festivo trabajado, festivo en domingo, festivo en vacaciones', 'Trabajar un festivo', cuerpo, faqs, 'Art. 37.2 del <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430" target="_blank">Estatuto de los Trabajadores</a> y art. 47 del <a href="https://www.boe.es/buscar/act.php?id=BOE-A-1983-20906" target="_blank">Real Decreto 2001/1983</a>.'))

print('\n'.join(generadas))
json.dump(generadas, open(f'{S}/generadas.json', 'w'))
