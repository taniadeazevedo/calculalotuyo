# Página «Tramos del IRPF 2026» (23/10/2026): búsqueda muy frecuente («tramos irpf 2026», «escala irpf»).
# Escalas comprobadas en el BOE: art. 85 del Reglamento del IRPF (escala de retención de la nómina, la misma que usa
# la calculadora, en datos-2026.js) y art. 63 de la Ley del IRPF (escala estatal de la declaración).
# Los ejemplos se calculan aquí con esas escalas, no a mano. Uso: python3 _herramientas/irpf/gen-tramos.py
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))                     # carpeta de este script
sys.path.insert(0, os.path.join(AQUI, '..'))                         # para importar la plantilla común
from plantilla import pagina, REVISADO, e, RAIZ                      # e(1234.5, 2) → «1.234,50»

# Escala de retención: se lee de datos-2026.js (la misma de la calculadora), así en enero se actualiza sola
datos = open(os.path.join(RAIZ, 'datos-2026.js'), encoding='utf-8').read()
bloque = re.search(r'escala:\[(\[\d+,0\.\d+\](?:,\[(?:\d+|Infinity),0\.\d+\])*)\]', datos).group(1)
RETENCION = [(float('inf') if h == 'Infinity' else float(h), float(t)) for h, t in re.findall(r'\[(\d+|Infinity),(0\.\d+)\]', bloque)]
# Escala estatal de la declaración (art. 63 de la Ley del IRPF)
ESTATAL = [(12450, 0.095), (20200, 0.12), (35200, 0.15), (60000, 0.185), (300000, 0.225), (float('inf'), 0.245)]
MINIMO = 5550                                                        # mínimo personal general (art. 57 LIRPF)

def cuota(base, escala):
    """Impuesto de una base con una escala por tramos: cada tramo paga solo su parte."""
    total, desde = 0.0, 0.0
    for hasta, tipo in escala:
        if base > desde: total += (min(base, hasta) - desde) * tipo
        desde = hasta
    return total

pc = lambda x: f'{round(x * 100, 2):g}'.replace('.', ',') + ' %'      # 0.095 → «9,5 %»; 0.19 → «19 %»
def filas(escala):
    """Filas de la tabla: desde, hasta, tipo y lo que se paga acumulado al llegar al tramo."""
    out, desde = [], 0.0
    for hasta, tipo in escala:
        h = 'en adelante' if hasta == float('inf') else e(hasta) + ' €'
        out.append(f'<tr><td>{e(desde)} €</td><td>{h}</td><td><strong>{pc(tipo)}</strong></td><td>{e(cuota(desde, escala), 2)} €</td></tr>')
        desde = hasta
    return ''.join(out)

# Ejemplo: base de 25.000 € con la escala de retención, tramo a tramo
BASE = 25000
pasos, desde = [], 0.0
for hasta, tipo in RETENCION:
    if BASE > desde:
        parte = min(BASE, hasta) - desde
        pasos.append(f'<div class="calc-line">{e(parte)} € al {pc(tipo)} = {e(parte * tipo, 2)} €</div>')
    desde = hasta
c_base, c_min = cuota(BASE, RETENCION), cuota(MINIMO, RETENCION)
neto = c_base - c_min
ejemplo = f'''<div class="example-box">
    <h4>🧮 Ejemplo: base de {e(BASE)} €</h4>
    <p>Con la escala de la nómina, cada parte de la base paga el tipo de su tramo:</p>
    {''.join(pasos)}
    <div class="calc-line">Total: {e(c_base, 2)} € − lo del mínimo personal ({e(MINIMO)} € al 19 % = {e(c_min, 2)} €)</div>
    <p class="result-highlight">Impuesto: {e(neto, 2)} €, un {e(neto / BASE * 100, 2)} % de la base (no el 30 % del último tramo)</p>
</div>'''

REV = REVISADO.format(fecha='23 de octubre de 2026')
boe = lambda id_, txt: f'<a href="https://www.boe.es/buscar/act.php?id={id_}" target="_blank" rel="noopener">{txt}</a>'
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Escala oficial</div><h1>Tramos del IRPF 2026<br><span class="highlight">qué porcentaje pagas por cada parte</span></h1><p>Los tramos de la retención de la nómina y de la declaración de la renta de 2026, con un ejemplo calculado y la explicación de por qué no pagas el tipo de tu tramo sobre todo el sueldo.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>En la nómina, los tramos van del <strong>19 %</strong> (hasta 12.450 €) al <strong>47 %</strong> (más de 300.000 €).</li>
<li>Cada tramo paga <strong>solo su parte</strong>: subir de tramo no encarece todo el sueldo.</li>
<li>Al tipo final se le descuenta el <strong>mínimo personal (5.550 €)</strong> y el de tus hijos.</li>
<li>En la declaración de la renta, la mitad estatal va del 9,5 % al 24,5 % y la otra parte la pone <strong>tu comunidad</strong>.</li>
</ul></div>

