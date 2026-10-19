# Genera las páginas «X euros brutos en netos» y la tabla general, con los datos de sueldos.json
# (que calcula calcular.js con el mismo motor que la calculadora de sueldo neto).
# Uso: node _herramientas/sueldos/calcular.js && python3 _herramientas/sueldos/gen-sueldos.py
import json, os, re, html as H
AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(AQUI, '..', '..'))
CSS = re.search(r'styles(?:\.min)?\.css\?v=[0-9a-z]+', open('index.html', encoding='utf-8').read()).group(0)
R = json.load(open(f'{AQUI}/sueldos.json'))
DAT = {int(k): v for k, v in R['datos'].items()}
SMI = R['smi']
# Sueldos que tienen página propia (los más buscados)
PAGINAS = [18000, 20000, 21000, 22000, 24000, 25000, 26000, 27000, 28000, 30000, 32000, 33000, 35000, 36000, 38000, 40000, 42000, 45000, 50000, 55000, 60000, 70000, 80000]

def e(n, dec=0):                                   # 1927.5 → "1.928" (formato español, con punto de miles)
    t = f'{n:,.{dec}f}'
    return t.replace(',', 'X').replace('.', ',').replace('X', '.')
def pct(n):
    return f'{n:.2f}'.replace('.', ',') + ' %'
slug = lambda b: f'{b}-euros-brutos-en-netos'

