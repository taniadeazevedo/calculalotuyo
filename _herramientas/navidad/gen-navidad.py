# Páginas de Navidad: «Lotería de Navidad: cuánto se queda Hacienda» (con calculadora) y «Paga extra de Navidad 2026».
# Lotería: Ley 35/2006 del IRPF, disposición adicional 33.ª (DATOS.loteria en datos-2026.js).
# Paga extra: Estatuto de los Trabajadores art. 31 y la retención de IRPF de cada sueldo (sueldos.json).
# Uso: python3 _herramientas/navidad/gen-navidad.py
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, REVISADO, AD

REV = REVISADO.format(fecha='20 de octubre de 2026')
LEY = '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#datrigesimatercera" target="_blank" rel="noopener">Ley 35/2006 del IRPF, disposición adicional 33.ª</a>'

# ================================================================ 1) LOTERÍA
EXENTO, TIPO = 40000, 0.20
neto = lambda p: p - max(0, p - EXENTO) * TIPO                     # lo que te llega de un premio por décimo
# Premios del Sorteo Extraordinario de Navidad por décimo de 20 € (programa de Loterías y Apuestas del Estado)
PREMIOS = [('🥇 El Gordo (primer premio)', 400000), ('🥈 Segundo premio', 125000), ('🥉 Tercer premio', 50000),
           ('Cuarto premio', 20000), ('Quinto premio', 6000), ('Aproximación al Gordo', 2000), ('Pedrea', 100), ('Reintegro', 20)]
filas = ''.join(f'<tr><td>{n}</td><td>{e(p)} €</td><td>{e(max(0, p - EXENTO) * TIPO)} €</td><td><strong>{e(neto(p))} €</strong></td></tr>' for n, p in PREMIOS)
botones = ''.join(f'<option value="{p}"{" selected" if p == 400000 else ""}>{n.split(" (")[0]}: {e(p)} €</option>' for n, p in PREMIOS[:6]) + '<option value="otro">Otro importe</option>'

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🎄 Sorteo del 22 de diciembre</div><h1>Lotería de Navidad 2026<br><span class="highlight">¿cuánto se queda Hacienda?</span></h1><p>Si te toca el Gordo, de los 400.000 € de un décimo te llegan <strong>328.000 €</strong>. Los primeros 40.000 € de cada décimo no pagan nada; el resto paga un 20 %.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">🎟️</div>Tu premio</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="premio">¿Qué premio?</label><select class="form-select" id="premio">{botones}</select><span class="form-hint">Importes por décimo de 20 €</span></div>
                <div class="form-group" id="g-otro" hidden><label class="form-label" for="otro">Premio de un décimo (o apuesta)</label><input type="number" class="form-input" id="otro" placeholder="60000" min="0"><span class="form-hint">Sirve para cualquier sorteo de Loterías, ONCE o Cruz Roja</span></div>
                <div class="form-group"><label class="form-label" for="como">¿Cómo juegas?</label><select class="form-select" id="como"><option value="decimo" selected>Décimos enteros</option><option value="compartido">Un décimo compartido</option><option value="participacion">Una participación (papeleta)</option></select></div>
                <div class="form-group" id="g-decimos"><label class="form-label" for="decimos">¿Cuántos décimos premiados?</label><input type="number" class="form-input" id="decimos" value="1" min="1"></div>
                <div class="form-group" id="g-personas" hidden><label class="form-label" for="personas">¿Entre cuántas personas, a partes iguales?</label><input type="number" class="form-input" id="personas" value="2" min="2"></div>
                <div class="form-group" id="g-jugado" hidden><label class="form-label" for="jugado">¿Cuánto juegas de ese décimo?</label><input type="number" class="form-input" id="jugado" value="5" min="0.5" max="20" step="0.5"><span class="form-hint">Lo que pone la papeleta que juegas (no el donativo). El décimo cuesta 20 €</span></div>
            </div>
            <button type="submit" class="btn">Calcular lo que me llega</button>
            <p class="btn-text"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        <div class="result" id="result">
            <div class="result-hero"><p class="result-label">Te llega limpio</p><p class="result-value" id="total">—</p><p class="result-sub" id="resultSub"></p></div>
            <div class="reparto"><span class="r-neto" id="bNeto"></span><span class="r-irpf" id="bHac"></span></div>
            <div class="reparto-leyenda"><span><i class="r-neto"></i>Para ti</span><span><i class="r-irpf"></i>Hacienda (20 %)</span></div>
            <div class="fiscal-box"><div class="fiscal-title">🧮 Desglose</div><div id="fiscalContent"></div></div>
            <div class="aviso-ccaa" id="consejos"></div>
            <div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button><a href="#" class="btn-wa" id="wa" target="_blank">📱 WhatsApp</a></div>
        </div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🎄 Lo que te llega de cada premio</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Premio</th><th>Por décimo</th><th>Hacienda</th><th>Te llega</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota-corta">Décimo de 20 € del Sorteo Extraordinario de Navidad. Hacienda solo cobra en el Gordo, el segundo y el tercer premio: el resto no pasa de 40.000 €.</p>

