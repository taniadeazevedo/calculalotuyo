# Página «Jubilación flexible 2026» con calculadora (jubilacion-flexible.html), 05/11/2026: la búsqueda sube un 550 %.
# Reglas del Real Decreto 416/2026 (BOE-A-2026-11474), en vigor desde el 28/08/2026:
#   · trabajo por cuenta ajena a tiempo parcial: jornada entre el 33 % y el 80 % de una completa
#   · la pensión baja en proporción a la jornada (trabajas el 60 % → cobras el 40 %)
#   · si empiezas a trabajar 6 meses o más después de jubilarte: +25 % de la pensión anterior (jornada del 55 al 80 %)
#     o +15 % (jornada del 33 al 55 %)
#   · por cuenta propia (sin haber sido autónomo los 3 años antes): cobras el 25 % de la pensión
# Uso: python3 _herramientas/jubilacion/gen-flexible.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, AD, REVISADO, RAIZ

def cobras(jornada, seis_meses=True):
    """% de la pensión que se cobra trabajando esa jornada (por cuenta ajena)."""
    extra = (25 if jornada >= 55 else 15) if seis_meses else 0
    return min(100, 100 - jornada + extra)

EJ = 1500
filas = ''.join(f'<tr><td>{j} %</td><td>{100 - j} % · {e(EJ * (100 - j) / 100)} €</td><td><strong>{cobras(j)} % · {e(EJ * cobras(j) / 100)} €</strong></td></tr>' for j in (33, 40, 50, 55, 60, 70, 80))

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🌅 Jubilación 2026</div><h1>Jubilación flexible 2026<br><span class="highlight">trabaja a media jornada y sigue cobrando parte de tu pensión</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Desde el <strong>28 de agosto de 2026</strong> puedes volver a trabajar entre el <strong>33 % y el 80 %</strong> de una jornada completa sin perder toda la pensión: cobras la parte que no trabajas y, si empiezas 6 meses o más después de jubilarte, <strong>un 15 % o un 25 % más</strong> (Real Decreto 416/2026).</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">🌅</div>Calcula tu pensión trabajando</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="pension">Tu pensión al mes (€)</label><input type="number" class="form-input" id="pension" placeholder="1500" min="1" step="0.01" required></div>
                <div class="form-group"><label class="form-label" for="tipo">¿Cómo vas a trabajar?</label><select class="form-select" id="tipo"><option value="ajena">Por cuenta ajena, a tiempo parcial</option><option value="propia">Por cuenta propia (autónomo)</option></select></div>
                <div class="form-group" id="jornadaGrupo"><label class="form-label" for="jornada">Jornada que vas a trabajar (%)</label><input type="number" class="form-input" id="jornada" placeholder="50" min="33" max="80" step="1"><span class="form-hint">Entre el 33 % y el 80 % de una jornada completa</span></div>
                <div class="form-group" id="mesesGrupo"><label class="form-label" for="meses">¿Empiezas 6 meses o más después de jubilarte?</label><select class="form-select" id="meses"><option value="si">Sí</option><option value="no">No</option></select></div>
            </div>
            <button type="submit" class="btn">Calcular</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        <div class="result" id="result">
            <div class="result-hero"><p class="result-label">Pensión que cobrarías trabajando</p><p class="result-value" id="total">0 €</p><p class="result-sub" id="resultSub"></p></div>
            <div class="result-breakdown">
                <div class="result-row"><span class="result-row-label">🌅 Tu pensión ahora</span><span class="result-row-value" id="rAhora">0 €</span></div>
                <div class="result-row bruto"><span class="result-row-label">📉 Por la jornada</span><span class="result-row-value" id="rBase">0 €</span></div>
                <div class="result-row exento"><span class="result-row-label">➕ Incremento</span><span class="result-row-value" id="rExtra">0 €</span></div>
            </div>
            <div class="fiscal-box"><div class="fiscal-title">⚖️ Por qué</div><div id="porque"></div></div>
            <div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button></div>
        </div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📌 Qué es la jubilación flexible</h2>
<p>Es volver a trabajar cuando ya cobras la pensión de jubilación, sin perderla del todo. Mientras trabajas, la pensión <strong>baja en proporción a tu jornada</strong> y sigues cotizando: cuando lo dejes, te recalculan la pensión con lo que hayas cotizado de más.</p>
<h2>📌 Lo que cambió el 28 de agosto de 2026</h2>
<ul>
<li>La jornada puede ir del <strong>33 % al 80 %</strong> de una completa (antes, los límites del contrato a tiempo parcial).</li>
<li>Si empiezas a trabajar <strong>6 meses o más después de jubilarte</strong>, la pensión sube un <strong>25 %</strong> de la que cobrabas (con jornadas del 55 % al 80 %) o un <strong>15 %</strong> (del 33 % al 55 %).</li>
<li>También vale para trabajar <strong>por cuenta propia</strong>, si no fuiste autónomo en los 3 años antes de jubilarte: cobras el <strong>25 %</strong> de la pensión.</li>
<li>Hay que comunicarlo a la Seguridad Social <strong>antes de empezar</strong> a trabajar.</li>
</ul>
<h2>📋 Cuánto cobras según la jornada</h2>
<p>Con una pensión de {e(EJ)} € al mes:</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Jornada que trabajas</th><th>Sin incremento</th><th>Con incremento (6 meses después)</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota-corta">Cálculo propio con el Real Decreto 416/2026. A la pensión se suma tu sueldo por el trabajo a tiempo parcial.</p>
<p>No es compatible con el complemento por retrasar la jubilación (el «complemento de demora»). Mira también la <a href="edad-jubilacion-2027">edad de jubilación 2027</a> y la <a href="pension-minima-maxima-2026">pensión mínima y máxima</a>.</p>
</article></div></section>

