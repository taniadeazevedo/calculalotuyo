# Página «Pensión mínima y máxima 2026» (pension-minima-maxima-2026.html), 05/11/2026.
# Cifras oficiales del Real Decreto-ley 3/2026 (BOE-A-2026-2548): art. 1 (pensión máxima), art. 2 y anexo I (mínimas).
# La previsión de 2027 usa la subida estimada del artículo de pensiones (se lee de subida-pensiones-2027.html).
# Lanzar DESPUÉS de novedades/gen-novedades.py. Uso: python3 _herramientas/jubilacion/gen-pensiones-minimas.py
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, AD, REVISADO, RAIZ

MAXIMA = 3359.60                                            # al mes, 14 pagas (47.034,40 € al año)
_pen = open(os.path.join(RAIZ, 'subida-pensiones-2027.html'), encoding='utf-8').read()
_max27 = float(re.search(r'<tr><td>4,9 %</td><td><strong>[\d,]+ %</strong></td><td>([\d.,]+) € al mes', _pen).group(1).replace('.', '').replace(',', '.'))   # pensión máxima 2027 del escenario central del artículo
SUBIDA = (_max27 / MAXIMA - 1) * 100                         # la misma subida exacta que usa el artículo (≈ 3,59 %)
mes = lambda anual: anual / 14                              # las cuantías del BOE son anuales, en 14 pagas
# Mínimas de jubilación y viudedad (euros al año): (tipo, con cónyuge a cargo, sin cónyuge, con cónyuge no a cargo)
JUBILACION = [('Jubilación, con 65 años o más', 17592.40, 13106.80, 12441.80),
              ('Jubilación, con menos de 65 años', 17592.40, 12262.60, 11590.60),
              ('Incapacidad permanente absoluta', 17592.40, 13106.80, 12441.80)]
VIUDEDAD = [('Con cargas familiares', 17592.40), ('Con 65 años o más (o discapacidad del 65 %)', 13106.80),
            ('Entre 60 y 64 años', 12262.60), ('Con menos de 60 años', 9931.60)]
NO_CONTRIBUTIVA = 8803.20

f_jub = ''.join(f'<tr><td>{t}</td><td><strong>{e(mes(a), 2)} €</strong></td><td><strong>{e(mes(b), 2)} €</strong></td><td>{e(mes(c), 2)} €</td></tr>' for t, a, b, c in JUBILACION)
f_viu = ''.join(f'<tr><td>{t}</td><td><strong>{e(mes(a), 2)} €</strong></td><td>{e(a, 2)} €</td></tr>' for t, a in VIUDEDAD)
pc = lambda x: f'{x:.2f}'.replace('.', ',') + ' %'

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">👵 Pensiones 2026</div><h1>Pensión mínima y máxima 2026<br><span class="highlight">y lo que se espera para 2027</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>En 2026 la <strong>pensión máxima es de {e(MAXIMA, 2)} € al mes</strong> (14 pagas). La <strong>mínima de jubilación</strong> con 65 años es de <strong>{e(mes(13106.80), 2)} € al mes</strong> si vives solo y de {e(mes(17592.40), 2)} € con cónyuge a cargo. La no contributiva, {e(mes(NO_CONTRIBUTIVA), 2)} €.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>📈 Pensión máxima 2026 y 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Año</th><th>Al mes (14 pagas)</th><th>Al año</th></tr></thead><tbody>
<tr><td>2026</td><td><strong>{e(MAXIMA, 2)} €</strong></td><td>{e(MAXIMA * 14, 2)} €</td></tr>
<tr><td>2027 (previsión con un {pc(SUBIDA)})</td><td><strong>{e(MAXIMA * (1 + SUBIDA / 100), 2)} €</strong></td><td>{e(MAXIMA * (1 + SUBIDA / 100) * 14, 2)} €</td></tr>
</tbody></table></div>
<p>Nadie cobra más de la pensión máxima, aunque haya cotizado mucho. La de 2027 se sabrá cuando el Gobierno fije la subida con el IPC de noviembre: lo explicamos en <a href="subida-pensiones-2027">cuánto subirán las pensiones en 2027</a>.</p>

<h2>🧾 Pensión mínima de jubilación 2026</h2>
<p>Si tu pensión no llega a estas cifras y tus otros ingresos son bajos, la Seguridad Social te paga la diferencia (el <strong>complemento a mínimos</strong>). Cantidades al mes, en 14 pagas:</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Tipo de pensión</th><th>Con cónyuge a cargo</th><th>Sin cónyuge (vives solo)</th><th>Con cónyuge no a cargo</th></tr></thead><tbody>{f_jub}</tbody></table></div>
<p class="nota-corta">Para cobrar el complemento a mínimos, tus otros ingresos no pueden pasar de 9.442 € al año (11.013 € con cónyuge a cargo).</p>

