# Página «Autónomo colaborador 2026» (autonomo-colaborador.html), 05/11/2026: «bonificación autónomo colaborador» +60 % en Trends.
# Bonificación: art. 35 de la Ley 20/2007 del Estatuto del Trabajo Autónomo (texto consolidado del BOE): 50 % los 18 primeros
# meses y 25 % los 6 siguientes de la cuota por contingencias comunes de la base mínima del tramo 1 de la tabla general.
# Bases y tipos: datos-2026.js (los mismos que la calculadora de cuota de autónomos). Uso: python3 _herramientas/autonomos/gen-colaborador.py
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO, e, AD, RAIZ

datos = open(os.path.join(RAIZ, 'datos-2026.js'), encoding='utf-8').read()
TIPO = float(re.search(r'autonomos:\{\s*tipo:([\d.]+)', datos).group(1))                       # 0,315
BASE_COLAB = float(re.search(r'baseMinimaSocietario:([\d.]+)', datos).group(1))                 # 1.000 € (también familiares colaboradores)
BASE_T1 = float(re.search(r'\[1300,([\d.]+)\]', datos).group(1))                                 # tramo 1 de la tabla general: 950,98 €
CC = 0.283                                                                                         # contingencias comunes
cuota = BASE_COLAB * TIPO
bon50, bon25 = BASE_T1 * CC * 0.50, BASE_T1 * CC * 0.25
ahorro = bon50 * 18 + bon25 * 6

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">💼 Autónomos 2026</div><h1>Autónomo colaborador 2026<br><span class="highlight">requisitos, cuota y bonificación</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Es el familiar (cónyuge, pareja de hecho o pariente hasta segundo grado) que trabaja de forma habitual en el negocio de un autónomo. Si no ha sido autónomo en los últimos 5 años, tiene una <strong>bonificación del 50 % durante 18 meses y del 25 % otros 6</strong>: con la base mínima, paga unos <strong>{e(cuota - bon50, 2)} € al mes</strong> al principio en vez de {e(cuota, 2)} €.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>👥 Quién puede ser autónomo colaborador</h2>
<ul>
<li>El <strong>cónyuge</strong>, la <strong>pareja de hecho</strong> o un familiar del autónomo <strong>hasta el segundo grado</strong> (padres, hijos, hermanos, abuelos, nietos y los mismos parientes políticos), también por adopción.</li>
<li>Que trabaje en el negocio de forma <strong>habitual, personal y directa</strong>, sin contrato de trabajo.</li>
<li>Se da de alta en el régimen de autónomos (RETA) como familiar colaborador.</li>
</ul>
<h2>💶 Cuánto paga</h2>
<p>Cotiza como cualquier autónomo, según sus rendimientos, con una <strong>base mínima de {e(BASE_COLAB)} € al mes</strong>. Con esa base y el {str(round(TIPO * 100, 1)).replace(".", ",")} % de cotización, la cuota es de <strong>{e(cuota, 2)} € al mes</strong>.</p>
<h2>🎁 La bonificación de 24 meses</h2>
<p>Si el familiar <strong>no ha estado de alta como autónomo en los 5 años anteriores</strong>, tiene derecho a una rebaja sobre la cuota de contingencias comunes de la base mínima del tramo 1 ({e(BASE_T1, 2)} €):</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Meses desde el alta</th><th>Bonificación</th><th>Rebaja al mes</th><th>Cuota con la base mínima</th></tr></thead><tbody>
<tr><td>Del 1 al 18</td><td>50 %</td><td>−{e(bon50, 2)} €</td><td><strong>{e(cuota - bon50, 2)} €</strong></td></tr>
<tr><td>Del 19 al 24</td><td>25 %</td><td>−{e(bon25, 2)} €</td><td><strong>{e(cuota - bon25, 2)} €</strong></td></tr>
<tr><td>Desde el 25</td><td>—</td><td>—</td><td><strong>{e(cuota, 2)} €</strong></td></tr>
</tbody></table></div>
<p class="nota-corta">En total, unos <strong>{e(ahorro)} € de ahorro</strong> en dos años. Se pide al darse de alta. Cálculo propio con el art. 35 de la Ley del Estatuto del Trabajo Autónomo y las bases de 2026.</p>
<p>¿Es tu primer año como autónomo titular? Mira la <a href="tarifa-plana-autonomos-2026">tarifa plana 2026</a> y calcula tu cuota con la <a href="cuota-autonomos">calculadora de cuota de autónomos</a>.</p>
</article></div></section>
''' + AD
faqs = [
    ('¿Qué es un autónomo colaborador?', 'El <strong>familiar del autónomo</strong> (cónyuge, pareja de hecho o pariente hasta segundo grado) que trabaja de forma habitual en su negocio sin contrato laboral, dado de alta en el régimen de autónomos.'),
    ('¿Cuánto paga un autónomo colaborador en 2026?', f'Con la base mínima de {e(BASE_COLAB)} €, <strong>{e(cuota, 2)} € al mes</strong>. Con la bonificación, {e(cuota - bon50, 2)} € los 18 primeros meses y {e(cuota - bon25, 2)} € los 6 siguientes.'),
    ('¿Qué bonificación tiene el autónomo colaborador?', 'El <strong>50 % durante 18 meses</strong> y el <strong>25 % durante 6 meses más</strong> de la cuota de contingencias comunes de la base mínima del tramo 1, si no ha sido autónomo en los 5 años anteriores (art. 35 de la Ley 20/2007).'),
    ('¿Puede el hijo de un autónomo ser autónomo colaborador?', 'Sí: los hijos son familiares de primer grado. También los padres, hermanos, abuelos y nietos, y los mismos parientes del cónyuge.'),
]
fuente = ('<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409" target="_blank" rel="noopener">Ley 20/2007 del Estatuto del Trabajo Autónomo</a>, art. 35; '
          'bases y tipos de 2026: Real Decreto-ley 3/2026 y Real Decreto-ley 13/2022.')
pagina('autonomo-colaborador', 'Autónomo colaborador 2026: requisitos, cuota y bonificación',
       f'Autónomo colaborador familiar en 2026: quién puede serlo, cuota de {e(cuota, 2)} € con la base mínima y bonificación del 50 % 18 meses y del 25 % otros 6.',
       'autonomo colaborador, bonificacion autonomo colaborador, autonomo colaborador familiar 2026, cuota autonomo colaborador, alta autonomo colaborador',
       [('Autónomos', 'cuota-autonomos'), ('Autónomo colaborador', None)], cuerpo, faqs, fuente)

_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
if '/autonomo-colaborador<' not in _s:
    _s = _s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/autonomo-colaborador</loc><lastmod>2026-11-05</lastmod><priority>0.7</priority></url>\n</urlset>')
    open(_sm, 'w', encoding='utf-8').write(_s)
print(f'autonomo-colaborador · cuota {e(cuota, 2)} € · con 50 % {e(cuota - bon50, 2)} €')