<script>
// Reglas del Real Decreto 416/2026 (las mismas que la tabla, escritas por gen-flexible.py)
const f2=n=>new Intl.NumberFormat('es-ES',{{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}}).format(n);
document.getElementById('tipo').onchange=function(){{const aj=this.value==='ajena';document.getElementById('jornadaGrupo').style.display=aj?'':'none';document.getElementById('mesesGrupo').style.display=aj?'':'none'}};
document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const p=+document.getElementById('pension').value, tipo=document.getElementById('tipo').value;
    if(!p){{document.getElementById('pension').focus();return}}
    let base, extra=0, txt;
    if(tipo==='propia'){{base=25;txt='Por cuenta propia cobras el <strong>25 %</strong> de la pensión, si no fuiste autónomo en los 3 años anteriores a jubilarte.'}}
    else{{
        const j=+document.getElementById('jornada').value;
        if(!(j>=33&&j<=80)){{document.getElementById('jornada').focus();mostrarError('La jornada tiene que estar entre el 33 % y el 80 %');return}}
        base=100-j;
        if(document.getElementById('meses').value==='si') extra=j>=55?25:15;
        txt='Trabajas el '+j+' % de la jornada, así que cobras el <strong>'+base+' %</strong> de la pensión'+(extra?', más un <strong>'+extra+' %</strong> por empezar 6 meses o más después de jubilarte':'')+'.';
    }}
    const pct=Math.min(100,base+extra), total=p*pct/100;
    document.getElementById('total').textContent=f2(total);
    document.getElementById('resultSub').textContent=pct+' % de tu pensión, más tu sueldo';
    document.getElementById('rAhora').textContent=f2(p);
    document.getElementById('rBase').textContent=f2(p*base/100);
    document.getElementById('rExtra').textContent='+'+f2(p*(pct-base)/100);
    document.getElementById('porque').innerHTML='<p>'+txt+'</p>';
    document.getElementById('result').classList.add('visible');
    document.getElementById('result').scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('reset').onclick=function(){{document.getElementById('calc').reset();document.getElementById('tipo').onchange.call(document.getElementById('tipo'));document.getElementById('result').classList.remove('visible');window.scrollTo({{top:0,behavior:'smooth'}})}};
</script>
'''

faqs = [
    ('¿Qué es la jubilación flexible?', 'Volver a trabajar a <strong>tiempo parcial</strong> (entre el 33 % y el 80 % de la jornada) cuando ya cobras la pensión: la pensión baja en proporción a la jornada y sigues cotizando.'),
    ('¿Cuánto cobro con la jubilación flexible?', f'La parte de la jornada que no trabajas, más un 15 % o un 25 % si empiezas 6 meses o más después de jubilarte. Con {e(EJ)} € de pensión y media jornada (50 %): {e(EJ * cobras(50) / 100)} € al mes, más tu sueldo.'),
    ('¿Qué cambió en la jubilación flexible en 2026?', 'El <strong>Real Decreto 416/2026</strong>, en vigor desde el 28 de agosto de 2026: jornada del 33 % al 80 %, incremento del 15 % o el 25 % y la posibilidad de trabajar por cuenta propia cobrando el 25 % de la pensión.'),
    ('¿Puedo ser autónomo y cobrar la pensión?', 'Sí, con la jubilación flexible por cuenta propia cobras el <strong>25 %</strong> de la pensión, si no fuiste autónomo en los 3 años anteriores a jubilarte. Existe también la jubilación activa, con otras condiciones.'),
]
fuente = '<a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-11474" target="_blank" rel="noopener">Real Decreto 416/2026, de 27 de mayo</a>, de jubilación flexible (en vigor desde el 28 de agosto de 2026).'
pagina('jubilacion-flexible', 'Jubilación flexible 2026: calcula tu pensión trabajando',
       'Desde el 28/08/2026 puedes trabajar entre el 33 % y el 80 % de la jornada y cobrar parte de la pensión, con un 15 % o 25 % extra. Calcula cuánto cobrarías.',
       'jubilación flexible, jubilación flexible 2026, trabajar y cobrar la pensión, real decreto 416/2026, compatibilizar pensión y trabajo',
       [('Jubilación', 'jubilacion'), ('Jubilación flexible', None)], cuerpo, faqs, fuente)

_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
if '/jubilacion-flexible<' not in _s:
    _s = _s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/jubilacion-flexible</loc><lastmod>2026-11-05</lastmod><priority>0.8</priority></url>\n</urlset>')
    open(_sm, 'w', encoding='utf-8').write(_s)
print('jubilacion-flexible')