<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Los primeros 40.000 € no pagan</strong><p>Cuenta por cada décimo: si tienes dos décimos del Gordo, cada uno tiene sus 40.000 € libres.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Lo que pasa de 40.000 € paga un 20 %</strong><p>El Gordo: (400.000 − 40.000) × 20 % = <strong>72.000 €</strong> para Hacienda. Te llegan 328.000 €.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Te lo quitan al cobrar</strong><p>El banco te paga el premio con el 20 % ya descontado. No tienes que hacer nada más: el premio <strong>no va en la declaración de la renta</strong>.</p></div></div>
</div>

<h2>👥 Décimos compartidos y participaciones</h2>
<ul>
<li><strong>Décimo compartido:</strong> los 40.000 € libres se reparten entre los que lo compartís. Si sois dos a medias y toca el Gordo, cada uno cobra 200.000 € y paga 36.000 €: os llegan <strong>164.000 € a cada uno</strong>.</li>
<li><strong>Participaciones</strong> (las papeletas de bares, peñas o asociaciones): cobras la parte del premio que te toca según lo que juegas, y libre de impuestos solo esa misma parte de los 40.000 €. Con 5 € de un décimo del Gordo cobras 100.000 €, pagas 18.000 € y te llegan <strong>82.000 €</strong>.</li>
<li>Si compartes un décimo, <strong>déjalo por escrito</strong> (una fotocopia firmada por todos con lo que juega cada uno) y cobradlo juntos en el banco. Si lo cobra una sola persona y luego reparte, Hacienda puede tratar ese reparto como una donación.</li>
</ul>

<h2>📌 Otros sorteos</h2>
<p>La regla es la misma para todos los sorteos de <strong>Loterías y Apuestas del Estado</strong> (El Niño, Euromillones, Primitiva, Quiniela…), las loterías de las comunidades autónomas, la <strong>ONCE</strong> y la <strong>Cruz Roja</strong>: 40.000 € libres por décimo o apuesta y un 20 % sobre el resto. Usa «Otro importe» en la calculadora.</p>
<p>¿Te toca y no sabes si eso cambia tu renta? No: estos premios no cuentan para la declaración. Mira si <a href="obligado-a-declarar-renta">tienes que hacer la renta</a> por tus otros ingresos.</p>
</article></div></section>

