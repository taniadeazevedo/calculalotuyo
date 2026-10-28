# Páginas de «situaciones concretas» (búsquedas muy específicas, 28/10/2026): la respuesta con cifras arriba,
# tablas calculadas y enlace a la calculadora. Cada cifra sale de la MISMA fórmula que la calculadora de la web.
# Uso: python3 _herramientas/situaciones/gen-situaciones.py   (regenerar.sh ya lo lanza)
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))                     # carpeta de este script
sys.path.insert(0, os.path.join(AQUI, '..'))                         # para usar la plantilla común
from plantilla import pagina, REVISADO, e, RAIZ                      # e(1234.5) → «1.235»

REV = REVISADO.format(fecha='28 de octubre de 2026')
boe = lambda id_, txt: f'<a href="https://www.boe.es/buscar/act.php?id={id_}" target="_blank" rel="noopener">{txt}</a>'

def sitemap(slug):
    """Añade la página al sitemap si aún no está (sitemap.py pone la fecha buena)."""
    sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    if f'/{slug}<' not in s:
        s = s.replace('</urlset>', f'    <url><loc>https://calculalotuyo.es/{slug}</loc><lastmod>2026-10-28</lastmod><priority>0.7</priority></url>\n</urlset>')
        open(sm, 'w', encoding='utf-8').write(s)

# ===================== «Baja de 15 días: cuánto cobro» =====================
# La misma regla que baja-medica.html (porcentaje de cada día) y quién paga (art. 173 LGSS)
def porcentaje(dia, tipo):
    if tipo == 'profesional': return 1 if dia == 1 else 0.75          # accidente de trabajo: el día de la baja, salario entero (empresa)
    if dia <= 3: return 0                                              # enfermedad común: días 1 a 3, nada (salvo convenio)
    if dia <= 20: return 0.60                                          # días 4 a 20, el 60 %
    return 0.75                                                        # desde el 21, el 75 %

def baja(base_mes, dias, tipo='comun'):
    """Cuánto se cobra en total por la baja y cuánto paga la empresa (bruto)."""
    diario = base_mes / 30                                             # base reguladora diaria
    total = empresa = 0.0
    for d in range(1, dias + 1):
        imp = diario * porcentaje(d, tipo); total += imp
        if (tipo == 'profesional' and d == 1) or (tipo == 'comun' and 4 <= d <= 15): empresa += imp
    return total, empresa, diario * dias                               # cobrado, a cargo de la empresa, lo que habría cobrado trabajando

BASES = [1300, 1500, 1800, 2000, 2500, 3000]                          # bases de cotización mensuales frecuentes
filas_base = ''
for b in BASES:
    comun, _, trab = baja(b, 15); acc, _, _ = baja(b, 15, 'profesional')
    filas_base += f'<tr id="base-{b}"><td>{e(b)} €</td><td><strong>{e(comun)} €</strong></td><td>{e(acc)} €</td><td>{e(trab)} €</td></tr>'
DURACIONES = [3, 7, 10, 15, 20, 30]
filas_dias = ''
for d in DURACIONES:
    c, emp, trab = baja(2000, d)
    filas_dias += f'<tr><td>{d} días</td><td><strong>{e(c)} €</strong></td><td>{e(emp)} €</td><td>{e(c - emp)} €</td><td>{e(trab)} €</td></tr>'
c15, emp15, trab15 = baja(2000, 15)                                    # el ejemplo de la respuesta rápida
a15, _, _ = baja(2000, 15, 'profesional')

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🩺 Baja médica</div><h1>Baja de 15 días: cuánto cobro<br><span class="highlight">con ejemplos ya calculados</span></h1><p>Lo que cobras por una baja de 15 días por enfermedad común o por accidente de trabajo, quién te lo paga y cómo queda la nómina, según tu sueldo.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Con una baja de 15 días por <strong>enfermedad común</strong>, los <strong>3 primeros días no cobras</strong> (salvo convenio) y los 12 restantes cobras el <strong>60 %</strong> de tu base reguladora.</li>
<li>Con una base de cotización de 2.000 € al mes: <strong>{e(c15)} € brutos</strong>, frente a los {e(trab15)} € de esos días trabajando.</li>
<li>Si es por <strong>accidente de trabajo</strong>, el día del accidente lo paga la empresa entero y desde el siguiente cobras el 75 %: <strong>{e(a15)} €</strong> con la misma base.</li>
<li>En una baja de 15 días, lo de la enfermedad común lo paga <strong>todo la empresa</strong>, en tu nómina.</li>
</ul></div>

