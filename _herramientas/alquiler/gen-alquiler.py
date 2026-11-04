# Calculadora «¿Cuánto te pueden subir el alquiler?» (subida-alquiler.html), 05/11/2026.
# Las reglas, según la fecha en que toca actualizar la renta:
#   · Desde el 8/10/2026 hasta el 31/12/2027: como mucho un 2 %, si no pactáis otra cosa (RDL 29/2026, disposición final sexta).
#     Si la vivienda está en zona tensionada y la renta pasa del precio de referencia: nada.
#   · Antes (2026): lo que diga el contrato (IPC, IRAV o un %), con el IRAV como límite en los contratos firmados
#     desde el 26/05/2023 (LAU, disposición adicional undécima, añadida por la Ley 12/2023).
#   · Si el contrato no dice nada: no hay subida (art. 18 LAU).
# Se usa el último dato publicado al llegar la fecha: el de dos meses antes (el INE lo publica a mediados del mes siguiente).
# CADA MES: añadir el IRAV nuevo (y el IPC) a las listas de abajo y lanzar sh _herramientas/regenerar.sh
# Uso: python3 _herramientas/alquiler/gen-alquiler.py
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, AD, REVISADO, RAIZ

# IRAV: variación anual (%), INE, serie IRAV1 (descargada de la API del INE el 05/11/2026)
IRAV = {'2025-01': 2.19, '2025-02': 2.08, '2025-03': 1.98, '2025-04': 2.09, '2025-05': 1.99, '2025-06': 2.10, '2025-07': 2.15,
        '2025-08': 2.19, '2025-09': 2.22, '2025-10': 2.25, '2025-11': 2.29, '2025-12': 2.32,
        '2026-01': 2.14, '2026-02': 2.16, '2026-03': 2.47, '2026-04': 2.40, '2026-05': 2.48, '2026-06': 2.44, '2026-07': 2.49,
        '2026-08': 2.47, '2026-09': 2.54}
# IPC general: variación anual (%), INE (octubre de 2026: dato adelantado)
IPC = {'2025-10': 3.1, '2025-11': 3.0, '2025-12': 2.9, '2026-01': 2.3, '2026-02': 2.3, '2026-03': 3.4, '2026-04': 3.2, '2026-05': 3.2,
       '2026-06': 3.2, '2026-07': 3.6, '2026-08': 4.3, '2026-09': 4.9, '2026-10': 4.9}
PUBLICADO_IRAV = '14 de octubre de 2026'          # fecha en que el INE publicó el último IRAV
SIGUIENTE_IRAV = 'mediados de noviembre de 2026'  # cuándo sale el siguiente
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
nombre_mes = lambda k: f'{MESES[int(k[5:]) - 1]} de {k[:4]}'               # «2026-09» → «septiembre de 2026»
pc = lambda x: f'{x:.2f}'.replace('.', ',') + ' %'
ULTIMO = max(IRAV)                                                           # «2026-09»
U = IRAV[ULTIMO]

# Ejemplo para los textos: 900 € al mes
EJ = 900
filas_irav = ''.join(f'<tr><td>{nombre_mes(k).capitalize()}</td><td><strong>{pc(v)}</strong></td><td>+{e(EJ * v / 100, 2)} €</td></tr>' for k, v in sorted(IRAV.items(), reverse=True))

