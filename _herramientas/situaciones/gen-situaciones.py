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

# ===================== «¿Qué es el finiquito?» (definición, 02/11/2026) =====================
# Datos de la guía del finiquito (revisada contra el BOE): art. 49.2 ET (propuesta de liquidación y representante),
# art. 59 ET (un año para reclamar cantidades) y el ejemplo de Marta, calculado allí paso a paso.
DIFERENCIAS = [
    ('Qué paga', 'Lo que ya has trabajado y aún no has cobrado', 'La pérdida del empleo'),
    ('Cuándo existe', 'Siempre, termine como termine el contrato', 'Solo en algunos casos (despido, fin de contrato temporal…)'),
    ('Si te vas tú', 'Sí lo cobras', 'En general, no'),
    ('IRPF', 'Tributa como tu sueldo', 'La legal está exenta (hasta 180.000 €)'),
]
filas_dif = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in DIFERENCIAS)
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📖 Definición</div><h1>¿Qué es el finiquito?<br><span class="highlight">y qué tiene que incluir</span></h1><p>Qué es el finiquito, qué conceptos lleva, en qué se diferencia de la indemnización y qué hacer antes de firmarlo, según el Estatuto de los Trabajadores.</p>
            {REV.replace("28 de octubre", "2 de noviembre")}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>El <strong>finiquito</strong> es el pago de todo lo que la empresa te debe el día que termina tu contrato.</li>
<li>Lo cobras <strong>siempre</strong>: si te despiden, si te vas tú o si se acaba un contrato temporal.</li>
<li>Incluye el <strong>sueldo de los días del mes</strong>, las <strong>vacaciones no disfrutadas</strong> y la <strong>parte de las pagas extra</strong> que llevas generada.</li>
<li><strong>No es la indemnización:</strong> esa solo existe en algunos casos y se suma aparte.</li>
</ul></div>

<h2>🧾 Los conceptos que debe incluir</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Sueldo de los días trabajados del mes</strong><p>Desde el día 1 hasta tu último día. Con sueldo mensual: tu sueldo ÷ 30 × días trabajados.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Vacaciones generadas y no disfrutadas</strong><p>Se generan día a día (2,5 días por mes con el mínimo legal de 30). Las que no hayas disfrutado se pagan: es el único caso en que se cambian por dinero.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>La parte de las pagas extra ya generada</strong><p>Si cobras 14 pagas, la parte de la próxima paga extra que ya llevas acumulada. Si las tienes prorrateadas en 12 pagas, no queda nada pendiente.</p></div></div>
    <div class="calc-step"><span class="step-num">4</span><div><strong>Cualquier otra cosa pendiente</strong><p>Horas extra sin pagar, comisiones, pluses o días de descanso que te deban.</p></div></div>
</div>
<p>Un ejemplo real: con 1.800 € brutos al mes en 14 pagas, dejando la empresa el 20 de mayo y con 5 días de vacaciones disfrutados, el finiquito sale de unos <strong>2.990 € brutos</strong>. Lo tienes paso a paso en la <a href="guia-finiquito">guía del finiquito</a>, y con tus datos en la <a href="finiquito">calculadora de finiquito</a>.</p>

<h2>⚖️ Finiquito e indemnización: no son lo mismo</h2>
<table class="info-table"><tr><th></th><th>Finiquito</th><th>Indemnización</th></tr>{filas_dif}</table>
<p>A menudo vienen en el mismo papel, pero son cosas distintas. Si te despiden, mira también cuánto te corresponde de <a href="despido-improcedente">indemnización por despido</a>.</p>

