# Páginas «Tramos del IRPF en Madrid 2026» y «Tramos del IRPF en Bizkaia 2026» (05/11/2026): búsquedas que suben
# en Google Trends («tramos irpf madrid» +60 %, «tabla irpf bizkaia 2026» +130 %).
# Escalas comprobadas en el texto oficial:
#   · Madrid: art. 1 del Decreto Legislativo 1/2010 (texto consolidado del BOE, última modificación: Ley 13/2023), más la
#     escala estatal del art. 63 de la Ley 35/2006.
#   · Bizkaia: arts. 75, 76 y 77 de la Norma Foral 13/2013 (texto de la Diputación «actualizado a fecha de 01/01/2026»).
# Uso: python3 _herramientas/irpf/gen-tramos-ccaa.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO, e, AD, RAIZ

INF = float('inf')
ESTATAL = [(12450, 0.095), (20200, 0.12), (35200, 0.15), (60000, 0.185), (300000, 0.225), (INF, 0.245)]
MADRID = [(13362.22, 0.085), (19004.63, 0.107), (35425.68, 0.128), (57320.40, 0.174), (INF, 0.205)]
BIZKAIA = [(18080, 0.23), (36160, 0.28), (54240, 0.35), (77450, 0.40), (107260, 0.45), (142960, 0.46), (208390, 0.47), (INF, 0.49)]
BIZKAIA_AHORRO = [(7500, 0.19), (15000, 0.20), (30000, 0.22), (50000, 0.24), (90000, 0.255), (120000, 0.26), (240000, 0.265), (300000, 0.27), (INF, 0.28)]
MINORACION_BIZKAIA = 1615                                   # minoración de cuota por declaración (art. 77 NF 13/2013)

pc = lambda x: f'{round(x * 100, 2):g}'.replace('.', ',') + ' %'
eu = lambda x: 'en adelante' if x == INF else f'{e(x, 2)} €'
def cuota(base, escala):
    """Impuesto de una base por tramos: cada tramo paga solo su parte."""
    total, desde = 0.0, 0.0
    for hasta, tipo in escala:
        if base > desde: total += (min(base, hasta) - desde) * tipo
        desde = hasta
    return total
def tipo_en(x, escala):
    return next(t for h, t in escala if x < h)
def filas(escala):
    """Desde · hasta · tipo · cuota acumulada al empezar el tramo."""
    out, desde = '', 0.0
    for hasta, tipo in escala:
        out += f'<tr><td>{e(desde, 2)} €</td><td>{eu(hasta)}</td><td><strong>{pc(tipo)}</strong></td><td>{e(cuota(desde, escala), 2)} €</td></tr>'
        desde = hasta
    return out
CAB = '<thead><tr><th>Desde</th><th>Hasta</th><th>Tipo</th><th>Cuota hasta ese tramo</th></tr></thead>'

# ================================================================ MADRID: escala estatal + autonómica = tipo total
cortes = sorted({h for h, _ in ESTATAL + MADRID})
f_total, desde = '', 0.0
for hasta in cortes:
    medio = (desde + min(hasta, desde + 1)) if hasta == INF else (desde + hasta) / 2
    te, ta = tipo_en(medio, ESTATAL), tipo_en(medio, MADRID)
    f_total += f'<tr><td>{e(desde, 2)} €</td><td>{eu(hasta)}</td><td>{pc(te)}</td><td>{pc(ta)}</td><td><strong>{pc(te + ta)}</strong></td></tr>'
    desde = hasta
EJ = 30000
c_est, c_mad = cuota(EJ, ESTATAL), cuota(EJ, MADRID)