# Meses que se pueden elegir: de enero de 2026 a diciembre de 2027
opciones = ''.join(f'<option value="{a}-{m:02d}"{" selected" if (a, m) == (2026, 11) else ""}>{MESES[m - 1].capitalize()} de {a}</option>' for a in (2026, 2027) for m in range(1, 13))

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🏠 Alquiler 2026-2027</div><h1>¿Cuánto te pueden subir el alquiler?<br><span class="highlight">Calculadora con el IRAV, el IPC y el tope del 2 %</span></h1><p>Pon tu renta y el mes en que se cumple el año de contrato: te decimos la subida máxima que permite la ley.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">🏠</div>Datos de tu alquiler</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="renta">Renta que pagas al mes (€)</label><input type="number" class="form-input" id="renta" placeholder="900" min="1" step="0.01" required></div>
                <div class="form-group"><label class="form-label" for="mes">¿Cuándo se cumple el año de contrato?</label><select class="form-select" id="mes">{opciones}</select><span class="form-hint">El mes en que toca actualizar la renta</span></div>
                <div class="form-group"><label class="form-label" for="clausula">¿Qué dice tu contrato sobre la subida?</label><select class="form-select" id="clausula"><option value="ipc">Que se actualiza con el IPC</option><option value="irav">Que se actualiza con el IRAV (índice de referencia)</option><option value="fijo">Una subida fija (un %)</option><option value="nada">No dice nada</option></select></div>
                <div class="form-group" id="fijoGrupo" style="display:none;"><label class="form-label" for="fijo">Subida pactada (%)</label><input type="number" class="form-input" id="fijo" placeholder="3" step="0.1" min="0"></div>
                <div class="form-group"><label class="form-label" for="firma">¿Cuándo firmaste el contrato?</label><select class="form-select" id="firma"><option value="nuevo">Desde el 26 de mayo de 2023</option><option value="viejo">Antes del 26 de mayo de 2023</option></select></div>
                <div class="form-group"><label class="form-label" for="tensionada">¿Zona tensionada con renta por encima del precio de referencia?</label><select class="form-select" id="tensionada"><option value="no">No, o no lo sé</option><option value="si">Sí</option></select><span class="form-hint">Solo en los municipios declarados tensionados</span></div>
            </div>
            <button type="submit" class="btn">Calcular la subida</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>

        <div class="result" id="result">
            <div class="result-hero"><p class="result-label">Tu nueva renta como mucho</p><p class="result-value" id="total">0 €</p><p class="result-sub" id="resultSub"></p></div>
            <div class="result-breakdown">
                <div class="result-row"><span class="result-row-label">🏠 Renta actual</span><span class="result-row-value" id="rActual">0 €</span></div>
                <div class="result-row bruto"><span class="result-row-label">📈 Subida al mes</span><span class="result-row-value" id="rMes">0 €</span></div>
                <div class="result-row exento"><span class="result-row-label">📅 Subida en un año</span><span class="result-row-value" id="rAnio">0 €</span></div>
            </div>
            <div class="result-grid" id="details"></div>
            <div class="fiscal-box"><div class="fiscal-title">⚖️ Por qué</div><div id="porque"></div></div>
            <div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button><a href="#" class="btn-wa" id="wa" target="_blank" rel="noopener">📱 WhatsApp</a></div>
        </div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📌 Las reglas de la subida del alquiler</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Si toca actualizar…</th><th>Te pueden subir como mucho</th></tr></thead><tbody>
<tr><td>Desde el 8 de octubre de 2026 hasta el 31 de diciembre de 2027</td><td><strong>Un 2 %</strong>, salvo que pactéis otra cosa. Nada si estás en zona tensionada y pagas más que el precio de referencia.</td></tr>
<tr><td>En 2025 y 2026 (hasta el 7 de octubre)</td><td>Lo que diga tu contrato (IPC, IRAV o un %), con el <strong>IRAV</strong> como límite si lo firmaste desde el 26 de mayo de 2023.</td></tr>
<tr><td>Si el contrato no dice nada</td><td><strong>Nada</strong>: sin cláusula de actualización, la renta no sube.</td></tr>
</tbody></table></div>
<p>El tope del 2 % lo puso el <strong>Real Decreto-ley 29/2026</strong> (BOE del 7 de octubre de 2026). Está en vigor, pero el Congreso tiene que convalidarlo; si no lo hiciera, volvería a valer el IRAV como límite. Actualizaremos la calculadora en cuanto se vote.</p>
<h2>📊 El IRAV mes a mes</h2>
<p>El <strong>IRAV</strong> (Índice de Referencia para la Actualización de Arrendamientos de Vivienda) lo publica el INE cada mes desde 2025. El último es el de <strong>{nombre_mes(ULTIMO)}: {pc(U)}</strong> (publicado el {PUBLICADO_IRAV}); el siguiente sale a {SIGUIENTE_IRAV}. Con un alquiler de {EJ} € al mes:</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Mes</th><th>IRAV</th><th>Subida con {EJ} € al mes</th></tr></thead><tbody>{filas_irav}</tbody></table></div>
<p class="nota-corta">Fuente: INE, serie IRAV (variación anual). Se aplica el último dato publicado en la fecha en que toca actualizar.</p>
<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Mira tu contrato:</strong><p>Si no dice cómo se actualiza la renta, no te la pueden subir. Si dice «IPC», «IRAV» o un porcentaje, ese es el punto de partida.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Aplica el límite de la ley:</strong><p>Desde el 8/10/2026, el 2 % (si no pactáis otra cosa). Antes, el IRAV en los contratos firmados desde el 26/05/2023.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Multiplica:</strong><p>Con {EJ} € y un 2 %: {EJ} × 1,02 = <strong>{e(EJ * 1.02, 2)} €</strong> al mes, {e(EJ * 0.02, 2)} € más.</p></div></div>
</div>
<p>El casero tiene que avisarte por escrito, y la subida solo se aplica desde que se cumple el año de contrato. Si te la cobra de más, puedes reclamar la diferencia. Para ver cómo va la inflación, mira el <a href="ipc-actual">IPC actual</a>.</p>
</article></div></section>