<h2>👵 Pensión mínima de viudedad 2026</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Situación</th><th>Al mes (14 pagas)</th><th>Al año</th></tr></thead><tbody>{f_viu}</tbody></table></div>

<h2>🤝 Pensión no contributiva 2026</h2>
<p>Para quien no ha cotizado lo suficiente y tiene pocos ingresos: <strong>{e(mes(NO_CONTRIBUTIVA), 2)} € al mes</strong> en 14 pagas ({e(NO_CONTRIBUTIVA, 2)} € al año), de jubilación o de invalidez.</p>

<h2>🔮 ¿Y en 2027?</h2>
<p>Las pensiones mínimas suben <strong>al menos lo mismo que las demás</strong> (en torno a un {pc(SUBIDA)}) y en los últimos años el Gobierno las ha subido más, para acercarlas al umbral de la pobreza. Con un {pc(SUBIDA)}, la mínima de jubilación para quien vive solo pasaría a unos <strong>{e(mes(13106.80) * (1 + SUBIDA / 100), 2)} € al mes</strong>. Las cifras oficiales saldrán en el BOE a finales de diciembre o en enero.</p>
<p>¿Cuándo te puedes jubilar? Míralo en <a href="edad-jubilacion-2027">edad de jubilación 2027</a>, y calcula tu pensión en la <a href="jubilacion">calculadora de jubilación</a>.</p>
</article></div></section>
''' + AD

faqs = [
    ('¿Cuál es la pensión máxima de jubilación en 2026?', f'<strong>{e(MAXIMA, 2)} € al mes</strong> en 14 pagas, {e(MAXIMA * 14, 2)} € al año (Real Decreto-ley 3/2026).'),
    ('¿Cuál es la pensión mínima de jubilación en 2026?', f'Con 65 años o más: <strong>{e(mes(13106.80), 2)} € al mes</strong> si no tienes cónyuge, {e(mes(17592.40), 2)} € con cónyuge a cargo y {e(mes(12441.80), 2)} € con cónyuge no a cargo (14 pagas).'),
    ('¿Cuánto será la pensión máxima en 2027?', f'Unos <strong>{e(MAXIMA * (1 + SUBIDA / 100), 2)} € al mes</strong> si sube un {pc(SUBIDA)}, la subida que sale con el IPC hasta octubre. Se confirmará en diciembre.'),
    ('¿Cuánto es la pensión no contributiva en 2026?', f'<strong>{e(mes(NO_CONTRIBUTIVA), 2)} € al mes</strong> en 14 pagas ({e(NO_CONTRIBUTIVA, 2)} € al año).'),
    ('¿Qué es el complemento a mínimos?', 'Lo que paga la Seguridad Social para que tu pensión llegue a la mínima, si tus otros ingresos no pasan de <strong>9.442 € al año</strong> (11.013 € con cónyuge a cargo).'),
]
fuente = '<a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-2548" target="_blank" rel="noopener">Real Decreto-ley 3/2026, de 3 de febrero</a> (art. 1, art. 2.5 y anexo I: cuantías mínimas de 2026).'
pagina('pension-minima-maxima-2026', 'Pensión mínima y máxima 2026: cuánto es (y en 2027)',
       f'Pensión máxima 2026: {e(MAXIMA, 2)} € al mes. Mínima de jubilación: {e(mes(13106.80), 2)} € (sin cónyuge) y {e(mes(17592.40), 2)} € (con cónyuge a cargo). Viudedad, no contributiva y 2027.',
       'pension minima 2026, pension maxima 2026, pension minima jubilacion 2026, cual es la pension maxima de jubilacion, pension maxima 2027, pension no contributiva 2026',
       [('Jubilación', 'jubilacion'), ('Pensión mínima y máxima 2026', None)], cuerpo, faqs, fuente)

_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
if '/pension-minima-maxima-2026<' not in _s:
    _s = _s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/pension-minima-maxima-2026</loc><lastmod>2026-11-05</lastmod><priority>0.8</priority></url>\n</urlset>')
    open(_sm, 'w', encoding='utf-8').write(_s)
print(f'pension-minima-maxima-2026 · máxima 2027 ≈ {e(MAXIMA * (1 + SUBIDA / 100), 2)} €')