<h2>✍️ Antes de firmarlo</h2>
<ul>
<li>La empresa tiene que darte una <strong>propuesta del finiquito</strong> junto con la carta de fin de contrato, y puedes pedir que esté delante un representante de los trabajadores al firmar ({boe("BOE-A-2015-11430", "artículo 49.2 del Estatuto de los Trabajadores")}).</li>
<li>Si no estás de acuerdo con las cifras, firma como <strong>«recibido, no conforme»</strong>: así dejas claro que solo lo has recibido.</li>
<li>Para reclamar dinero que te deban tienes <strong>un año</strong> desde que pudiste reclamarlo ({boe("BOE-A-2015-11430", "artículo 59 del Estatuto de los Trabajadores")}).</li>
</ul>
<p>Si te han despedido, sigue los pasos en <a href="que-hacer-si-me-despiden">qué hacer si te despiden</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿Qué es el finiquito?', 'El pago de todo lo que la empresa te debe al terminar el contrato: el sueldo de los días del mes, las vacaciones no disfrutadas y la parte de las pagas extra ya generada. Se cobra siempre, también si te vas tú.'),
    ('¿El finiquito y la indemnización son lo mismo?', '<strong>No.</strong> El finiquito paga lo ya trabajado y se cobra siempre; la indemnización compensa la pérdida del empleo y solo existe en algunos casos, como un despido o el fin de un contrato temporal.'),
    ('¿Si me voy de la empresa cobro finiquito?', '<strong>Sí.</strong> El finiquito se cobra termine como termine el contrato. Lo que no suele haber al irte tú es indemnización.'),
]
pagina('que-es-el-finiquito', '¿Qué es el finiquito? Qué incluye y en qué se diferencia',
    'El finiquito es lo que te debe la empresa al acabar el contrato: días del mes, vacaciones y pagas extra. Qué incluye, en qué se diferencia de la indemnización.',
    'qué es el finiquito, qué incluye el finiquito, finiquito e indemnización diferencia, finiquito si me voy',
    [('Guías', 'guias'), ('¿Qué es el finiquito?', None)], cuerpo, faqs,
    'Estatuto de los Trabajadores (arts. 49.2 y 59), versión consolidada del BOE, y la guía del finiquito de CalculaLoTuyo.',
    menu_activo='Guías')
sitemap('que-es-el-finiquito')
DEF2 = '<!-- DEFINICION-FQ --><p class="nota-corta">📖 ¿Finiquito o indemnización? Te lo explicamos en <a href="que-es-el-finiquito">qué es el finiquito</a>.</p><!-- /DEFINICION-FQ -->\n'
for f in ['finiquito.html', 'despido-improcedente.html']:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    ancla = next((x for x in ['<section class="faq">', '<section class="section section-alt">'] if x in t), None)
    if '<!-- DEFINICION-FQ -->' not in t and ancla:
        t = t.replace(ancla, DEF2 + ancla, 1); open(ruta, 'w', encoding='utf-8').write(t)
print('creada: que-es-el-finiquito')

# ===================== «Paro tras un contrato temporal» (02/11/2026) =====================
# LGSS arts. 266 (requisitos), 267.1.a.6.º (fin de contrato temporal = situación legal de desempleo), 268 (15 días),
# 269 (escala de duración) y 270 (base reguladora); ET art. 49.1.c (12 días por año al acabar el contrato).
ESCALA_PARO = [(360, 120), (540, 180), (720, 240), (900, 300), (1080, 360), (1260, 420), (1440, 480), (1620, 540), (1800, 600), (1980, 660), (2160, 720)]
def dias_paro(cotizados):
    """Días de paro según los días cotizados en los últimos 6 años (art. 269 LGSS)."""
    return max([p for c, p in ESCALA_PARO if cotizados >= c], default=0)
SUELDO_T = 1600                                                         # el ejemplo: 1.600 € brutos al mes en 14 pagas
anual_t = SUELDO_T * 14
base_t = anual_t / 12                                                   # base de cotización mensual
paro_t = min(base_t * 0.70, 1225)                                       # 70 % con el tope sin hijos de 2026
indem = lambda dias: anual_t / 365 * 12 * dias / 365                     # 12 días de salario por año, en proporción
CONTRATOS = [('6 meses', 182), ('1 año', 365), ('18 meses', 547), ('2 años', 730), ('3 años', 1095)]
filas_t = ''.join(f'<tr><td>{n}</td><td>{d}</td><td><strong>{dias_paro(d) // 30} meses</strong></td><td>{e(indem(d))} €</td></tr>' if dias_paro(d) else
                  f'<tr><td>{n}</td><td>{d}</td><td>Sin paro (menos de 360 días)</td><td>{e(indem(d))} €</td></tr>' for n, d in CONTRATOS)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro</div><h1>Paro tras un contrato temporal<br><span class="highlight">cuánto y cuánto tiempo</span></h1><p>Si se te acaba un contrato temporal: si tienes derecho a paro, cuánto tiempo lo cobrarás, cuánto al mes y la indemnización de 12 días por año.</p>
            {REV.replace("28 de octubre", "2 de noviembre")}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Que se acabe un contrato temporal <strong>da derecho a paro</strong>, como un despido, si has cotizado <strong>al menos 360 días</strong> en los últimos 6 años.</li>