<script>
// Datos del INE (los escribe gen-alquiler.py) y reglas de la calculadora
const IRAV={json.dumps(IRAV)}, IPC={json.dumps(IPC)};
const MESES={json.dumps(MESES, ensure_ascii=False)};
const f2=n=>new Intl.NumberFormat('es-ES',{{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}}).format(n);   // 912,34 €
const p2=n=>n.toLocaleString('es-ES',{{minimumFractionDigits:2,maximumFractionDigits:2}})+' %';
const nom=k=>MESES[+k.slice(5)-1]+' de '+k.slice(0,4);
// Último dato publicado al llegar la fecha: el de dos meses antes (o el último que haya, si aún no ha salido)
function dato(serie,mes){{
    let [a,m]=mes.split('-').map(Number); m-=2; if(m<1){{m+=12;a--}}
    let k=a+'-'+String(m).padStart(2,'0');
    const claves=Object.keys(serie).sort();
    if(!(k in serie)) k=claves.filter(c=>c<=k).pop()||claves[claves.length-1];
    return [k,serie[k]];
}}
document.getElementById('clausula').onchange=function(){{document.getElementById('fijoGrupo').style.display=this.value==='fijo'?'block':'none'}};
document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const renta=+document.getElementById('renta').value, mes=document.getElementById('mes').value;
    const clausula=document.getElementById('clausula').value, firma=document.getElementById('firma').value, tens=document.getElementById('tensionada').value==='si';
    if(!renta){{document.getElementById('renta').focus();return}}
    const [kIrav,irav]=dato(IRAV,mes), [kIpc,ipc]=dato(IPC,mes);
    const tope2=mes>='2026-10' && mes<='2027-12';            // RDL 29/2026: del 8/10/2026 al 31/12/2027
    let base, txtBase, limite, txtLim, sube;
    if(clausula==='ipc'){{base=ipc;txtBase='IPC de '+nom(kIpc)+': '+p2(ipc)}}
    else if(clausula==='irav'){{base=irav;txtBase='IRAV de '+nom(kIrav)+': '+p2(irav)}}
    else if(clausula==='fijo'){{base=+document.getElementById('fijo').value||0;txtBase='Subida pactada: '+p2(base)}}
    else {{base=0;txtBase='Tu contrato no dice cómo se actualiza'}}
    if(clausula==='nada'){{limite=0;txtLim='Sin cláusula de actualización, la renta no sube (art. 18 de la Ley de Arrendamientos Urbanos).'}}
    else if(tope2 && tens){{limite=0;txtLim='En zona tensionada, si tu renta pasa del precio de referencia, no puede subir hasta el 31/12/2027 (Real Decreto-ley 29/2026).'}}
    else if(tope2){{limite=2;txtLim='Del 8/10/2026 al 31/12/2027, como mucho un <strong>2 %</strong> si no pactáis otra cosa (Real Decreto-ley 29/2026, pendiente de convalidar).'}}
    else if(firma==='nuevo'){{limite=irav;txtLim='Contratos firmados desde el 26/05/2023: el límite es el <strong>IRAV</strong> ('+nom(kIrav)+': '+p2(irav)+').'}}
    else {{limite=Infinity;txtLim='Contrato anterior al 26/05/2023: se aplica lo que diga el contrato.'}}
    if(mes==='2026-10') txtLim+=' Ojo: si el año se cumplió del 1 al 7 de octubre de 2026, el tope del 2 % no se aplica.';
    sube=Math.max(0,Math.min(base,limite));
    const nueva=renta*(1+sube/100), mas=nueva-renta;
    document.getElementById('total').textContent=f2(nueva);
    document.getElementById('resultSub').textContent=sube>0?'+'+p2(sube)+' desde '+nom(mes):'Sin subida';
    document.getElementById('rActual').textContent=f2(renta);
    document.getElementById('rMes').textContent='+'+f2(mas);
    document.getElementById('rAnio').textContent='+'+f2(mas*12);
    document.getElementById('details').innerHTML=`<div class="result-item"><p class="result-item-label">Según tu contrato</p><p class="result-item-value">${{txtBase}}</p></div><div class="result-item"><p class="result-item-label">Límite de la ley</p><p class="result-item-value">${{limite===Infinity?'Sin límite':p2(limite)}}</p></div><div class="result-item"><p class="result-item-label">Se aplica</p><p class="result-item-value">${{p2(sube)}}</p></div>`;
    document.getElementById('porque').innerHTML='<p>'+txtLim+'</p>';
    document.getElementById('wa').href='https://wa.me/?text='+encodeURIComponent(`🏠 Subida del alquiler: de ${{f2(renta)}} a ${{f2(nueva)}} al mes como mucho (+${{p2(sube)}}).\n\nhttps://calculalotuyo.es/subida-alquiler`);
    document.getElementById('result').classList.add('visible');
    document.getElementById('result').scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('reset').onclick=function(){{document.getElementById('calc').reset();document.getElementById('fijoGrupo').style.display='none';document.getElementById('result').classList.remove('visible');window.scrollTo({{top:0,behavior:'smooth'}})}};