<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Tu base reguladora diaria</strong><p>Es (<a href="que-es-la-base-reguladora">qué es</a>) tu base de cotización del mes anterior a la baja dividida entre 30 (ya incluye la parte de las pagas extra). Con 2.000 € al mes: {e(2000 / 30, 2)} € al día.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Días 1 a 3: sin prestación</strong><p>En la enfermedad común y el accidente no laboral, los tres primeros días no se cobran, salvo que tu convenio los pague.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Días 4 a 15: el 60 %, lo paga la empresa</strong><p>12 días × {e(2000 / 30, 2)} € × 60 % = <strong>{e(c15)} €</strong>. La empresa paga los días 4 a 15 ({boe("BOE-A-2015-11724", "artículo 173 de la Ley General de la Seguridad Social")}); desde el día 16 paga la Seguridad Social o la mutua, aunque lo sigues cobrando en la nómina.</p></div></div>
</div>

<h2>💶 Una baja de 15 días según tu base de cotización</h2>
<table class="info-table"><tr><th>Base al mes</th><th>Enfermedad común</th><th>Accidente de trabajo</th><th>Trabajando esos 15 días</th></tr>{filas_base}</table>
<p class="nota-corta">Importes brutos de la prestación, sin complemento de convenio. La base de cotización la ves en tu nómina; suele ser tu sueldo bruto del mes más la parte proporcional de las pagas extra.</p>

<h2>📆 Y si la baja dura más o menos</h2>
<p>Con una base de cotización de 2.000 € al mes, por enfermedad común:</p>
<table class="info-table"><tr><th>Duración</th><th>Cobras en total</th><th>Lo paga la empresa</th><th>Lo paga la Seguridad Social</th><th>Trabajando</th></tr>{filas_dias}</table>
<p>A partir del día 21 se cobra el 75 %. Calcula tu caso exacto, con tus días y tu convenio, en la <a href="baja-medica">calculadora de la baja médica</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li><strong>Tu convenio puede mejorarlo:</strong> muchos completan hasta el 100 % del sueldo, a veces desde el primer día. Es lo que más cambia la cifra.</li>
<li>Para la enfermedad común necesitas <strong>180 días cotizados en los últimos 5 años</strong>; para el accidente, ninguno.</li>
<li>La prestación <strong>tributa en el IRPF</strong> y sigues cotizando, así que en la nómina se descuentan como siempre.</li>
<li>Todo el detalle está en la <a href="guia-baja-medica">guía de la baja médica</a> y, paso a paso, en <a href="que-hacer-si-me-pongo-de-baja">qué hacer si te pones de baja</a>.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Cuánto cobro por una baja de 15 días?', f'Por enfermedad común, nada los 3 primeros días y el 60 % de tu base reguladora diaria los 12 siguientes. Con una base de 2.000 € al mes, unos <strong>{e(c15)} € brutos</strong>. Por accidente de trabajo, unos <strong>{e(a15)} €</strong>. Tu convenio puede mejorarlo.'),
    ('¿Quién paga una baja de 15 días?', 'En la enfermedad común, los días 4 a 15 los paga <strong>la empresa</strong>, así que en una baja de 15 días lo paga todo ella, en tu nómina. Desde el día 16 paga la Seguridad Social o la mutua (artículo 173 de la Ley General de la Seguridad Social).'),
    ('¿Se cobran los 3 primeros días de baja?', 'Por ley, no: en la enfermedad común y el accidente no laboral la prestación empieza el día 4. Pero muchos convenios los pagan; míralo en el tuyo. En el accidente de trabajo, el día de la baja lo paga la empresa como salario y desde el día siguiente cobras el 75 %.'),
]
pagina('baja-15-dias-cuanto-cobro', 'Baja de 15 días: cuánto cobro en 2026 (ejemplos)',
    f'Baja de 15 días por enfermedad común: 3 días sin cobrar y 12 al 60 %. Con 2.000 € de base, unos {e(c15)} €. Por accidente, {e(a15)} €. Tablas por sueldo.',
    'baja de 15 días cuánto cobro, cuánto se cobra de baja 15 días, baja médica 15 días, baja 15 días nómina',
    [('Guías', 'guias'), ('Baja de 15 días: cuánto cobro', None)], cuerpo, faqs,
    'Ley General de la Seguridad Social (arts. 169 a 174), versión consolidada del BOE, y porcentajes de la incapacidad temporal (60 % y 75 %), los mismos de la calculadora de la baja médica.',
    menu_activo='Guías')