<li>Con un contrato de <strong>1 año</strong> (y nada más cotizado) cobras <strong>4 meses</strong> de paro.</li>
<li>Además, al acabar el contrato te corresponden <strong>12 días de sueldo por año</strong> de indemnización (salvo en los contratos formativos y de sustitución).</li>
<li>Pídelo en los <strong>15 días hábiles</strong> siguientes: si tardas, pierdes días.</li>
</ul></div>

<h2>✅ ¿Tengo derecho a paro?</h2>
<p>Sí, si se cumplen dos cosas: que el contrato <strong>termine porque se acaba</strong> (no porque lo dejes tú) y que hayas cotizado <strong>360 días o más en los últimos 6 años</strong>, sumando todos tus contratos que no hayas usado ya para otro paro ({boe("BOE-A-2015-11724", "artículos 266 y 267 de la Ley General de la Seguridad Social")}).</p>

<h2>📆 Cuánto paro te corresponde según lo que duró el contrato</h2>
<table class="info-table"><tr><th>Contrato</th><th>Días cotizados</th><th>Paro</th><th>Indemnización (12 días/año)</th></tr>{filas_t}</table>
<p class="nota-corta">Si es tu único contrato en los últimos 6 años y cobras {e(SUELDO_T)} € brutos al mes en 14 pagas. Si has trabajado antes, se suman esos días y el paro dura más (hasta 24 meses con 2.160 días). Escala del {boe("BOE-A-2015-11724", "artículo 269 de la Ley General de la Seguridad Social")}.</p>

<h2>🧮 Un ejemplo: Pablo, contrato de un año</h2>
<div class="example-box">
    <h4>👨‍🔧 Pablo: 1.600 € brutos al mes en 14 pagas, contrato temporal de 12 meses</h4>
    <p>Es su primer trabajo, así que tiene 365 días cotizados.</p>
    <div class="calc-line">Paro: 365 días cotizados → <strong>4 meses</strong> (120 días)</div>
    <div class="calc-line">Base reguladora: 1.600 × 14 ÷ 12 = {e(base_t, 2)} € al mes</div>
    <div class="calc-line">70 % = {e(base_t * 0.70)} € → con el tope sin hijos de 2026, <strong>{e(paro_t)} € al mes</strong></div>
    <div class="calc-line">Indemnización por fin de contrato: {e(anual_t)} € ÷ 365 × 12 días = <strong>{e(indem(365))} €</strong></div>
    <p class="result-highlight">Pablo cobra {e(indem(365))} € al terminar y {e(paro_t)} € brutos al mes de paro durante 4 meses</p>