cuerpo_m = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧾 IRPF 2026</div><h1>Tramos del IRPF en Madrid 2026<br><span class="highlight">del 18 % al 45 %, sumando la parte estatal y la autonómica</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>En la Comunidad de Madrid el IRPF va del <strong>18 %</strong> (hasta 12.450 €) al <strong>45 %</strong> (más de 300.000 €), sumando la parte estatal y la autonómica. La escala autonómica tiene 5 tramos, del <strong>8,5 % al 20,5 %</strong>.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>📊 Tipo total en Madrid por tramos</h2>
<p>El IRPF se paga en dos partes: una para el Estado y otra para la comunidad. Esto es lo que pagas por cada euro de cada tramo de tu <strong>base liquidable</strong> (lo que queda de tus ingresos tras restar la Seguridad Social y otros gastos):</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Desde</th><th>Hasta</th><th>Estatal</th><th>Madrid</th><th>Total</th></tr></thead><tbody>{f_total}</tbody></table></div>
<p class="nota-corta">Cada tramo solo paga su parte: con 30.000 € no pagas el 27,8 % de todo, sino el 18 % de los primeros 12.450 €, el 20,5 % de los siguientes, etc.</p>
<h2>🏛️ Escala autonómica de Madrid</h2>
<div class="tabla-wrap"><table class="tabla-festivos">{CAB}<tbody>{filas(MADRID)}</tbody></table></div>
<h2>🧮 Ejemplo con {e(EJ)} € de base liquidable</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Parte estatal:</strong><p>{e(c_est, 2)} € con la escala estatal.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Parte de Madrid:</strong><p>{e(c_mad, 2)} € con la escala autonómica.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Cuota íntegra:</strong><p><strong>{e(c_est + c_mad, 2)} €</strong>, antes de restar lo que corresponde al mínimo personal y familiar y las deducciones.</p></div></div>
</div>
<p>Lo que te retienen cada mes en la nómina sale de otra tabla, la de retenciones, que es igual en toda España salvo el País Vasco y Navarra: calcúlalo en la <a href="irpf">calculadora de IRPF</a> y mira la <a href="tramos-irpf-2026">escala estatal completa</a>.</p>
</article></div></section>
''' + AD
faqs_m = [
    ('¿Cuáles son los tramos del IRPF en Madrid en 2026?', 'Sumando la parte estatal y la autonómica: <strong>18 %</strong> hasta 12.450 €, 20,5 %, 22,7 %, 24,8 %, 27,8 %, 31,3 %, 35,9 %, 39 %, 43 % y <strong>45 %</strong> a partir de 300.000 €.'),
    ('¿Cuál es la escala autonómica de Madrid?', '<strong>8,5 %</strong> hasta 13.362,22 €; 10,7 % hasta 19.004,63 €; 12,8 % hasta 35.425,68 €; 17,4 % hasta 57.320,40 €; y <strong>20,5 %</strong> desde ahí.'),
    ('¿Se paga menos IRPF en Madrid?', 'Sí: su tipo autonómico máximo (20,5 %) es el más bajo de las comunidades de régimen común, así que el tipo total máximo es del <strong>45 %</strong>, frente al 47 % o más de otras.'),
]
fuente_m = ('<a href="https://www.boe.es/buscar/act.php?id=BOCM-m-2010-90068" target="_blank" rel="noopener">Decreto Legislativo 1/2010 de la Comunidad de Madrid</a>, art. 1 (redacción de la Ley 13/2023); '
            '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764" target="_blank" rel="noopener">Ley 35/2006 del IRPF</a>, art. 63 (escala estatal).')
pagina('tramos-irpf-madrid-2026', 'Tramos del IRPF en Madrid 2026: del 18 % al 45 %',
       'Tramos del IRPF en Madrid 2026: escala autonómica del 8,5 % al 20,5 % y tipo total, sumando la estatal, del 18 % al 45 %. Tabla y ejemplo con 30.000 €.',
       'tramos irpf madrid, tramos irpf madrid 2026, escala autonómica madrid irpf, irpf comunidad de madrid 2026',
       [('Hacienda', None), ('Tramos del IRPF', 'tramos-irpf-2026'), ('Madrid', None)], cuerpo_m, faqs_m, fuente_m)

# ================================================================ BIZKAIA: escala foral completa (no hay parte estatal)
EJB = 30000
cb = cuota(EJB, BIZKAIA); cbn = max(0, cb - MINORACION_BIZKAIA)
cuerpo_b = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧾 IRPF 2026</div><h1>Tramos del IRPF en Bizkaia 2026<br><span class="highlight">escala foral del 23 % al 49 %</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>En Bizkaia el IRPF lo regula la Diputación Foral, no Hacienda: la escala general tiene <strong>8 tramos, del 23 % al 49 %</strong>, y a la cuota se le restan <strong>1.615 €</strong> por declaración. Los ahorros pagan del 19 % al 28 %.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>📊 Escala general de Bizkaia 2026</h2>
<p>Para el sueldo, las pensiones y los demás rendimientos (la base liquidable general). Cada tramo paga solo su parte:</p>
<div class="tabla-wrap"><table class="tabla-festivos">{CAB}<tbody>{filas(BIZKAIA)}</tbody></table></div>
<p class="nota-corta">Después se resta la <strong>minoración de cuota de 1.615 €</strong> por declaración (art. 77), que hace el papel del mínimo personal del resto de España.</p>
<h2>💰 Escala del ahorro</h2>
<p>Para intereses, dividendos y ganancias al vender (la base liquidable del ahorro):</p>
<div class="tabla-wrap"><table class="tabla-festivos">{CAB}<tbody>{filas(BIZKAIA_AHORRO)}</tbody></table></div>
<h2>🧮 Ejemplo con {e(EJB)} € de base liquidable</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Escala:</strong><p>{e(cuota(18080, BIZKAIA), 2)} € por los primeros 18.080 € y el 28 % del resto: <strong>{e(cb, 2)} €</strong>.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Minoración:</strong><p>{e(cb, 2)} − 1.615 = <strong>{e(cbn, 2)} €</strong>.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Tipo medio:</strong><p>{e(cbn, 2)} ÷ {e(EJB)} = <strong>{pc(cbn / EJB)}</strong>, antes de las deducciones (por hijos, alquiler, vivienda…).</p></div></div>
</div>
<p>Lo que te retienen cada mes en la nómina sale de las <strong>tablas de retención de la Diputación Foral de Bizkaia</strong>, distintas de las del resto de España: nuestra <a href="irpf">calculadora de IRPF</a> sigue las de la Agencia Tributaria y no vale para Bizkaia. Compara con los <a href="tramos-irpf-2026">tramos del IRPF del régimen común</a>.</p>
</article></div></section>
''' + AD
faqs_b = [
    ('¿Cuáles son los tramos del IRPF en Bizkaia en 2026?', '<strong>23 %</strong> hasta 18.080 €; 28 % hasta 36.160 €; 35 % hasta 54.240 €; 40 % hasta 77.450 €; 45 % hasta 107.260 €; 46 % hasta 142.960 €; 47 % hasta 208.390 €; y <strong>49 %</strong> desde ahí.'),
    ('¿Qué es la minoración de cuota en Bizkaia?', 'Una cantidad fija que se resta a la cuota: <strong>1.615 €</strong> por declaración en 2026 (art. 77 de la Norma Foral 13/2013). Hace el papel del mínimo personal.'),
    ('¿Cómo tributan los ahorros en Bizkaia en 2026?', 'Del <strong>19 %</strong> (primeros 7.500 €) al <strong>28 %</strong> (a partir de 300.000 €), en 9 tramos.'),
    ('¿Vale la calculadora de IRPF de Hacienda para Bizkaia?', '<strong>No.</strong> Bizkaia tiene su propia norma y sus propias tablas de retención, que publica la Diputación Foral.'),
]
fuente_b = '<a href="https://www.bizkaia.eus/documents/880307/15187815/ca_13_2013.pdf" target="_blank" rel="noopener">Norma Foral 13/2013, de 5 de diciembre, del IRPF de Bizkaia</a>, arts. 75, 76 y 77 (texto actualizado a 1 de enero de 2026).'
pagina('tramos-irpf-bizkaia-2026', 'Tramos del IRPF en Bizkaia 2026: escala foral (23-49 %)',
       'Tabla del IRPF de Bizkaia 2026: escala general del 23 % al 49 % en 8 tramos, minoración de 1.615 € y escala del ahorro del 19 % al 28 %. Con un ejemplo.',
       'tabla irpf bizkaia 2026, tramos irpf bizkaia, irpf bizkaia 2026, escala irpf bizkaia, irpf país vasco 2026',
       [('Hacienda', None), ('Tramos del IRPF', 'tramos-irpf-2026'), ('Bizkaia', None)], cuerpo_b, faqs_b, fuente_b)

_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
for slug in ('tramos-irpf-madrid-2026', 'tramos-irpf-bizkaia-2026'):
    if f'/{slug}<' not in _s:
        _s = _s.replace('</urlset>', f'    <url><loc>https://calculalotuyo.es/{slug}</loc><lastmod>2026-11-05</lastmod><priority>0.7</priority></url>\n</urlset>')
open(_sm, 'w', encoding='utf-8').write(_s)
print(f'tramos Madrid y Bizkaia · Madrid 30.000 € → {e(c_est + c_mad, 2)} € · Bizkaia 30.000 € → {e(cbn, 2)} €')