<script>
// =====================================================================
// LOTERÍA: CUÁNTO TE LLEGA. Las cifras están en datos-2026.js (DATOS.loteria).
// Espera a DOMContentLoaded porque site.js y datos-2026.js se cargan al final de la página.
// =====================================================================
document.addEventListener('DOMContentLoaded',()=>{{
const L=DATOS.loteria;
const g=id=>document.getElementById(id);
// Muestra los campos que tocan según lo elegido
function campos(){{
    g('g-otro').hidden=g('premio').value!=='otro';
    const c=g('como').value;
    g('g-decimos').hidden=c!=='decimo';
    g('g-personas').hidden=c!=='compartido';
    g('g-jugado').hidden=c!=='participacion';
}}
g('premio').addEventListener('change',campos); g('como').addEventListener('change',campos); campos();

g('calc').onsubmit=function(e){{
    e.preventDefault();
    const decimo=g('premio').value==='otro'?+g('otro').value:+g('premio').value;   // premio de un décimo entero
    if(!decimo){{mostrarError('Pon el importe del premio');return}}
    const c=g('como').value;
    // Parte del décimo que es tuya y cuántos décimos
    let parte=1, n=1, texto='';
    if(c==='decimo'){{n=Math.max(1,Math.round(+g('decimos').value||1));texto=n===1?'1 décimo':n+' décimos'}}
    if(c==='compartido'){{const p=Math.max(2,Math.round(+g('personas').value||2));parte=1/p;texto='tu parte de un décimo compartido entre '+p}}
    if(c==='participacion'){{const j=Math.min(20,Math.max(0.5,+g('jugado').value||0));parte=j/20;texto='una participación de '+fmtDec(j).replace(',00','')+' de un décimo'}}
    // Cálculo: los 40.000 € libres y el 20 % se reparten en la misma proporción que el premio
    const bruto=decimo*parte*n;
    const hacienda=Math.max(0,decimo-L.exento)*L.tipo/100*parte*n;
    const neto=bruto-hacienda;
    g('total').textContent=fmt(neto);
    g('resultSub').textContent='De un premio de '+fmt(bruto)+' ('+texto+')';
    g('bNeto').style.width=(bruto?neto/bruto*100:100)+'%'; g('bHac').style.width=(bruto?hacienda/bruto*100:0)+'%';
    const fila=(t,v,cl)=>'<div class="fiscal-row'+(cl?' highlight':'')+'"><span>'+t+'</span><span>'+v+'</span></div>';
    g('fiscalContent').innerHTML=fila('Premio que te corresponde',fmt(bruto))+
        fila('Libre de impuestos (40.000 € por décimo'+(parte<1?', tu parte':'')+')',fmt(Math.min(decimo,L.exento)*parte*n))+
        fila('Hacienda: 20 % del resto','− '+fmt(hacienda))+fila('Te llega',fmt(neto),true);
    g('consejos').innerHTML=hacienda?'💡 El banco te lo paga con el 20 % ya descontado y no va en la renta. '+(parte<1?'Para que cada uno pague solo su parte, cobradlo juntos y con lo que juega cada uno por escrito.':''):
        '🎉 Este premio <strong>no paga nada</strong> a Hacienda: no pasa de 40.000 € por décimo.';
    g('wa').href='https://wa.me/?text='+encodeURIComponent('🎄 Si me toca '+fmt(bruto)+' en la lotería, me llegan '+fmt(neto)+'\\nCalcúlalo: https://calculalotuyo.es/loteria-navidad-hacienda');
    g('result').classList.add('visible');
    g('result').scrollIntoView({{behavior:'smooth',block:'start'}});
}};
g('reset').onclick=()=>{{g('calc').reset();campos();g('result').classList.remove('visible');window.scrollTo({{top:0,behavior:'smooth'}})}};
}});
</script>
<script src="datos-2026.js?v=20261020b"></script>
'''
faqs = [
    ('¿Cuánto se queda Hacienda del Gordo de Navidad?', '<strong>72.000 € por décimo</strong>: el 20 % de lo que pasa de 40.000 €. De los 400.000 € te llegan <strong>328.000 €</strong>.'),
    ('¿Cuánto me queda del segundo y del tercer premio?', 'Del segundo (125.000 € por décimo) te llegan <strong>108.000 €</strong>, y del tercero (50.000 €), <strong>48.000 €</strong>. Los cuartos, quintos, la pedrea y el reintegro no pagan nada.'),
    ('¿Tengo que declarar el premio de la lotería en la renta?', 'No. El 20 % te lo quitan al cobrar y el premio no se incluye en la declaración de la renta.'),
    ('¿Los 40.000 € libres son por persona o por décimo?', 'Por décimo (o por apuesta). Si el décimo es compartido, los 40.000 € se reparten entre los que lo compartís.'),
    ('¿Cuánto me llega si juego 5 € en una participación y toca el Gordo?', 'Cobras 100.000 € (la cuarta parte del premio de un décimo), Hacienda se queda 18.000 € y te llegan <strong>82.000 €</strong>.'),
]
pagina('loteria-navidad-hacienda', 'Lotería de Navidad 2026: cuánto se queda Hacienda de tu premio',
    'Calcula cuánto te llega si te toca la Lotería de Navidad: del Gordo (400.000 € por décimo) te quedan 328.000 €. Décimos compartidos, participaciones y otros sorteos.',
    'lotería de navidad hacienda, cuánto se queda hacienda del gordo, premio lotería impuestos, gordo navidad neto, lotería navidad 2026 premios',
    [('Lotería de Navidad: cuánto se queda Hacienda', None)], cuerpo, faqs,
    f'{LEY}: premios exentos hasta 40.000 € por décimo y gravamen del 20 % sobre el resto. Importes de los premios: programa del Sorteo Extraordinario de Navidad de Loterías y Apuestas del Estado (décimo de 20 €).')

# ================================================================ 2) PAGA EXTRA DE NAVIDAD
D = json.load(open(os.path.join(AQUI, '..', 'sueldos', 'sueldos.json')))['datos']
SUELDOS = [17094, 18000, 20000, 22000, 25000, 28000, 30000, 35000, 40000, 45000, 50000, 60000]
paga = lambda b: b / 14                                             # una paga extra bruta (en 14 pagas, todas iguales)
neta = lambda b: paga(b) * (1 - D[str(b)]['base']['tipo'] / 100)    # solo le quitan el IRPF (la Seguridad Social va repartida en las mensualidades)
filas_p = ''.join(f'<tr><td>{e(b)} €{" (SMI)" if b == 17094 else ""}</td><td>{e(paga(b))} €</td><td>{str(D[str(b)]["base"]["tipo"]).replace(".", ",")} %</td><td><strong>{e(neta(b))} €</strong></td></tr>' for b in SUELDOS)
p30 = neta(30000)
ET = '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a31" target="_blank" rel="noopener">Estatuto de los Trabajadores, art. 31</a>'

cuerpo_p = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🎁 Diciembre de 2026</div><h1>Paga extra de Navidad 2026<br><span class="highlight">cuánto cobras y cuándo</span></h1><p>Con 30.000 € brutos al año en 14 pagas, tu paga de Navidad es de {e(paga(30000))} € brutos y te llegan unos <strong>{e(p30)} € netos</strong>. Busca tu sueldo en la tabla.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{e(paga(17094))} €</strong><span>paga extra con el salario mínimo</span></div><div><strong>{e(p30)} €</strong><span>netos con 30.000 € brutos</span></div><div><strong>Diciembre</strong><span>la fecha la fija tu convenio</span></div></div>
        <h2 class="puentes-titulo">🎁 Tu paga extra de Navidad según tu sueldo</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Sueldo bruto al año</th><th>Paga extra bruta</th><th>Retención IRPF</th><th>Paga extra neta</th></tr></thead><tbody>{filas_p}</tbody></table></div>
        <p class="nota-corta">Sueldo en 14 pagas, persona sin hijos y contrato indefinido, 2026. La paga extra solo lleva retención de IRPF: la Seguridad Social ya se descuenta, repartida, en las nóminas de cada mes.</p>
        <div class="result-actions"><a href="pagas-extra" class="btn">🧮 Calcular mi paga extra exacta</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📅 ¿Cuándo se cobra la paga de Navidad?</h2>
<p>La ley dice que hay <strong>dos pagas extra al año, una de ellas en Navidad</strong>. El día exacto lo fija tu convenio: lo normal es cobrarla en diciembre, antes de Navidad, o junto con la nómina de noviembre. Si no la has cobrado a final de año, reclámala.</p>
<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>La cuantía la fija tu convenio</strong><p>Si cobras en 14 pagas, cada paga extra suele ser igual que una mensualidad: tu sueldo anual entre 14.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Solo le quitan el IRPF</strong><p>Se aplica el mismo porcentaje de retención que en tus nóminas. Por eso la paga extra neta es algo mayor que tu nómina neta de un mes.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Si no has trabajado todo el año, cobras la parte proporcional</strong><p>Normalmente se genera de enero a diciembre (o de julio a diciembre, según el convenio). Si entraste en septiembre, cobras la parte de esos meses.</p></div></div>
</div>
<h2>❓ Casos frecuentes</h2>
<ul>
<li><strong>Cobro en 12 pagas:</strong> tus pagas extra van prorrateadas en cada nómina, así que en diciembre no cobras una paga aparte.</li>
<li><strong>Me voy o me despiden antes de Navidad:</strong> la parte generada de la paga extra va en el <a href="finiquito">finiquito</a>.</li>
<li><strong>Estoy en paro:</strong> el paro no tiene pagas extra; ya está calculado en tus mensualidades.</li>
</ul>
<p>Para ver tu nómina de cada mes, usa la <a href="sueldo-neto">calculadora de sueldo neto</a> o busca tu sueldo en la <a href="sueldo-bruto-a-neto-2026">tabla de bruto a neto</a>.</p>
</article></div></section>
'''
faqs_p = [
    ('¿Cuánto es la paga extra de Navidad?', f'Si cobras en 14 pagas, suele ser igual que una mensualidad: tu sueldo anual entre 14. Con 30.000 € brutos son {e(paga(30000))} € brutos y unos <strong>{e(p30)} € netos</strong>.'),
    ('¿Cuándo se cobra la paga extra de Navidad?', 'Lo fija tu convenio. Normalmente en diciembre, antes de Navidad, o junto con la nómina de noviembre.'),
    ('¿La paga extra tiene descuento de Seguridad Social?', 'No: solo lleva la retención de IRPF. La cotización de las pagas extra se reparte en las nóminas de todos los meses.'),
    ('¿Cuánto es la paga extra con el salario mínimo?', f'<strong>{e(paga(17094))} € brutos</strong> (el SMI de 2026 en 14 pagas). Con el salario mínimo la retención de IRPF es muy baja.'),
    ('¿Si cobro en 12 pagas tengo paga de Navidad?', 'No aparte: las pagas extra ya van repartidas en tus 12 nóminas.'),
]
pagina('paga-extra-navidad-2026', 'Paga extra de Navidad 2026: cuánto cobras y cuándo',
    f'Paga extra de Navidad 2026: con 30.000 € brutos son unos {e(p30)} € netos. Tabla para cada sueldo, cuándo se cobra y cómo se calcula.',
    'paga extra navidad 2026, cuánto es la paga extra de navidad, cuándo se cobra la paga extra, paga extra neta, paga extra diciembre',
    [('Pagas extra', 'pagas-extra'), ('Paga extra de Navidad 2026', None)], cuerpo_p, faqs_p,
    f'{ET} (dos gratificaciones extraordinarias al año, una en Navidad). Retención de IRPF de cada sueldo según el algoritmo de la Agencia Tributaria para 2026.')
print('creadas: loteria-navidad-hacienda, paga-extra-navidad-2026')