</div>
<p>Calcula tu caso, con tu sueldo y tus días cotizados, en la <a href="paro">calculadora del paro</a>. Si no sabes qué es la base reguladora, lo explicamos en <a href="que-es-la-base-reguladora">qué es la base reguladora</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li><strong>Vacaciones sin disfrutar:</strong> si te las pagan en el finiquito, el paro empieza cuando acabarían esos días, y el plazo de 15 días cuenta desde entonces.</li>
<li><strong>Si no llegas a 360 días</strong>, puede corresponderte un <strong>subsidio por desempleo</strong> si cumples sus requisitos: pregúntalo en el SEPE.</li>
<li>La indemnización de 12 días <strong>no se cobra</strong> en los contratos formativos ni en los de sustitución ({boe("BOE-A-2015-11430", "artículo 49.1.c del Estatuto de los Trabajadores")}).</li>
<li>Paso a paso para pedirlo: <a href="que-hacer-si-me-quedo-en-paro">qué hacer si te quedas en paro</a>.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Se cobra paro cuando se acaba un contrato temporal?', '<strong>Sí</strong>, si el contrato termina porque se acaba (no porque lo dejes tú) y has cotizado al menos <strong>360 días en los últimos 6 años</strong>. Es una situación legal de desempleo, igual que un despido (artículo 267 de la Ley General de la Seguridad Social).'),
    ('¿Cuánto paro me queda con un contrato de un año?', 'Si no has cotizado nada más en los últimos 6 años, <strong>4 meses</strong>: con 360 a 539 días cotizados corresponden 120 días de paro. Si sumas otros contratos, dura más.'),
    ('¿Me pagan indemnización al acabar un contrato temporal?', f'Sí: <strong>12 días de sueldo por año trabajado</strong>, en proporción al tiempo del contrato (artículo 49.1.c del Estatuto de los Trabajadores). Con 1.600 € al mes en 14 pagas y un año de contrato, unos <strong>{e(indem(365))} €</strong>. No se cobra en los contratos formativos ni en los de sustitución.'),
]
pagina('paro-tras-contrato-temporal', 'Paro tras un contrato temporal: cuánto y cuánto tiempo',
    f'Al acabar un contrato temporal tienes paro si has cotizado 360 días: con un año, 4 meses. Y 12 días por año de indemnización ({e(indem(365))} € con 1.600 €/mes).',
    'paro contrato temporal, paro fin de contrato temporal, cuánto paro con un contrato de un año, indemnización fin contrato temporal',
    [('Guías', 'guias'), ('Paro tras un contrato temporal', None)], cuerpo, faqs,
    'Ley General de la Seguridad Social (arts. 266 a 270) y Estatuto de los Trabajadores (art. 49.1.c), versiones consolidadas del BOE.',
    menu_activo='Guías')
