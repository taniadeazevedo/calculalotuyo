# Genera la calculadora de jubilación (jubilacion.html). Las cifras vienen de datos-2026.js (DATOS.jubilacion).
# Uso: python3 _herramientas/jubilacion/gen-jubilacion.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO, AD

REV = REVISADO.format(fecha='19 de octubre de 2026')
LGSS = '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724" target="_blank">Ley General de la Seguridad Social</a>'
FUENTE = f'Arts. 205, 208, 209 y 210 y disposiciones transitorias 7.ª y 9.ª de la {LGSS}; pensión máxima de 2026: <a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-2548" target="_blank">Real Decreto-ley 3/2026</a>, art. 1.'

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🌅 Jubilación 2026</div><h1>Calculadora de jubilación<br><span class="highlight">¿cuándo te jubilas y cuánto cobrarás?</span></h1><p>Calcula tu edad de jubilación (65 o 67 años), el porcentaje de pensión que te corresponde por los años cotizados y una estimación de lo que cobrarás.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">📝</div>Tus datos</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="nacimiento">Fecha de nacimiento</label><input type="date" class="form-input" id="nacimiento" min="1955-01-01" max="2008-12-31" required></div>
                <div class="form-group"><label class="form-label" for="sueldo">Sueldo bruto al año</label><input type="number" class="form-input" id="sueldo" placeholder="30000" min="0" required><span class="form-hint">El de los últimos años, con pagas extra</span></div>
                <div class="form-group"><label class="form-label" for="anios">Años cotizados hasta hoy</label><input type="number" class="form-input" id="anios" placeholder="20" min="0" max="60" required><span class="form-hint">Lo ves en tu informe de vida laboral</span></div>
                <div class="form-group"><label class="form-label" for="meses">y meses</label><input type="number" class="form-input" id="meses" value="0" min="0" max="11"></div>
                <div class="form-group"><label class="form-label" for="sigo">¿Seguirás trabajando hasta jubilarte?</label><select class="form-select" id="sigo"><option value="si" selected>Sí, sin parar</option><option value="no">No, ya no cotizo</option></select></div>
            </div>
            <button type="submit" class="btn">Calcular mi jubilación</button>
            <p class="btn-text"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        <div class="result" id="result">
            <div class="result-hero"><p class="result-label">Te podrás jubilar</p><p class="result-value" id="total">—</p><p class="result-sub" id="resultSub"></p></div>
            <div class="cifras" id="cifras"></div>
            <h3 class="puentes-titulo">📊 Porcentaje de tu pensión</h3>
            <div class="reparto"><span class="r-neto" id="barra"></span></div>
            <p class="nota-corta" id="notaBarra"></p>
            <div class="fiscal-box"><div class="fiscal-title">🧮 Desglose</div><div id="fiscalContent"></div></div>
            <div class="aviso-ccaa" id="consejos"></div>
            <div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button><a href="#" class="btn-wa" id="wa" target="_blank">📱 WhatsApp</a></div>
        </div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📅 Edad de jubilación en 2026 y 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Año en que te jubilas</th><th>Con estos años cotizados…</th><th>…te jubilas a los</th></tr></thead><tbody>
<tr><td rowspan="2">2026</td><td>38 años y 3 meses o más</td><td><strong>65 años</strong></td></tr><tr><td>Menos de 38 años y 3 meses</td><td><strong>66 años y 10 meses</strong></td></tr>
<tr><td rowspan="2">2027 en adelante</td><td>38 años y 6 meses o más</td><td><strong>65 años</strong></td></tr><tr><td>Menos de 38 años y 6 meses</td><td><strong>67 años</strong></td></tr>
</tbody></table></div>
<h2>🧮 Cómo se calcula la pensión</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Mínimo de 15 años cotizados</strong><p>Y al menos 2 de ellos en los últimos 15 años. Con menos no hay pensión contributiva.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Porcentaje según los años cotizados</strong><p>Los primeros 15 años dan el 50 %. Cada mes de más suma: desde 2027, un 0,19 % los primeros 248 meses y un 0,18 % los 16 siguientes, hasta el <strong>100 % con 37 años cotizados</strong> (en 2026 basta con 36 años y medio).</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Base reguladora</strong><p>Es la media de lo que has cotizado en los últimos años, con la inflación actualizada. Desde 2026 el periodo se va alargando poco a poco: en 2026 se toman las 302 mejores bases de los últimos 304 meses, y así hasta llegar a 29 años descartando los 2 peores (disposición transitoria 40.ª).</p></div></div>
    <div class="calc-step"><span class="step-num">4</span><div><strong>Pensión</strong><p>Base reguladora × porcentaje, con un máximo de <strong>3.359,60 € al mes</strong> en 14 pagas (2026).</p></div></div>
