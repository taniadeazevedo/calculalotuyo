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
    <div class="calc-step"><span class="step-num">1</span><div><strong>Tu base reguladora diaria</strong><p>Es tu base de cotización del mes anterior a la baja dividida entre 30 (ya incluye la parte de las pagas extra). Con 2.000 € al mes: {e(2000 / 30, 2)} € al día.</p></div></div>
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