sitemap('paro-tras-contrato-temporal')
print('creada: paro-tras-contrato-temporal · 1 año → paro', dias_paro(365) // 30, 'meses de', e(paro_t), '€ · indemnización', e(indem(365)), '€')
CAJA_T = '<!-- SITUACION-TEMPORAL --><p class="nota-corta">📋 <strong>¿Se te acaba un contrato temporal?</strong> Mira cuánto paro y qué indemnización te corresponden en <a href="paro-tras-contrato-temporal">paro tras un contrato temporal</a>.</p><!-- /SITUACION-TEMPORAL -->\n'
for f in ['paro.html', 'guia-paro.html']:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    ancla = next((x for x in ['<section class="faq">', '<section id="calculadoras" class="guide-section"', '<section class="section section-alt">'] if x in t), None)
    if '<!-- SITUACION-TEMPORAL -->' not in t and ancla:
        t = t.replace(ancla, CAJA_T + ancla, 1); open(ruta, 'w', encoding='utf-8').write(t)

# ===================== «¿Cuándo se cobra el paro?» (02/11/2026) =====================
# Fuente: preguntas frecuentes del SEPE (pago y cuantía): el pago es el día 10 de cada mes (si es festivo, el primer
# día hábil siguiente), por mensualidades de 30 días, en el mes siguiente al devengo y sin pagas extra.
import datetime as _dt
SEPE_FAQ = 'https://www.sepe.es/HomeSepe/prestaciones-desempleo/FAQS/pago-cuantia-prestaciones/abono-nomina-prestacion.html'
_MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
_DIA = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
NACIONALES = {'2026-12-08', '2026-12-25', '2027-01-01', '2027-01-06', '2027-03-26', '2027-05-01', '2027-10-12', '2027-11-01', '2027-12-06', '2027-12-08', '2027-12-25'}
def dia_pago(anio, mes):
    """Día 10; si cae en fin de semana o festivo nacional, el siguiente día hábil."""
    d = _dt.date(anio, mes, 10)
    while d.weekday() >= 5 or d.isoformat() in NACIONALES: d += _dt.timedelta(days=1)
    return d
hoy = _dt.date.today()                                                 # la tabla empieza en el próximo pago (se rehace al regenerar)
a, m = hoy.year, hoy.month
if hoy > dia_pago(a, m): m, a = (1, a + 1) if m == 12 else (m + 1, a)
prox = dia_pago(a, m)
pagos = []
for _ in range(12):                                                    # los 12 próximos pagos
    d = dia_pago(a, m); prev = (m - 2) % 12
    pagos.append(f'<tr><td>{_MES[m - 1].capitalize()} {a}</td><td><strong>{_DIA[d.weekday()]} {d.day}</strong></td><td>El paro de {_MES[prev]}</td></tr>')
    m += 1
    if m == 13: m, a = 1, a + 1
filas_pago = ''.join(pagos)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro</div><h1>¿Cuándo se cobra el paro?<br><span class="highlight">el día de pago, mes a mes</span></h1><p>Qué día del mes ingresa el SEPE el paro, por qué cobras el mes anterior, cuándo llega el primer pago y las fechas de los próximos meses.</p>
            {REV.replace("28 de octubre", "2 de noviembre")}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>El SEPE paga el paro el <strong>día 10 de cada mes</strong>; si es festivo, el primer día hábil siguiente.</li>
<li>Se cobra <strong>a mes vencido</strong>: el día 10 de cada mes llega el paro del mes anterior.</li>
<li>El próximo pago es el <strong>{_DIA[prox.weekday()]} {prox.day} de {_MES[prox.month - 1]}</strong>. Muchos bancos lo adelantan unos días.</li>
<li>Se paga siempre por <strong>meses de 30 días</strong> y el paro <strong>no tiene pagas extra</strong>.</li>
</ul></div>

<h2>📆 Fechas de pago del paro</h2>
<table class="info-table"><tr><th>Mes</th><th>Día de pago</th><th>Qué cobras</th></tr>{filas_pago}</table>
<p class="nota-corta">Fecha de referencia del SEPE (día 10 o el siguiente día hábil). Tu banco puede ingresarlo antes: depende de cada entidad.</p>

<h2>⏰ El primer pago</h2>
<p>El primer ingreso llega el <strong>día 10 del mes siguiente</strong> a que el SEPE apruebe tu paro, con lo que corresponda desde la fecha de inicio. Si la aprobación tarda, ese primer pago incluye también los días anteriores. Por eso conviene pedirlo cuanto antes: el plazo es de <strong>15 días hábiles</strong> (lo explicamos en <a href="que-hacer-si-me-quedo-en-paro">qué hacer si te quedas en paro</a>).</p>

<h2>❓ Dudas frecuentes sobre el cobro</h2>
<ul>
<li><strong>¿Cobro más los meses de 31 días?</strong> No: el SEPE paga siempre mensualidades de <strong>30 días</strong>.</li>
<li><strong>¿Hay pagas extra?</strong> No: ni el paro ni el subsidio tienen pagas extra.</li>
<li><strong>¿Dónde veo lo que me van a pagar?</strong> En tu Área personal del SEPE, con certificado digital, Cl@ve o un PIN que te mandan al móvil.</li>
</ul>
<p>¿Cuánto vas a cobrar? Calcúlalo en la <a href="paro">calculadora del paro</a> o mira la <a href="tabla-paro-2026">tabla del paro 2026</a>.</p>
<p class="nota-corta">Fuente: <a href="{SEPE_FAQ}" target="_blank" rel="noopener">preguntas frecuentes del SEPE sobre el pago y la cuantía de las prestaciones</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿Qué día se cobra el paro?', 'El <strong>día 10 de cada mes</strong>. Si ese día es festivo, el primer día hábil siguiente. Muchos bancos lo adelantan unos días.'),
    ('¿El paro se cobra a mes vencido?', '<strong>Sí.</strong> El día 10 cobras el paro del mes anterior: en noviembre, el de octubre.'),
    ('¿Se cobra más paro los meses de 31 días?', '<strong>No.</strong> El SEPE paga siempre mensualidades de 30 días, tenga el mes 28, 30 o 31.'),
]
pagina('cuando-se-cobra-el-paro', '¿Cuándo se cobra el paro? Día de pago y fechas',
    f'El SEPE paga el paro el día 10 de cada mes (o el siguiente día hábil), a mes vencido y por meses de 30 días. Próximo pago: {prox.day} de {_MES[prox.month - 1]}.',
    'cuándo se cobra el paro, qué día pagan el paro, día de pago del paro, cuando ingresan el paro',
    [('Guías', 'guias'), ('¿Cuándo se cobra el paro?', None)], cuerpo, faqs,
    'Preguntas frecuentes del SEPE sobre el pago y la cuantía de las prestaciones por desempleo.',
    menu_activo='Guías')
sitemap('cuando-se-cobra-el-paro')
print('creada: cuando-se-cobra-el-paro · próximo pago', prox.isoformat())

