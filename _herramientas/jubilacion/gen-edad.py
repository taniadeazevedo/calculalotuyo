# Página «Edad de jubilación 2027» (edad-jubilacion-2027.html), 05/11/2026: la búsqueda sube un 300 % en Google Trends.
# Edad ordinaria según la disposición transitoria 7.ª de la Ley General de la Seguridad Social (calendario de la Ley 27/2011)
# y jubilación anticipada (arts. 207 y 208 LGSS). Uso: python3 _herramientas/jubilacion/gen-edad.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, AD, REVISADO, RAIZ

# Año → (cotizado para jubilarse a los 65, edad si se tiene menos)
ORDINARIA = [(2025, '38 años y 3 meses', '66 años y 8 meses'), (2026, '38 años y 3 meses', '66 años y 10 meses'), (2027, '38 años y 6 meses', '67 años')]
filas = ''.join(f'<tr><td>{a}{" en adelante" if a == 2027 else ""}</td><td><strong>65 años</strong> con {c} cotizados o más</td><td><strong>{edad}</strong> con menos</td></tr>' for a, c, edad in ORDINARIA)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🌅 Jubilación 2027</div><h1>Edad de jubilación 2027<br><span class="highlight">a los 67, o a los 65 con 38 años y medio cotizados</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>En 2027 te jubilas a los <strong>67 años</strong>, o a los <strong>65</strong> si tienes al menos <strong>38 años y 6 meses cotizados</strong>. Desde 2027 ya no cambia: es la edad definitiva de la reforma de 2011.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>📅 Edad ordinaria de jubilación por año</h2>
<p>La edad sube poco a poco desde 2013 y llega a su punto final en 2027. Depende del año en que te jubiles y de cuánto hayas cotizado:</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Año en que te jubilas</th><th>Con carrera larga</th><th>Si no</th></tr></thead><tbody>{filas}</tbody></table></div>
<h2>⏩ Jubilación anticipada en 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Tipo</th><th>Edad más temprana</th><th>Cotizado mínimo</th></tr></thead><tbody>
<tr><td>Voluntaria (porque tú quieres)</td><td><strong>65 años</strong> (63 con 38 años y 6 meses cotizados)</td><td>35 años</td></tr>
<tr><td>Involuntaria (despido, ERE, cierre)</td><td><strong>63 años</strong> (61 con 38 años y 6 meses cotizados)</td><td>33 años</td></tr>
</tbody></table></div>
<p>La anticipada se puede pedir hasta <strong>2 años antes</strong> de tu edad ordinaria si es voluntaria y hasta <strong>4 años antes</strong> si es involuntaria, pero la pensión baja con unos <strong>coeficientes reductores</strong> por cada mes que adelantes (arts. 207 y 208 de la Ley General de la Seguridad Social).</p>
<h2>🧮 Cuánto cobrarás</h2>
<p>Para tener pensión necesitas <strong>15 años cotizados</strong> (2 de ellos en los últimos 15). Con 15 años cobras el 50 % de tu base reguladora, y para el <strong>100 % necesitas 37 años</strong> cotizados en 2027. Calcula tu caso en la <a href="jubilacion">calculadora de jubilación</a> y mira <a href="subida-pensiones-2027">cuánto subirán las pensiones en 2027</a>.</p>
</article></div></section>
''' + AD

faqs = [
    ('¿A qué edad me puedo jubilar en 2027?', 'A los <strong>67 años</strong>, o a los <strong>65</strong> si tienes al menos <strong>38 años y 6 meses cotizados</strong>.'),
    ('¿Cuál es la edad de jubilación en 2026?', 'A los <strong>66 años y 10 meses</strong>, o a los 65 con al menos 38 años y 3 meses cotizados.'),
    ('¿Puedo jubilarme antes de los 65?', 'Sí, con la <strong>jubilación anticipada</strong>: en 2027, desde los 63 si es voluntaria y tienes 38 años y 6 meses cotizados, o desde los 61 si es involuntaria (por despido). La pensión baja por cada mes que adelantes.'),
    ('¿Qué es la jubilación flexible?', 'Es volver a trabajar a <strong>tiempo parcial</strong> cuando ya cobras la pensión: la pensión se reduce en proporción a la jornada que trabajes y, al dejar el trabajo, se recalcula con lo que hayas cotizado de más.'),
    ('¿Cuántos años hay que cotizar para cobrar el 100 % de la pensión?', 'En 2027, <strong>37 años</strong>. Con 15 años (el mínimo) cobras el 50 % de tu base reguladora.'),
]
fuente = ('<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724" target="_blank" rel="noopener">Ley General de la Seguridad Social</a> '
          '(art. 205, arts. 207 y 208 y disposición transitoria 7.ª, con el calendario de la Ley 27/2011).')
pagina('edad-jubilacion-2027', 'Edad de jubilación 2027: a qué edad te puedes jubilar',
       'En 2027 te jubilas a los 67 años, o a los 65 con 38 años y 6 meses cotizados. Tabla por año, jubilación anticipada y años que necesitas para el 100 %.',
       'edad de jubilación 2027, edad jubilación, a qué edad me puedo jubilar, jubilación anticipada 2027, jubilación flexible',
       [('Jubilación', 'jubilacion'), ('Edad de jubilación 2027', None)], cuerpo, faqs, fuente)

_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
if '/edad-jubilacion-2027<' not in _s:
    _s = _s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/edad-jubilacion-2027</loc><lastmod>2026-11-05</lastmod><priority>0.8</priority></url>\n</urlset>')
    open(_sm, 'w', encoding='utf-8').write(_s)
print('edad-jubilacion-2027')