# ---------------- plantilla común (menú y pie de vacaciones.html, con "Nómina" marcado)
v = open('vacaciones.html', encoding='utf-8').read()
NAV = v[v.index('<body>') + len('<body>\n'):v.index('<main>')].replace(' aria-current="page"', '')
FOOT = v[v.index('<footer'):v.index('<script src="site.js')]
FAQ_HTML = lambda faqs: ''.join(f'<div class="faq-item"><button class="faq-q"><span>{q}</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faqs)
limpio = lambda t: re.sub(r'<[^>]+>', '', t)
FUENTE = 'Cálculo con las cifras de 2026: cotización a la Seguridad Social de la Orden PJC/297/2026 y retención de IRPF según el algoritmo de la Agencia Tributaria (arts. 80 a 86 del Reglamento del IRPF).'

def pagina(nombre, titulo, desc, keywords, miga, cuerpo, faqs):
    ld_faq = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': limpio(q), 'acceptedAnswer': {'@type': 'Answer', 'text': limpio(a)}} for q, a in faqs]}, ensure_ascii=False, indent=1)
    migas = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': 'https://calculalotuyo.es/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Sueldo neto', 'item': 'https://calculalotuyo.es/sueldo-neto'}]
    if nombre != 'sueldo-bruto-a-neto-2026':
        migas.append({'@type': 'ListItem', 'position': 3, 'name': 'Tabla bruto a neto 2026', 'item': 'https://calculalotuyo.es/sueldo-bruto-a-neto-2026'})
    migas.append({'@type': 'ListItem', 'position': len(migas) + 1, 'name': miga})
    ld_miga = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': migas}, ensure_ascii=False, indent=1)
    t, d = H.escape(titulo), H.escape(desc)
    migas_html = '<a href="./">Inicio</a> <span class="breadcrumb-sep">›</span> <a href="sueldo-neto">Sueldo neto</a> <span class="breadcrumb-sep">›</span> '
    if nombre != 'sueldo-bruto-a-neto-2026':
        migas_html += '<a href="sueldo-bruto-a-neto-2026">Tabla bruto a neto</a> <span class="breadcrumb-sep">›</span> '
    cuerpo = cuerpo.replace('{{MIGAS}}', f'<nav class="breadcrumb" aria-label="Estás en">{migas_html}<span aria-current="page">{miga}</span></nav>')
    texto = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-4853214655991551">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4853214655991551" crossorigin="anonymous"></script>
    <meta name="description" content="{d}">
    <meta name="keywords" content="{H.escape(keywords)}">
    <title>{t}</title>
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://calculalotuyo.es/{nombre}">
    <meta property="og:title" content="{t}">
    <meta property="og:description" content="{d}">
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
    <meta name="theme-color" content="#4F46E5">
    <link rel="canonical" href="https://calculalotuyo.es/{nombre}">
    <link rel="stylesheet" href="{CSS}">
    <script type="application/ld+json">
{ld_faq}
    </script>
    <script type="application/ld+json">
{ld_miga}
    </script>
</head>
<body>
{NAV.replace('class="nav-link" data-dropdown-btn>Nómina', 'class="nav-link active" data-dropdown-btn>Nómina')}<main>
{cuerpo}
    <section class="section section-alt"><div class="container"><h2 class="section-title">❓ Preguntas frecuentes</h2>
        <div class="faq-list">{FAQ_HTML(faqs)}</div>
    </div></section>
    <section class="section"><div class="container"><div class="source-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg><div><strong>Cómo lo calculamos:</strong><p>{FUENTE}</p></div></div></div></section>
</main>

{FOOT}<script src="site.js?v=20261019b"></script>
</body>
</html>
'''
    open(f'{nombre}.html', 'w', encoding='utf-8').write(texto)
    return nombre

REVISADO = '<p class="hero-meta">📅 Revisado el 19 de octubre de 2026 · ✍️ <a href="sobre-el-proyecto">CalculaLoTuyo</a></p>'
AD = '\n    <div class="container"><div class="ad"></div></div>\n'
CTA = '<div class="result-actions"><a href="sueldo-neto" class="btn">🏦 Calcular con mis datos</a></div>'
generadas = []

# ================================================================ PÁGINA DE CADA SUELDO
for b in PAGINAS:
    x = DAT[b]; base = x['base']
    m12, m14 = base['neto'] / 12, base['neto'] / 14
    p_neto, p_ss, p_irpf = (base['neto'] / b * 100, base['ss'] / b * 100, base['irpf'] / b * 100)
    filas = ''
    for k, nombre in [('base', 'Sin hijos'), ('hijo1', '1 hijo'), ('hijos2', '2 hijos'), ('temporal', 'Temporal')]:
        c = x[k]
        filas += f'<tr><td>{nombre}</td><td><strong>{e(c["neto"] / 12)} €</strong></td><td>{e(c["neto"] / 14)} €</td><td>{pct(c["tipo"])}</td></tr>'
    i = PAGINAS.index(b)
    vecinos = [p for p in PAGINAS[max(0, i - 3):i + 4] if p != b]
    enl = '<div class="enlaces-sueldo">' + ''.join(f'<a href="{slug(p)}">{e(p)} €</a>' for p in vecinos) + '<a href="sueldo-bruto-a-neto-2026">Ver todos →</a></div>'
    dif_hijo = x['hijo1']['neto'] / 12 - m12
    cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🏦 Nómina 2026</div><h1>{e(b)} € brutos en netos<br><span class="highlight">{e(m12)} € al mes</span></h1><p>Con un sueldo de {e(b)} € brutos al año en 2026, sin hijos y con contrato indefinido, te quedan <strong>{e(base["neto"])} € netos</strong>.</p>
            {REVISADO}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{e(m12)} €</strong><span>al mes en 12 pagas</span></div><div><strong>{e(m14)} €</strong><span>al mes en 14 pagas</span></div><div><strong>{pct(base["tipo"])}</strong><span>de retención de IRPF</span></div></div>
        <h2 class="puentes-titulo">💶 Adónde va cada euro de tu sueldo</h2>
        <div class="reparto"><span class="r-neto" style="width:{p_neto:.1f}%"></span><span class="r-ss" style="width:{p_ss:.1f}%"></span><span class="r-irpf" style="width:{p_irpf:.1f}%"></span></div>
        <div class="reparto-leyenda"><span><i class="r-neto"></i>Para ti: <strong>{e(base["neto"])} €</strong> ({e(p_neto)} %)</span><span><i class="r-ss"></i>Seguridad Social: <strong>{e(base["ss"])} €</strong></span><span><i class="r-irpf"></i>IRPF: <strong>{e(base["irpf"])} €</strong></span></div>
        <h2 class="puentes-titulo">👨‍👩‍👧 Según tu situación</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Situación</th><th>12 pagas</th><th>14 pagas</th><th>IRPF</th></tr></thead><tbody>{filas}</tbody></table></div>
        <p class="nota-corta">Neto al mes. «Sin hijos», «1 hijo» y «2 hijos» son con contrato indefinido; «Temporal», sin hijos. Con hijos, el mínimo por descendientes se reparte a medias entre los dos progenitores, que es lo más habitual. Menor de 65 años y sin discapacidad.</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Cálculo paso a paso</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Sueldo bruto anual:</strong><p>{e(b)} € (son {e(b / 12, 2)} € brutos al mes en 12 pagas o {e(b / 14, 2)} € en 14)</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Seguridad Social ({pct(base["ss"] / b * 100)}):</strong><p>− {e(base["ss"], 2)} €</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Retención de IRPF ({pct(base["tipo"])}):</strong><p>− {e(base["irpf"], 2)} €</p></div></div>
    <div class="calc-step"><span class="step-num">4</span><div><strong>Sueldo neto anual:</strong><p><strong>{e(base["neto"], 2)} €</strong>, es decir, {e(m12, 2)} € al mes en 12 pagas o {e(m14, 2)} € en 14 pagas.</p></div></div>
</div>
<p>A la empresa, este sueldo le cuesta unos <strong>{e(base["coste"])} €</strong> al año, porque además paga su parte de la Seguridad Social (alrededor del 30,65 %).</p>
<h2>👶 ¿Y si tienes hijos?</h2>
<p>Con un hijo, la retención baja al {pct(x["hijo1"]["tipo"])} y cobras unos <strong>{e(dif_hijo)} € más al mes</strong>. Con dos, el neto sube a {e(x["hijos2"]["neto"] / 12)} € al mes. Con un contrato temporal pagas algo más de Seguridad Social (6,55 % en vez de 6,50 %).</p>
<h2>❔ Por qué tu nómina puede ser un poco distinta</h2>
<p>La retención es un adelanto del IRPF. En la declaración de la renta se ajusta con la escala de tu comunidad autónoma, y también cambia si tienes horas extra, pagas en especie o un cambio de sueldo a mitad de año. Para tu caso exacto, usa la <a href="sueldo-neto">calculadora de sueldo neto</a>, y para ver el IRPF tramo a tramo, la <a href="irpf">calculadora de IRPF</a>.</p>
<h2>💶 Sueldos parecidos</h2>
{enl}
</article></div></section>
'''
    faqs = [
        (f'¿Cuánto son {e(b)} € brutos en netos al mes?', f'<strong>{e(m12)} € al mes</strong> si cobras en 12 pagas, o <strong>{e(m14)} €</strong> si son 14 pagas (con dos pagas extra). Es para una persona sin hijos y con contrato indefinido en 2026.'),
        (f'¿Cuánto IRPF se paga con {e(b)} € brutos?', f'La retención es del <strong>{pct(base["tipo"])}</strong>: unos {e(base["irpf"])} € al año. Con hijos, baja.'),
        (f'¿Cuánto le cuesta a la empresa un sueldo de {e(b)} € brutos?', f'Unos <strong>{e(base["coste"])} €</strong> al año, sumando la cotización a la Seguridad Social que paga la empresa.'),
        (f'¿{e(b)} € brutos son mucho o poco?', f'El salario mínimo de 2026 es de {e(SMI)} € brutos al año. Un sueldo de {e(b)} € es {e(b / SMI, 1)} veces el salario mínimo.'),
    ]
    generadas.append(pagina(slug(b), f'{e(b)} € brutos en netos 2026: {e(m12)} € al mes', f'{e(b)} euros brutos al año son {e(base["neto"])} € netos en 2026: {e(m12)} € al mes en 12 pagas o {e(m14)} € en 14. Retención del {pct(base["tipo"])}, con y sin hijos.', f'{b} brutos en netos, {e(b)} euros brutos en netos, {b} brutos anuales cuánto es neto, sueldo {b} brutos al mes', f'{e(b)} € brutos', cuerpo, faqs))

# ================================================================ TABLA GENERAL
filas = ''
for b in sorted(DAT):
    c = DAT[b]['base']
    nom = f'<a href="{slug(b)}">{e(b)} €</a>' if b in PAGINAS else (f'{e(b)} € <small>(SMI)</small>' if b == SMI else f'{e(b)} €')
    filas += f'<tr><td>{nom}</td><td>{e(b / 14)} €</td><td><strong>{e(c["neto"] / 12)} €</strong></td><td>{e(c["neto"] / 14)} €</td><td>{pct(c["tipo"])}</td></tr>'
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🏦 Nómina 2026</div><h1>Tabla de sueldo bruto a neto<br><span class="highlight">2026</span></h1><p>Cuánto te queda al mes de cada sueldo, de {e(SMI)} € (el salario mínimo) a 100.000 € brutos al año.</p>
            {REVISADO}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <h2 class="puentes-titulo" style="margin-top:0">🔎 Los sueldos más buscados</h2>
        <div class="enlaces-sueldo">{"".join(f'<a href="{slug(p)}">{e(p)} €</a>' for p in PAGINAS)}</div>
        <h2 class="puentes-titulo">📋 Bruto anual → neto mensual</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Bruto/año</th><th>Bruto/mes (14)</th><th>Neto/mes (12)</th><th>Neto/mes (14)</th><th>Retención</th></tr></thead><tbody>{filas}</tbody></table></div>
        <p class="nota-corta">Persona sin hijos, menor de 65 años y con contrato indefinido. Cotización a la Seguridad Social del 6,50 % y retención de IRPF según el algoritmo de Hacienda para 2026.</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📖 Cómo se pasa de bruto a neto</h2>
<p>Del sueldo bruto se restan dos cosas: la <strong>cotización a la Seguridad Social</strong> (6,50 % con contrato indefinido, 6,55 % si es temporal) y la <strong>retención de IRPF</strong>, que sube con el sueldo y baja si tienes hijos u otras personas a cargo. Lo que queda es el neto.</p>
<p>Si cobras en 14 pagas, el neto anual es el mismo: solo se reparte en más nóminas. Por eso el neto al mes en 14 pagas es más bajo, aunque en junio y diciembre cobras el doble.</p>
<p>Para hacer el cálculo con tu situación exacta (hijos, edad, contrato o discapacidad), usa la <a href="sueldo-neto">calculadora de sueldo neto</a>. Te lo explicamos todo en la <a href="guia-sueldo-neto">guía del sueldo neto</a>.</p>
</article></div></section>
'''
c30 = DAT[30000]['base']
faqs = [
    ('¿Cuánto se queda Hacienda de mi sueldo bruto?', 'Depende del sueldo: con 20.000 € la retención ronda el ' + pct(DAT[20000]['base']['tipo']) + ', con 30.000 € el ' + pct(c30['tipo']) + ' y con 50.000 € el ' + pct(DAT[50000]['base']['tipo']) + '. A eso se suma un 6,50 % de Seguridad Social.'),
    ('¿Cuánto es el salario mínimo de 2026 en neto?', f'El salario mínimo es de {e(SMI)} € brutos al año. En la nómina quedan unos <strong>{e(DAT[SMI]["base"]["neto"] / 14)} € netos al mes</strong> en 14 pagas, con una retención del {pct(DAT[SMI]["base"]["tipo"])}. Esa retención se recupera en la renta: en 2026 hay una deducción que deja a cero el IRPF de quien cobra el SMI. Lo explicamos en <a href="smi-2026">SMI 2026</a>.'),
    ('¿Es mejor cobrar en 12 o en 14 pagas?', 'Cobras lo mismo al año. Con 12 pagas recibes más cada mes; con 14, cobras menos al mes pero tienes dos pagas extra en junio y diciembre.'),
]
generadas.append(pagina('sueldo-bruto-a-neto-2026', 'Tabla de sueldo bruto a neto 2026: cuánto cobras al mes', f'Tabla 2026 para pasar de sueldo bruto a neto: de {e(SMI)} a 100.000 € brutos al año, con el neto al mes en 12 y 14 pagas y la retención de IRPF.', 'sueldo bruto a neto 2026, tabla bruto neto, de bruto a neto, cuánto cobro neto', 'Tabla bruto a neto 2026', cuerpo, faqs))
json.dump(generadas, open(f'{AQUI}/generadas.json', 'w'))
print(len(generadas), 'páginas')