</div>
<p>La calculadora estima la base reguladora a partir de tu sueldo actual, como si hubieras cobrado lo mismo todos estos años. Si tu sueldo ha subido mucho, tu pensión real será algo menor; para el dato exacto, pide un informe a la Seguridad Social.</p>
<h2>⏩ Jubilarte antes o después</h2>
<ul>
<li><strong>Anticipada voluntaria:</strong> hasta <strong>2 años antes</strong> de tu edad ordinaria, si tienes al menos <strong>35 años cotizados</strong>. La pensión se reduce según los meses que adelantes y los años cotizados.</li>
<li><strong>Demorada:</strong> por cada año completo que sigas trabajando después de tu edad ordinaria, tu pensión sube un <strong>4 %</strong> (o puedes cobrarlo de una vez, como cantidad a tanto alzado).</li>
</ul>
<p>Si te quedas sin trabajo antes de jubilarte, mira <a href="tabla-paro-2026">cuánto paro te corresponde</a>. Y si quieres saber cuánto te queda neto de tu sueldo actual, usa la <a href="sueldo-neto">calculadora de sueldo neto</a>.</p>
</article></div></section>

<script>
// =====================================================================
// CALCULADORA DE JUBILACIÓN. Las cifras están en datos-2026.js (DATOS.jubilacion).
// Espera a DOMContentLoaded porque site.js y datos-2026.js se cargan al final de la página.
// =====================================================================
document.addEventListener('DOMContentLoaded',()=>{{
const J=DATOS.jubilacion;
const g=id=>document.getElementById(id);
const masMeses=(f,m)=>{{const d=new Date(f);d.setMonth(d.getMonth()+m);return d}};          // suma meses a una fecha
const mesesEntre=(a,b)=>(b.getFullYear()-a.getFullYear())*12+b.getMonth()-a.getMonth();   // meses entre dos fechas
const fecha=f=>f.toLocaleDateString('es-ES',{{day:'numeric',month:'long',year:'numeric'}});  // «3 de marzo de 2040»
const aniosMeses=m=>Math.floor(m/12)+' años'+(m%12?' y '+(m%12)+(m%12===1?' mes':' meses'):'');  // 462 → «38 años y 6 meses»
// Regla de edad del año en que te jubilas: [año, meses cotizados para hacerlo a los 65, edad si no llegas]
const regla=anio=>J.edades.find(e=>e[0]===anio)||(anio<J.edades[0][0]?J.edades[0]:J.edades[J.edades.length-1]);

// Porcentaje de la pensión según los meses cotizados y el año en que te jubilas
function porcentaje(meses,anio){{
    if(meses<J.minimoMeses)return 0;                                   // menos de 15 años: sin pensión contributiva
    const [,[m1,t1],[m2,t2]]=J.escala.find(e=>anio<=e[0]);              // escala de ese año
    const extra=meses-J.minimoMeses;                                    // meses después de los 15 primeros años
    return Math.min(100,50+Math.min(extra,m1)*t1+Math.min(Math.max(extra-m1,0),m2)*t2);
}}

// Fecha de jubilación ordinaria: la edad depende del año en que te jubilas y de lo cotizado a los 65
function jubilacion(nac,cotEn){{
    const a65=masMeses(nac,780);                                         // el día que cumples 65 años (780 meses)
    for(let anio=a65.getFullYear();anio<=a65.getFullYear()+3;anio++){{
        const [,umbral,edadSinUmbral]=regla(anio);
        const edad=cotEn(a65)>=umbral?780:edadSinUmbral;                 // ¿llegas cotizado a los 65? Si no, la edad del cuadro
        const f=masMeses(nac,edad);
        if(f.getFullYear()<=anio)return {{f,edad}};                       // la fecha cae en el año de esa regla: es la buena
    }}
    const ultima=J.edades[J.edades.length-1][2];
    return {{f:masMeses(nac,ultima),edad:ultima}};
}}

g('calc').onsubmit=function(e){{
    e.preventDefault();
    const nac=new Date(g('nacimiento').value), sueldo=+g('sueldo').value;
    const cotHoy=(+g('anios').value)*12+(+g('meses').value||0);        // meses cotizados hasta hoy
    const sigo=g('sigo').value==='si';
    if(isNaN(nac)||!sueldo||!g('anios').value){{mostrarError('Rellena la fecha de nacimiento, el sueldo y los años cotizados');return}}
    const hoy=new Date();
    const cotEn=f=>cotHoy+(sigo?Math.max(0,mesesEntre(hoy,f)):0);      // lo que tendrás cotizado en una fecha
    const {{f,edad}}=jubilacion(nac,cotEn);
    const cot=cotEn(f), anio=f.getFullYear(), pct=porcentaje(cot,anio);
    const base=Math.min(sueldo/12,DATOS.cotizacion.baseMaximaMes)*12/14;   // base reguladora estimada (al mes, en 14 pagas)
    const pension=Math.min(base*pct/100,J.pensionMaxima);
    const yaPuede=f<=hoy;

    g('total').textContent=yaPuede?'Ya puedes':fecha(f);
    g('resultSub').textContent='Con '+aniosMeses(edad)+' de edad'+(yaPuede?' (ya los has cumplido)':'');
    g('cifras').innerHTML=
        '<div><strong>'+aniosMeses(cot).replace(' y ','<br>y ')+'</strong><span>cotizados al jubilarte</span></div>'+
        '<div><strong>'+pct.toLocaleString('es-ES',{{maximumFractionDigits:1}})+' %</strong><span>de la base reguladora</span></div>'+
        '<div><strong>'+(pct?fmt(pension):'—')+'</strong><span>'+(pct?'al mes (14 pagas), estimado':'sin pensión contributiva')+'</span></div>';
    g('barra').style.width=pct+'%';
    g('notaBarra').textContent=pct>=100?'Tienes el 100 %: cotizar más no sube el porcentaje (salvo si retrasas la jubilación).':
        pct?'Te falta '+aniosMeses(Math.max(0,(anio<=2026?438:444)-cot))+' cotizado para llegar al 100 %.':'Necesitas al menos 15 años cotizados para tener pensión contributiva.';
    g('fiscalContent').innerHTML=
        '<div class="fiscal-row"><span>Base reguladora estimada</span><span>'+fmt(base)+'/mes</span></div>'+
        '<div class="fiscal-row"><span>Porcentaje por años cotizados</span><span>'+pct.toLocaleString('es-ES',{{maximumFractionDigits:2}})+' %</span></div>'+
        (base*pct/100>J.pensionMaxima?'<div class="fiscal-row"><span>Tope de la pensión máxima (2026)</span><span>'+fmt(J.pensionMaxima)+'</span></div>':'')+
        '<div class="fiscal-row highlight"><span>Pensión estimada</span><span>'+(pct?fmt(pension)+'/mes':'—')+'</span></div>'+
        '<div class="fiscal-row"><span>Al año (14 pagas)</span><span>'+(pct?fmt(pension*14):'—')+'</span></div>';
    // Consejos: jubilación anticipada y demorada
    const ant=masMeses(nac,edad-J.anticipadaAnios*12), cotAnt=cotEn(ant);
    let c=[];
    if(cotAnt>=J.anticipadaCotizados*12&&!yaPuede)c.push('⏩ Podrías adelantarla hasta el <strong>'+fecha(ant)+'</strong> (jubilación anticipada voluntaria), con una reducción en la pensión.');
    if(pct)c.push('⏸️ Si sigues trabajando un año más después de esa fecha, tu pensión subiría un <strong>4 %</strong>: unos '+fmt(Math.min(base*(pct+J.demora)/100,J.pensionMaxima)-pension)+' más al mes.');
    c.push('ℹ️ Es una estimación con tu sueldo actual y las reglas de 2026. Para el dato exacto, pide tu informe en la sede de la Seguridad Social.');
    g('consejos').innerHTML=c.join('<br>');
    g('wa').href='https://wa.me/?text='+encodeURIComponent('🌅 Me podré jubilar '+(yaPuede?'ya':'el '+fecha(f))+' con '+aniosMeses(edad)+'\\nhttps://calculalotuyo.es/jubilacion');
    g('result').classList.add('visible');
}};
g('reset').onclick=()=>{{g('calc').reset();g('result').classList.remove('visible');window.scrollTo({{top:0,behavior:'smooth'}})}};
}});
</script>
<script src="datos-2026.js?v=20261020a"></script>
'''
faqs = [
    ('¿A qué edad me puedo jubilar en 2027?', 'A los <strong>67 años</strong>, o a los <strong>65</strong> si tienes al menos <strong>38 años y 6 meses cotizados</strong>. En 2026 es a los 66 años y 10 meses, o a los 65 con 38 años y 3 meses cotizados.'),
    ('¿Cuántos años hay que cotizar para cobrar el 100 % de la pensión?', 'Desde 2027, <strong>37 años</strong>. En 2026, 36 años y medio. Con 15 años cotizados se cobra el 50 %.'),
    ('¿Cuál es la pensión máxima en 2026?', '<strong>3.359,60 € al mes</strong> en 14 pagas (47.034,40 € al año) para las pensiones que empiezan en 2026.'),
    ('¿Cuántos años necesito para tener pensión?', 'Un mínimo de <strong>15 años cotizados</strong>, y al menos 2 de ellos en los últimos 15 años.'),
    ('¿Me puedo jubilar antes?', 'Sí, hasta <strong>2 años antes</strong> de tu edad ordinaria si tienes 35 años cotizados (jubilación anticipada voluntaria), aunque la pensión se reduce. Si te despiden por causas ajenas a tu voluntad hay otras opciones de jubilación anticipada.'),
]
nombre = pagina('jubilacion', 'Calculadora de jubilación 2026: cuándo te jubilas y cuánto cobrarás',
    'Calcula tu edad de jubilación (65 o 67 años), el porcentaje de pensión según tus años cotizados y una estimación de lo que cobrarás. Con las reglas y la pensión máxima de 2026.',
    'calculadora jubilación, edad de jubilación 2027, cuánto cobraré de pensión, calcular pensión jubilación, años cotizados pensión 100%',
    [('Jubilación', None)], cuerpo, faqs, FUENTE, 'Nómina')
print('creada:', nombre)