sitemap('baja-15-dias-cuanto-cobro')
CAJA = '<!-- SITUACIONES --><p class="nota-corta">📋 <strong>Ejemplo ya calculado:</strong> <a href="baja-15-dias-cuanto-cobro">baja de 15 días, cuánto cobro</a>, con tablas por sueldo y por duración.</p><!-- /SITUACIONES -->\n'
for f, antes in [('baja-medica.html', '<section class="faq">'), ('guia-baja-medica.html', '<section id="calculadoras" class="guide-section"')]:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    if '<!-- SITUACIONES -->' not in t and antes in t:
        t = t.replace(antes, CAJA + antes, 1); open(ruta, 'w', encoding='utf-8').write(t)
print('creada: baja-15-dias-cuanto-cobro · base 2.000 € → enfermedad', e(c15), '€ · accidente', e(a15), '€')

# ===================== «¿Qué es la base reguladora?» (definición, 28/10/2026) =====================
# Paro: art. 270 LGSS (media de lo cotizado por desempleo en los últimos 180 días, sin horas extra).
# Baja, nacimiento y jubilación: lo ya verificado en sus guías y calculadoras.
SUELDO_MES, PAGAS = 2000, 14                                           # el ejemplo: 2.000 € brutos al mes en 14 pagas
base_cot = SUELDO_MES * PAGAS / 12                                     # base de cotización mensual (con la parte de las pagas extra)
br_dia = base_cot / 30                                                 # base reguladora diaria (baja y paro)
paro70 = min(base_cot * 0.70, 1225)                                    # paro los 6 primeros meses, con el tope sin hijos de 2026
TABLA = [
    ('Paro', 'La media de lo cotizado por desempleo en los <strong>últimos 180 días</strong>, sin horas extra', '70 % los 6 primeros meses y 60 % después, con mínimo y máximo', 'paro'),
    ('Baja médica', 'Tu base de cotización del <strong>mes anterior</strong> a la baja, entre 30 (por día)', '60 % del día 4 al 20 y 75 % desde el 21 (accidente: 75 %)', 'baja-medica'),
    ('Nacimiento de un hijo', 'Tu base de cotización por contingencias comunes del <strong>mes anterior</strong> al permiso', '100 %, sin IRPF', 'guia-nacimiento'),
    ('Jubilación', 'La media actualizada de tus bases de los <strong>últimos años</strong> (en 2026, las 302 mejores de los últimos 304 meses)', 'Un porcentaje según los años cotizados, hasta el 100 %', 'jubilacion'),
]
filas_br = ''.join(f'<tr><td><a href="{u}">{p}</a></td><td>{c}</td><td>{q}</td></tr>' for p, c, q, u in TABLA)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📖 Definición</div><h1>¿Qué es la base reguladora?<br><span class="highlight">explicado con un ejemplo</span></h1><p>La cifra de la que salen tu paro, tu baja, tu permiso por nacimiento y tu pensión. Qué es, cómo se calcula en cada caso y dónde ver la tuya.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>La <strong>base reguladora</strong> es la cantidad sobre la que la Seguridad Social calcula lo que cobras de paro, baja, nacimiento o jubilación.</li>
<li>Sale de lo que <strong>has cotizado</strong> (tus bases de cotización), no de tu sueldo neto.</li>
<li>Cada prestación la calcula de una forma: el paro, con los <strong>últimos 180 días</strong>; la baja, con el <strong>mes anterior</strong>; la jubilación, con <strong>muchos años</strong>.</li>
<li>Luego se le aplica un porcentaje: por ejemplo, el <strong>70 %</strong> en el paro o el <strong>60 %</strong> en la baja.</li>
</ul></div>

<h2>📌 Base de cotización y base reguladora: la diferencia</h2>
<p>La <strong>base de cotización</strong> es lo que aparece en tu nómina cada mes: tu sueldo bruto más la parte proporcional de las pagas extra, sobre la que pagáis cotizaciones tú y la empresa. La <strong>base reguladora</strong> se calcula a partir de esas bases cuando pides una prestación: es una media de las de un periodo, que cambia según la prestación.</p>

<h2>🧾 Cómo se calcula en cada prestación</h2>
<table class="info-table"><tr><th>Prestación</th><th>Base reguladora</th><th>Qué cobras</th></tr>{filas_br}</table>
<p class="nota-corta">Paro: {boe("BOE-A-2015-11724", "artículo 270 de la Ley General de la Seguridad Social")}. Cada prestación tiene además sus requisitos y topes; los tienes en su calculadora o guía.</p>