# ===================== «Me despiden estando de baja: qué hacer» (02/11/2026) =====================
# Ley 15/2022 (art. 2.1: «enfermedad o condición de salud»; art. 26: nulidad), LGSS art. 283 (baja y paro),
# LRJS art. 103 (20 días hábiles), ET arts. 55.1 (carta), 56.1 (33 días) y 49.2 (finiquito). Todo comprobado en el BOE.
PASOS_BD = [
    ('Lee la carta y no la firmes sin más', 'El despido tiene que ser por escrito, con la causa y la fecha. Fírmala como <strong>«recibido, no conforme»</strong> y guárdala: los plazos cuentan desde la fecha de efectos.'),
    ('Ten en cuenta que no pueden despedirte por estar enfermo', f'Estar de baja no impide el despido, pero la <strong>enfermedad o condición de salud</strong> es una causa de discriminación prohibida ({boe("BOE-A-2022-11589", "artículo 2.1 de la Ley 15/2022")}). Si hay indicios de que te despiden <em>por</em> la baja (llega pocos días después y sin una causa creíble), el despido puede declararse <strong>nulo</strong> ({boe("BOE-A-2022-11589", "artículo 26")}): readmisión y pago de los salarios no cobrados.'),
    ('Reclama en 20 días hábiles, aunque sigas de baja', f'El plazo para impugnar el despido es de <strong>20 días hábiles</strong> y <strong>no se para por estar de baja</strong> ({boe("BOE-A-2011-15936", "artículo 103 de la Ley de la jurisdicción social")}). Empieza por la papeleta de conciliación.'),
    ('Revisa el finiquito y la indemnización', 'El finiquito (días del mes, vacaciones y pagas extra) se cobra siempre. Si el despido es improcedente, la indemnización es de <strong>33 días por año</strong>; si es objetivo, de 20. Calcúlalo en la <a href="despido-improcedente">calculadora de despido</a>.'),
    ('Sigues cobrando la baja, pero como si fuera paro', f'Si la baja es por <strong>enfermedad común</strong>, sigues de baja hasta el alta, pero cobras <strong>lo mismo que te correspondería de paro</strong>, y ese tiempo se descuenta luego del paro ({boe("BOE-A-2015-11724", "artículo 283 de la Ley General de la Seguridad Social")}). Si es por accidente de trabajo, mantienes la cuantía de la baja.'),
    ('Cuando te den el alta, pide el paro', 'Con el alta pasas a la situación de desempleo: pide el paro en los <strong>15 días hábiles</strong> siguientes. Lo explicamos en <a href="que-hacer-si-me-quedo-en-paro">qué hacer si te quedas en paro</a>.'),
]
pasos_bd = '\n'.join(f'    <div class="calc-step"><span class="step-num">{i}</span><div><strong>{t}</strong><p>{x}</p></div></div>' for i, (t, x) in enumerate(PASOS_BD, 1))
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧭 Paso a paso</div><h1>Me despiden estando de baja<br><span class="highlight">qué hacer y qué cobras</span></h1><p>Si te despiden mientras estás de baja médica: si puede ser nulo, el plazo para reclamar, qué cobras hasta el alta y cuándo pedir el paro.</p>
            {REV.replace("28 de octubre", "2 de noviembre")}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Pueden despedirte estando de baja, pero <strong>no por estar enfermo</strong>: si hay indicios de eso, el despido puede ser <strong>nulo</strong>.</li>
<li>Tienes <strong>20 días hábiles</strong> para reclamar, y el plazo <strong>no se para</strong> por estar de baja.</li>
<li>Sigues de baja hasta el alta, pero (en enfermedad común) cobras <strong>lo que te tocaría de paro</strong>, y ese tiempo se descuenta del paro.</li>
<li>Con el alta, pide el paro en <strong>15 días hábiles</strong>.</li>
</ul></div>

<h2>✅ Los pasos, en orden</h2>
<div class="calc-steps">
{pasos_bd}
</div>