</script>
'''

faqs = [
    ('¿Cuánto me pueden subir el alquiler en 2026?', f'Si el año de contrato se cumple <strong>desde el 8 de octubre de 2026</strong>, como mucho un <strong>2 %</strong>, salvo que pactéis otra cosa (Real Decreto-ley 29/2026). Antes de esa fecha, lo que diga tu contrato, con el IRAV como límite en los firmados desde el 26/05/2023.'),
    ('¿Cuál es el último IRAV?', f'El de <strong>{nombre_mes(ULTIMO)}: {pc(U)}</strong>, publicado por el INE el {PUBLICADO_IRAV}. El siguiente sale a {SIGUIENTE_IRAV}.'),
    ('¿Me pueden subir el alquiler con el IPC?', f'Solo si lo dice tu contrato, y con límites: hasta el 31/12/2027, como mucho un 2 % (si no pactáis otra cosa). El IPC de octubre de 2026 es del 4,9 %, así que se aplicaría el 2 %.'),
    ('¿Qué pasa si mi contrato no dice nada de la subida?', 'Que <strong>no te pueden subir la renta</strong> durante el contrato: la actualización solo se aplica si está pactada (art. 18 de la Ley de Arrendamientos Urbanos).'),
    ('¿Qué es el IRAV?', 'El <strong>Índice de Referencia para la Actualización de Arrendamientos de Vivienda</strong>. Lo calcula el INE desde 2025 para que las subidas del alquiler no sigan al IPC cuando la inflación se dispara.'),
]
fuente = ('<a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20823" target="_blank" rel="noopener">Real Decreto-ley 29/2026</a> (disposición final sexta: límite del 2 % hasta el 31/12/2027); '
          '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003" target="_blank" rel="noopener">Ley 29/1994 de Arrendamientos Urbanos</a> (art. 18 y disposición adicional undécima); '
          '<a href="https://www.ine.es/uc/oC7D0Ncd" target="_blank" rel="noopener">INE: Índice de referencia de arrendamientos de vivienda</a>.')
pagina('subida-alquiler', 'Calculadora subida alquiler 2026: IPC, IRAV y tope del 2 %',
       f'¿Cuánto te pueden subir el alquiler? Desde el 8/10/2026, como mucho un 2 %. Calcula tu nueva renta con el IPC o el IRAV ({pc(U)} en {MESES[int(ULTIMO[5:]) - 1]}).',
       'subida alquiler 2026, calculadora ipc alquiler, irav, actualizacion alquiler 2026, subida ipc alquiler 2026, cuanto me pueden subir el alquiler',
       [('Subida del alquiler', None)], cuerpo, faqs, fuente)

# Sitemap: si falta, se añade (sitemap.py pone luego la fecha buena)
_sm = os.path.join(RAIZ, 'sitemap.xml'); _s = open(_sm, encoding='utf-8').read()
if '/subida-alquiler<' not in _s:
    _s = _s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/subida-alquiler</loc><lastmod>2026-11-05</lastmod><priority>0.9</priority></url>\n</urlset>')
    open(_sm, 'w', encoding='utf-8').write(_s)
print(f'subida-alquiler · último IRAV {ULTIMO}: {pc(U)}')