<h2>🧮 Un ejemplo con un sueldo real</h2>
<div class="example-box">
    <h4>👩‍💼 Laura: 2.000 € brutos al mes en 14 pagas</h4>
    <p>Contrato indefinido, siempre el mismo sueldo y sin horas extra.</p>
    <div class="calc-line">Base de cotización: 2.000 × 14 ÷ 12 = {e(base_cot, 2)} € al mes (incluye la parte de las 2 pagas extra)</div>
    <div class="calc-line">Base reguladora diaria (baja y paro): {e(base_cot, 2)} ÷ 30 = {e(br_dia, 2)} € al día</div>
    <div class="calc-line">Paro: 70 % de {e(base_cot)} € = {e(base_cot * 0.70)} € → con el tope sin hijos de 2026, {e(paro70)} € al mes</div>
    <div class="calc-line">Baja de 15 días por enfermedad: 12 días × {e(br_dia, 2)} € × 60 % = {e(12 * br_dia * 0.60)} €</div>
    <p class="result-highlight">Por eso el paro o la baja no son «el 70 % de tu nómina»: salen de tu base reguladora, con sus porcentajes y sus topes</p>
</div>

<h2>🔎 Dónde ver tu base de cotización</h2>
<ul>
<li>En tu <strong>nómina</strong>, en el apartado de las bases de cotización: «contingencias comunes» (para la baja, el nacimiento y la jubilación) y «desempleo» o «contingencias profesionales» (para el paro).</li>
<li>En tu <strong>informe de bases de cotización</strong> de la Seguridad Social, que puedes pedir en su sede electrónica.</li>
</ul>
<p>Con ese dato, calcula lo tuyo en la <a href="paro">calculadora del paro</a>, la de la <a href="baja-medica">baja médica</a> o la de <a href="jubilacion">jubilación</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿Qué es la base reguladora?', 'La cantidad sobre la que la Seguridad Social calcula lo que cobras de una prestación (paro, baja, nacimiento, jubilación). Es una media de tus bases de cotización de un periodo, que cambia según la prestación.'),
    ('¿La base reguladora es mi sueldo bruto?', 'No exactamente. Sale de tus bases de cotización, que incluyen la parte proporcional de las pagas extra: con 2.000 € brutos al mes en 14 pagas, tu base de cotización es de unos 2.333 € al mes.'),
    ('¿Cómo se calcula la base reguladora del paro?', 'Es la media de lo cotizado por desempleo en los <strong>últimos 180 días</strong>, sin contar las horas extra (artículo 270 de la Ley General de la Seguridad Social). Sobre ella cobras el 70 % los 6 primeros meses y el 60 % después, con un mínimo y un máximo.'),
]
pagina('que-es-la-base-reguladora', '¿Qué es la base reguladora? Explicada con un ejemplo',
    'La base reguladora es la cifra con la que se calcula tu paro, baja, nacimiento o jubilación. Cómo se calcula en cada caso, un ejemplo y dónde ver la tuya.',
    'qué es la base reguladora, base reguladora paro, base reguladora baja, cómo se calcula la base reguladora',
    [('Guías', 'guias'), ('¿Qué es la base reguladora?', None)], cuerpo, faqs,
    'Ley General de la Seguridad Social (art. 270 y normas de cada prestación), versión consolidada del BOE.',
    menu_activo='Guías')
sitemap('que-es-la-base-reguladora')
print('creada: que-es-la-base-reguladora · ejemplo 2.000 € × 14 → base', e(base_cot, 2), '€')

# Enlace a la definición desde las calculadoras que la usan (una caja discreta, solo una vez)
DEF = '<!-- DEFINICION-BR --><p class="nota-corta">📖 ¿No sabes qué es tu base reguladora? Te lo explicamos con un ejemplo en <a href="que-es-la-base-reguladora">qué es la base reguladora</a>.</p><!-- /DEFINICION-BR -->\n'
for f in ['paro.html', 'baja-medica.html', 'jubilacion.html']:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    ancla = next((x for x in ['<section class="faq">', '<section class="section section-alt">'] if x in t), None)   # antes de las preguntas frecuentes
    if '<!-- DEFINICION-BR -->' not in t and ancla:
        t = t.replace(ancla, DEF + ancla, 1); open(ruta, 'w', encoding='utf-8').write(t)