<h2>⚖️ Nulo, improcedente o procedente</h2>
<table class="info-table"><tr><th>Si el juez lo declara…</th><th>Qué pasa</th></tr>
<tr><td>Nulo</td><td>Readmisión en tu puesto y pago de los salarios que no cobraste</td></tr>
<tr><td>Improcedente</td><td>La empresa elige: readmitirte o pagarte 33 días por año (máximo 24 mensualidades)</td></tr>
<tr><td>Procedente</td><td>Se mantiene el despido; si es objetivo, cobras 20 días por año</td></tr></table>
<p class="nota-corta">Estar de baja no basta por sí solo para la nulidad: hay que aportar indicios de que el despido se debe a la enfermedad, y entonces la empresa tiene que demostrar una causa real y ajena a ella. Los tribunales aún no aplican un criterio único.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li>Todo el detalle de la baja está en la <a href="guia-baja-medica">guía de la baja médica</a>, y el del despido, en la <a href="guia-despido">guía del despido</a>.</li>
<li>Esta página es orientativa. Antes de reclamar, consulta con un abogado laboralista, un graduado social o tu sindicato.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Me pueden despedir estando de baja?', 'Sí, la baja no protege del despido. Pero no pueden despedirte <strong>por estar enfermo</strong>: la enfermedad es una causa de discriminación prohibida (Ley 15/2022) y, si hay indicios de que el despido se debe a ella, puede declararse nulo.'),
    ('¿Qué cobro si me despiden estando de baja?', 'Sigues de baja hasta el alta, pero si es por enfermedad común cobras lo mismo que te correspondería de paro, y ese tiempo se descuenta después del paro (artículo 283 de la Ley General de la Seguridad Social). Además, el finiquito y, si corresponde, la indemnización.'),
    ('¿El plazo para reclamar el despido se para si estoy de baja?', '<strong>No.</strong> Son 20 días hábiles desde el despido, estés o no de baja. No esperes al alta para presentar la papeleta de conciliación.'),
]
pagina('despido-estando-de-baja', 'Me despiden estando de baja: qué hacer y qué cobro',
    'Si te despiden estando de baja: puede ser nulo si es por la enfermedad, tienes 20 días hábiles para reclamar y cobras la baja como si fuera paro. Paso a paso.',
    'me despiden estando de baja, despido estando de baja, despido durante baja médica, qué cobro si me despiden de baja',
    [('Guías', 'guias'), ('Me despiden estando de baja', None)], cuerpo, faqs,
    'Ley 15/2022 (arts. 2.1 y 26), Ley General de la Seguridad Social (art. 283), Ley reguladora de la jurisdicción social (art. 103) y Estatuto de los Trabajadores (arts. 49, 55 y 56), versiones consolidadas del BOE.',
    menu_activo='Guías')
sitemap('despido-estando-de-baja')
CAJA_BD = '<!-- SITUACION-DESPIDO-BAJA --><p class="nota-corta">📋 <strong>¿Te han despedido estando de baja?</strong> Los pasos en orden en <a href="despido-estando-de-baja">me despiden estando de baja</a>.</p><!-- /SITUACION-DESPIDO-BAJA -->\n'
for f in ['baja-medica.html', 'despido-improcedente.html']:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    ancla = next((x for x in ['<section class="faq">', '<section class="section section-alt">'] if x in t), None)
    if '<!-- SITUACION-DESPIDO-BAJA -->' not in t and ancla:
        t = t.replace(ancla, CAJA_BD + ancla, 1); open(ruta, 'w', encoding='utf-8').write(t)
print('creada: despido-estando-de-baja')
CAJA_CP = '<!-- SITUACION-COBRO-PARO --><p class="nota-corta">📆 <strong>¿Qué día se cobra?</strong> El día 10 de cada mes: mira las fechas en <a href="cuando-se-cobra-el-paro">cuándo se cobra el paro</a>.</p><!-- /SITUACION-COBRO-PARO -->\n'
for f in ['paro.html', 'guia-paro.html', 'tabla-paro-2026.html']:
    ruta = os.path.join(RAIZ, f); t = open(ruta, encoding='utf-8').read()
    ancla = next((x for x in ['<section class="faq">', '<section id="calculadoras" class="guide-section"', '<section class="section section-alt">'] if x in t), None)
    if '<!-- SITUACION-COBRO-PARO -->' not in t and ancla:
        t = t.replace(ancla, CAJA_CP + ancla, 1); open(ruta, 'w', encoding='utf-8').write(t)