<h2>💼 Tramos de la retención de la nómina 2026</h2>
<p>Es la escala que usa la empresa para calcular cuánto IRPF te quita cada mes ({boe("BOE-A-2007-6820", "artículo 85 del Reglamento del IRPF")}). Es la misma en toda España, salvo en el País Vasco y Navarra, que tienen la suya.</p>
<table class="info-table"><tr><th>Desde</th><th>Hasta</th><th>Tipo</th><th>Pagas al llegar</th></tr>{filas(RETENCION)}</table>
<p>«Pagas al llegar» es lo que suman los tramos anteriores: con una base de 35.200 €, por ejemplo, {e(cuota(35200, RETENCION), 2)} € antes de descontar el mínimo personal.</p>

<h2>📐 Cómo se aplican los tramos</h2>
{ejemplo}
<p>El porcentaje real que te retienen sale de dividir ese impuesto entre tu sueldo bruto, y suele ser bastante menor que el del último tramo. Calcula el tuyo con la <a href="irpf">calculadora de IRPF</a>.</p>

<h2>🧾 Tramos estatales de la declaración de la renta</h2>
<p>En la declaración anual, el impuesto se divide en dos mitades: la <strong>estatal</strong>, igual para todos ({boe("BOE-A-2006-20764", "artículo 63 de la Ley del IRPF")}), y la <strong>autonómica</strong>, que fija cada comunidad con sus propios tramos.</p>
<table class="info-table"><tr><th>Desde</th><th>Hasta</th><th>Tipo estatal</th><th>Pagas al llegar</th></tr>{filas(ESTATAL)}</table>
<p>Por eso el resultado de la renta puede cambiar de una comunidad a otra aunque ganes lo mismo. ¿Tienes que presentarla? Compruébalo en <a href="obligado-a-declarar-renta">¿tengo que hacer la renta?</a></p>
</article></div></section>
'''
faqs = [
    ('¿Cuáles son los tramos del IRPF en 2026?',
     'En la retención de la nómina: <strong>19 %</strong> hasta 12.450 €, <strong>24 %</strong> hasta 20.200 €, <strong>30 %</strong> hasta 35.200 €, <strong>37 %</strong> hasta 60.000 €, <strong>45 %</strong> hasta 300.000 € y <strong>47 %</strong> a partir de ahí (artículo 85 del Reglamento del IRPF).'),
    ('Si paso al siguiente tramo, ¿pago más IRPF por todo mi sueldo?',
     '<strong>No.</strong> Cada tramo solo grava la parte de la base que cae dentro de él. Si subes de tramo, solo los euros de más pagan el tipo nuevo; el resto sigue igual.'),
    ('¿Por qué la nómina y la renta tienen tramos distintos?',
     'La nómina usa una <strong>escala única</strong> para toda España, para calcular la retención. En la declaración, el impuesto se divide en una parte <strong>estatal</strong> (del 9,5 % al 24,5 %) y una <strong>autonómica</strong> que fija cada comunidad. Por eso en la renta puede salirte a pagar o a devolver.'),
    ('¿Los tramos del IRPF valen para el País Vasco y Navarra?',
     '<strong>No.</strong> El País Vasco y Navarra tienen su propio IRPF, con escalas y tablas de retención que publican sus haciendas forales.'),
]
pagina('tramos-irpf-2026', 'Tramos del IRPF 2026: escala de retención y de la renta',
    'Tramos del IRPF 2026: del 19 % al 47 % en la nómina y escala estatal de la renta. Con un ejemplo calculado tramo a tramo y la ley del BOE.',
    'tramos irpf 2026, escala irpf 2026, tramos irpf, tipos irpf 2026, escala de retenciones',
    [('Calculadora de IRPF', 'irpf'), ('Tramos del IRPF 2026', None)], cuerpo, faqs,
    'Reglamento del IRPF (art. 85, escala de retención) y Ley 35/2006 del IRPF (arts. 57 y 63), versiones consolidadas del BOE.',
    menu_activo='Hacienda')

# Sitemap: se añade si falta (sitemap.py pone la fecha buena)
sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
if '/tramos-irpf-2026<' not in s:
    s = s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/tramos-irpf-2026</loc><lastmod>2026-10-23</lastmod><priority>0.8</priority></url>\n</urlset>')
    open(sm, 'w', encoding='utf-8').write(s)
print('creada: tramos-irpf-2026 · base 25.000 € →', e(neto, 2), '€')
