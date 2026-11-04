# Familia «Contratar y costes» (05/11/2026): tres calculadoras nuevas que comparten público con la web.
#   · coste-trabajador.html  — cuánto le cuesta un trabajador a la empresa
#   · sueldo-por-horas.html  — de sueldo a precio por hora (bruto y neto) y al revés
#   · calculadora-iva.html   — sumar o quitar el IVA (21 %, 10 %, 4 %)
# Las dos primeras usan datos-2026.js e irpf-2026.js (el mismo motor que sueldo-neto e irpf) y sueldos.json para las tablas.
# Uso: python3 _herramientas/calculadoras/gen-contratar.py
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO, e, AD, RAIZ

datos = open(os.path.join(RAIZ, 'datos-2026.js'), encoding='utf-8').read()
EMPRESA = float(re.search(r'empresa:([\d.]+)', datos).group(1))               # 0,3065
BASE_MAX = float(re.search(r'baseMaximaMes:([\d.]+)', datos).group(1))        # 5.101,20 € al mes
V_DATOS = re.search(r'datos-2026\.js\?v=([\w]+)', open(os.path.join(RAIZ, 'sueldo-neto.html'), encoding='utf-8').read()).group(1)
SCRIPTS = f'<script src="datos-2026.js?v={V_DATOS}"></script>\n<script src="irpf-2026.js"></script>\n'   # el motor de nóminas, antes del script de la página
S = {int(k): v['base'] for k, v in json.load(open(os.path.join(AQUI, '..', 'sueldos', 'sueldos.json')))['datos'].items()}
REV = REVISADO.format(fecha='5 de noviembre de 2026')
AT_OFICINA = 0.01                                                            # accidentes de trabajo, oficinas: 0,65 % IT + 0,35 % IMS
coste = lambda b, at=AT_OFICINA: b + min(b, BASE_MAX * 12) * (EMPRESA + at)
pcs = lambda x, d=2: f'{x * 100:.{d}f}'.rstrip('0').rstrip(',.').replace('.', ',') + ' %'
F2 = "const f2=n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(n);\nconst f0=n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0,useGrouping:'always'}).format(n);\n"
def sitemap(slug):
    sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    if f'/{slug}<' not in s:
        s = s.replace('</urlset>', f'    <url><loc>https://calculalotuyo.es/{slug}</loc><lastmod>2026-11-05</lastmod><priority>0.9</priority></url>\n</urlset>')
        open(sm, 'w', encoding='utf-8').write(s)
def resultado(etiqueta, filas):
    """Caja de resultado con el estilo de las demás calculadoras."""
    return (f'<div class="result" id="result"><div class="result-hero"><p class="result-label">{etiqueta}</p><p class="result-value" id="total">0 €</p><p class="result-sub" id="resultSub"></p></div>'
            '<div class="result-breakdown">' + ''.join(f'<div class="result-row {c}"><span class="result-row-label">{t}</span><span class="result-row-value" id="{i}">0 €</span></div>' for t, i, c in filas) + '</div>'
            '<div class="result-grid" id="details"></div><div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button></div></div>')
RESET = "document.getElementById('reset').onclick=function(){document.getElementById('calc').reset();document.getElementById('result').classList.remove('visible');window.scrollTo({top:0,behavior:'smooth'})};\n"
MOSTRAR = "document.getElementById('result').classList.add('visible');document.getElementById('result').scrollIntoView({behavior:'smooth'});"

# ================================================================ 1. COSTE DE UN TRABAJADOR PARA LA EMPRESA
filas = ''.join(f'<tr><td>{e(b)} €</td><td><strong>{e(coste(b))} €</strong></td><td>{e(coste(b) / 12)} €</td><td>{e(coste(b) - b)} €</td><td>{e(S[b]["neto"] / 12)} €</td></tr>' for b in (18000, 20000, 25000, 30000, 35000, 40000, 50000) if b in S)
c30 = coste(30000)
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">💼 Empresa 2026</div><h1>¿Cuánto cuesta contratar a un trabajador?<br><span class="highlight">Calculadora del coste para la empresa en 2026</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Un trabajador cuesta a la empresa su sueldo bruto más <strong>alrededor de un 31-32 %</strong> de Seguridad Social. Con <strong>30.000 € brutos al año, unos {e(c30)} €</strong> ({e(c30 / 12)} € al mes), y él cobra unos {e(S[30000]["neto"] / 12)} € netos al mes.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">💼</div>Datos del puesto</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="bruto">Sueldo bruto al año (€)</label><input type="number" class="form-input" id="bruto" placeholder="30000" min="1" step="100" required><span class="form-hint">Con las pagas extra incluidas</span></div>
                <div class="form-group"><label class="form-label" for="contrato">Tipo de contrato</label><select class="form-select" id="contrato"><option value="indefinido">Indefinido</option><option value="temporal">Temporal</option></select></div>
                <div class="form-group"><label class="form-label" for="at">Actividad (accidentes de trabajo)</label><select class="form-select" id="at"><option value="1">Oficina (1 %)</option><option value="1.5">Comercio y servicios (aprox. 1,5 %)</option><option value="3.5">Industria y transporte (aprox. 3,5 %)</option><option value="6.7">Construcción (6,7 %)</option></select><span class="form-hint">Depende de la actividad de la empresa</span></div>
                <div class="form-group"><label class="form-label" for="horas">Horas a la semana (opcional)</label><input type="number" class="form-input" id="horas" placeholder="40" min="1" max="60"><span class="form-hint">Para ver el coste por hora</span></div>
            </div>
            <button type="submit" class="btn">Calcular el coste</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        {resultado('Coste total al año para la empresa', [('💶 Sueldo bruto', 'rBruto', ''), ('🏛️ Seguridad Social de la empresa', 'rSS', 'bruto'), ('💵 Lo que cobra el trabajador (neto)', 'rNeto', 'exento')])}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Qué paga la empresa además del sueldo</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Concepto</th><th>Tipo en 2026</th></tr></thead><tbody>
<tr><td>Contingencias comunes</td><td>23,60 %</td></tr>
<tr><td>Desempleo</td><td>5,50 % (6,70 % con contrato temporal)</td></tr>
<tr><td>Formación profesional</td><td>0,60 %</td></tr>
<tr><td>FOGASA</td><td>0,20 %</td></tr>
<tr><td>Mecanismo de Equidad Intergeneracional</td><td>0,75 %</td></tr>
<tr><td>Accidentes de trabajo y enfermedades profesionales</td><td>Según la actividad: 1 % en oficinas, 6,70 % en construcción</td></tr>
<tr><td><strong>Total</strong></td><td><strong>{pcs(EMPRESA)} + accidentes de trabajo</strong></td></tr>
</tbody></table></div>
<p>Se paga sobre el sueldo bruto mensual con las pagas extra repartidas, hasta la <strong>base máxima de {e(BASE_MAX, 2)} € al mes</strong>. Por encima, solo se paga la cuota de solidaridad, más pequeña.</p>
<h2>📋 Coste de un trabajador según el sueldo</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Sueldo bruto al año</th><th>Coste para la empresa</th><th>Coste al mes</th><th>Seguridad Social empresa</th><th>Neto del trabajador al mes</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota-corta">Contrato indefinido, trabajo de oficina (1 % de accidentes de trabajo), neto en 12 pagas sin hijos. Mira cómo se reparte cada euro en nuestro <a href="informe-sueldo-coste-empresa-2026">informe del coste de un trabajador</a>.</p>
</article></div></section>

{SCRIPTS}<script>
// Coste para la empresa: bruto + cotización de la empresa (tipos de datos-2026.js) + accidentes de trabajo; neto con el motor de irpf-2026.js
{F2}document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const b=+document.getElementById('bruto').value, contrato=document.getElementById('contrato').value, at=+document.getElementById('at').value/100, h=+document.getElementById('horas').value;
    if(!b){{document.getElementById('bruto').focus();return}}
    const c=DATOS.cotizacion, mes=b/12, base=Math.min(mes,c.baseMaximaMes);
    let tipo=c.empresa+at+(contrato==='temporal'?0.012:0);                 // temporal: desempleo 6,70 % en vez de 5,50 %
    let ssMes=base*tipo, desde=c.baseMaximaMes;
    for(const [hasta,t] of c.solidaridad){{ if(mes<=desde)break; ssMes+=(Math.min(mes,hasta)-desde)*t*5; desde=hasta; }}   // solidaridad: la empresa paga 5 de cada 6 partes
    const ss=ssMes*12, total=b+ss, r=calcularRetencion({{bruto:b,contrato:contrato,hijos:0,situacion:3}});
    document.getElementById('total').textContent=f0(total);
    document.getElementById('resultSub').textContent=f0(total/12)+' al mes · el sueldo más un '+(ss/b*100).toLocaleString('es-ES',{{maximumFractionDigits:1}})+' %';
    document.getElementById('rBruto').textContent=f0(b);
    document.getElementById('rSS').textContent='+'+f0(ss);
    document.getElementById('rNeto').textContent=f0(r.neto)+' ('+f0(r.neto/12)+' al mes)';
    document.getElementById('details').innerHTML=`<div class="result-item"><p class="result-item-label">De cada 100 € que cuesta</p><p class="result-item-value">${{Math.round(r.neto/total*100)}} € llegan al trabajador</p></div><div class="result-item"><p class="result-item-label">Seguridad Social total</p><p class="result-item-value">${{f0(ss+r.ss)}} al año</p></div>`+(h?`<div class="result-item"><p class="result-item-label">Coste por hora</p><p class="result-item-value">${{f2(total/(h*52))}}</p></div>`:'');
    {MOSTRAR}
}};
{RESET}</script>
'''
faqs = [
    ('¿Cuánto cuesta un trabajador a la empresa en 2026?', f'Su sueldo bruto más alrededor de un <strong>31-32 %</strong> de Seguridad Social (más en construcción). Con 30.000 € brutos, unos <strong>{e(c30)} € al año</strong>.'),
    ('¿Cuánto paga la empresa de Seguridad Social por un trabajador?', f'Un <strong>{pcs(EMPRESA)}</strong> del sueldo bruto (hasta la base máxima) más el tipo de accidentes de trabajo de su actividad, que va del 1 % en oficinas al 6,70 % en construcción.'),
    ('¿Cuánto cuesta contratar a alguien por el salario mínimo?', f'Con el SMI de 2026 (17.094 € al año), unos <strong>{e(coste(17094))} € al año</strong> para la empresa, {e(coste(17094) / 12)} € al mes.'),
    ('¿Cuesta más un contrato temporal?', 'Sí: la cotización por desempleo de la empresa es del <strong>6,70 %</strong> en vez del 5,50 %, y en contratos de menos de 30 días se paga además una cotización adicional al darlos de baja.'),
]
fuente = '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724" target="_blank" rel="noopener">Ley General de la Seguridad Social</a> y orden de cotización de 2026 (tipos y bases); tarifa de accidentes de trabajo de la disposición adicional 4.ª de la Ley 42/2006.'
pagina('coste-trabajador', 'Coste de un trabajador para la empresa 2026: calculadora',
       f'¿Cuánto cuesta contratar a un trabajador? El sueldo más un 31-32 % de Seguridad Social: con 30.000 € brutos, unos {e(c30)} € al año. Calcula el coste exacto.',
       'coste trabajador empresa, cuanto cuesta contratar a un trabajador, calculadora coste empresa, coste empresa trabajador 2026, seguridad social empresa',
       [('Coste de un trabajador', None)], cuerpo, faqs, fuente)
sitemap('coste-trabajador')

# ================================================================ 2. SUELDO POR HORAS
HORAS = 40
filas = ''.join(f'<tr><td>{e(b)} €</td><td><strong>{e(b / (HORAS * 52), 2)} €</strong></td><td>{e(S[b]["neto"] / (HORAS * 52), 2)} €</td><td>{e(b / (30 * 52), 2)} €</td></tr>' for b in (17094, 18000, 20000, 22000, 25000, 28000, 30000, 35000, 40000, 50000) if b in S)
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">⏰ Sueldo 2026</div><h1>Calculadora de sueldo por horas<br><span class="highlight">cuánto cobras por hora, en bruto y en neto</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Divide tu sueldo bruto anual entre las horas que trabajas al año (horas a la semana × 52). Con <strong>30.000 € brutos y 40 horas, cobras {e(30000 / (HORAS * 52), 2)} € brutos por hora</strong> (unos {e(S[30000]["neto"] / (HORAS * 52), 2)} € netos).</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">⏰</div>Tu sueldo y tu jornada</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="importe">Importe (€)</label><input type="number" class="form-input" id="importe" placeholder="30000" min="0.01" step="0.01" required></div>
                <div class="form-group"><label class="form-label" for="tipo">Ese importe es…</label><select class="form-select" id="tipo"><option value="anual">Bruto al año</option><option value="mes14">Bruto al mes (14 pagas)</option><option value="mes12">Bruto al mes (12 pagas)</option><option value="hora">Bruto por hora</option></select></div>
                <div class="form-group"><label class="form-label" for="horas">Horas a la semana</label><input type="number" class="form-input" id="horas" value="40" min="1" max="60" step="0.5" required></div>
                <div class="form-group"><label class="form-label" for="contrato">Tipo de contrato</label><select class="form-select" id="contrato"><option value="indefinido">Indefinido</option><option value="temporal">Temporal</option></select></div>
            </div>
            <button type="submit" class="btn">Calcular</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        {resultado('Bruto por hora', [('💵 Neto por hora', 'rNetoHora', 'exento'), ('📅 Bruto al año', 'rAnual', ''), ('🏦 Neto al mes (12 pagas)', 'rNetoMes', 'bruto')])}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Cómo se calcula el sueldo por hora</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Horas al año:</strong><p>Horas a la semana × 52. Con 40 horas: <strong>2.080 horas</strong>. Las vacaciones y los festivos también se cobran, así que cuentan.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Bruto por hora:</strong><p>Sueldo bruto anual ÷ horas al año. Con 30.000 €: 30.000 ÷ 2.080 = <strong>{e(30000 / 2080, 2)} €</strong>.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Neto por hora:</strong><p>Lo mismo con el sueldo neto (tras IRPF y Seguridad Social): unos <strong>{e(S[30000]["neto"] / 2080, 2)} €</strong>.</p></div></div>
</div>
<h2>📋 Sueldo por hora según el bruto anual</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Bruto al año</th><th>Bruto por hora (40 h)</th><th>Neto por hora (40 h)</th><th>Bruto por hora (30 h)</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota-corta">Neto: contrato indefinido, sin hijos. 17.094 € es el salario mínimo de 2026. Las horas extra se pagan aparte: calcúlalas en la <a href="horas-extra">calculadora de horas extra</a>.</p>
</article></div></section>

{SCRIPTS}<script>
// Sueldo por horas: horas al año = horas a la semana × 52; neto con el motor de irpf-2026.js
{F2}document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const x=+document.getElementById('importe').value, tipo=document.getElementById('tipo').value, h=+document.getElementById('horas').value, contrato=document.getElementById('contrato').value;
    if(!x||!h){{document.getElementById('importe').focus();return}}
    const horasAnio=h*52;
    const anual=tipo==='anual'?x:tipo==='mes14'?x*14:tipo==='mes12'?x*12:x*horasAnio;
    const r=calcularRetencion({{bruto:anual,contrato:contrato,hijos:0,situacion:3}});
    document.getElementById('total').textContent=f2(anual/horasAnio);
    document.getElementById('resultSub').textContent=horasAnio.toLocaleString('es-ES')+' horas al año ('+h.toLocaleString('es-ES')+' a la semana)';
    document.getElementById('rNetoHora').textContent=f2(r.neto/horasAnio);
    document.getElementById('rAnual').textContent=f0(anual);
    document.getElementById('rNetoMes').textContent=f0(r.neto/12);
    document.getElementById('details').innerHTML=`<div class="result-item"><p class="result-item-label">Retención de IRPF</p><p class="result-item-value">${{r.tipo.toLocaleString('es-ES')}} %</p></div><div class="result-item"><p class="result-item-label">Bruto al mes (14 pagas)</p><p class="result-item-value">${{f0(anual/14)}}</p></div>`;
    {MOSTRAR}
}};
{RESET}</script>
'''
faqs = [
    ('¿Cómo se calcula el sueldo por hora?', f'Sueldo bruto anual ÷ (horas a la semana × 52). Con 30.000 € y 40 horas: <strong>{e(30000 / 2080, 2)} € brutos por hora</strong>.'),
    ('¿Cuánto es el salario mínimo por hora en 2026?', f'Con 40 horas a la semana, <strong>{e(17094 / 2080, 2)} € brutos por hora</strong> (17.094 € al año ÷ 2.080 horas). Las empleadas del hogar por horas tienen su propio precio por hora, más alto porque incluye pagas y vacaciones.'),
    ('¿Cuánto cobro por hora con 1.500 € al mes?', f'Con 1.500 € brutos en 14 pagas (21.000 € al año) y 40 horas, unos <strong>{e(21000 / 2080, 2)} € brutos por hora</strong>.'),
]
fuente = 'Cálculo propio. Neto con el algoritmo de retenciones de la Agencia Tributaria y las cotizaciones de 2026 (las mismas que la <a href="sueldo-neto">calculadora de sueldo neto</a>).'
pagina('sueldo-por-horas', 'Calculadora de sueldo por horas 2026: bruto y neto por hora',
       f'¿Cuánto cobras por hora? Con 30.000 € brutos y 40 horas, {e(30000 / 2080, 2)} € brutos y unos {e(S[30000]["neto"] / 2080, 2)} € netos por hora. Calcula el tuyo y pasa de hora a sueldo.',
       'sueldo por horas, calculadora sueldo por horas, cuanto cobro por hora, precio hora sueldo, salario por hora 2026, smi por hora',
       [('Sueldo por horas', None)], cuerpo, faqs, fuente)
sitemap('sueldo-por-horas')

# ================================================================ 3. CALCULADORA DE IVA
TIPOS_IVA = [(21, 'General: la mayoría de productos y servicios'), (10, 'Reducido: hostelería, transporte de viajeros, vivienda nueva…'), (4, 'Superreducido: pan, leche, huevos, fruta, libros, medicamentos…')]
filas = ''.join(f'<tr><td>{e(x)} €</td><td>{e(x * 1.21, 2)} €</td><td>{e(x * 1.10, 2)} €</td><td>{e(x * 1.04, 2)} €</td></tr>' for x in (10, 50, 100, 500, 1000))
filas_q = ''.join(f'<tr><td>{e(x)} €</td><td>{e(x / 1.21, 2)} €</td><td>{e(x - x / 1.21, 2)} €</td></tr>' for x in (10, 50, 100, 500, 1000))
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧾 Impuestos 2026</div><h1>Calculadora de IVA<br><span class="highlight">suma o quita el IVA del 21 %, 10 % o 4 %</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Para <strong>sumar el IVA</strong>, multiplica por 1,21 (100 € → 121 €). Para <strong>quitarlo</strong> de un precio con IVA, divide entre 1,21 (121 € → 100 €). No restes el 21 %: 121 − 21 % da 95,59 €, que está mal.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">🧾</div>Importe y tipo de IVA</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="importe">Importe (€)</label><input type="number" class="form-input" id="importe" placeholder="100" min="0.01" step="0.01" required></div>
                <div class="form-group"><label class="form-label" for="modo">¿Qué quieres hacer?</label><select class="form-select" id="modo"><option value="sumar">Sumar el IVA (el importe es sin IVA)</option><option value="quitar">Quitar el IVA (el importe ya lo lleva)</option></select></div>
                <div class="form-group"><label class="form-label" for="tipo">Tipo de IVA</label><select class="form-select" id="tipo"><option value="21">21 % (general)</option><option value="10">10 % (reducido)</option><option value="4">4 % (superreducido)</option></select></div>
            </div>
            <button type="submit" class="btn">Calcular</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        {resultado('Precio con IVA', [('📄 Base (sin IVA)', 'rBase', ''), ('🏛️ IVA', 'rIva', 'bruto')])}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📌 Tipos de IVA en España</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-texto"><thead><tr><th>Tipo</th><th>Para qué</th></tr></thead><tbody>{''.join(f'<tr><td><strong>{t} %</strong></td><td>{d}</td></tr>' for t, d in TIPOS_IVA)}</tbody></table></div>
<h2>➕ Sumar el IVA</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Sin IVA</th><th>Con 21 %</th><th>Con 10 %</th><th>Con 4 %</th></tr></thead><tbody>{filas}</tbody></table></div>
<h2>➖ Quitar el IVA del 21 %</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Con IVA</th><th>Sin IVA (base)</th><th>IVA incluido</th></tr></thead><tbody>{filas_q}</tbody></table></div>
<p>¿Eres autónomo? En tus facturas, además del IVA, puede ir la retención de IRPF: hazlas con la <a href="facturas">calculadora de facturas</a>.</p>
</article></div></section>

<script>
// IVA: sumar = importe × (1 + tipo); quitar = importe ÷ (1 + tipo)
{F2}document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const x=+document.getElementById('importe').value, modo=document.getElementById('modo').value, t=+document.getElementById('tipo').value/100;
    if(!x){{document.getElementById('importe').focus();return}}
    const base=modo==='sumar'?x:x/(1+t), iva=base*t, total=base+iva;
    document.querySelector('#result .result-label').textContent=modo==='sumar'?'Precio con IVA':'Precio sin IVA';
    document.getElementById('total').textContent=f2(modo==='sumar'?total:base);
    document.getElementById('resultSub').textContent=modo==='sumar'?f2(base)+' + '+(t*100)+' % de IVA':f2(total)+' con el '+(t*100)+' % de IVA incluido';
    document.getElementById('rBase').textContent=f2(base);
    document.getElementById('rIva').textContent=f2(iva);
    document.getElementById('details').innerHTML='';
    {MOSTRAR}
}};
{RESET}</script>
'''
faqs = [
    ('¿Cómo se quita el IVA de un precio?', 'Divide el precio entre <strong>1,21</strong> (o 1,10 o 1,04 según el tipo). Con 121 €: 121 ÷ 1,21 = <strong>100 €</strong> sin IVA y 21 € de IVA.'),
    ('¿Cómo se suma el IVA?', 'Multiplica el precio sin IVA por <strong>1,21</strong> (o 1,10 o 1,04). Con 100 €: 100 × 1,21 = <strong>121 €</strong>.'),
    ('¿Por qué no se resta el 21 % para quitar el IVA?', 'Porque el 21 % se calculó sobre el precio sin IVA, no sobre el precio final. 121 € − 21 % = 95,59 €, pero la base real es 100 €.'),
    ('¿Qué tipos de IVA hay en España?', 'El <strong>21 %</strong> general, el <strong>10 %</strong> reducido y el <strong>4 %</strong> superreducido. Canarias tiene el IGIC y Ceuta y Melilla el IPSI, en lugar del IVA.'),
]
fuente = '<a href="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740" target="_blank" rel="noopener">Ley 37/1992 del IVA</a>, arts. 90 y 91 (tipos impositivos).'
pagina('calculadora-iva', 'Calculadora de IVA: sumar y quitar el IVA (21 %, 10 %, 4 %)',
       'Suma o quita el IVA de un precio en un segundo: 21 %, 10 % o 4 %. Para quitarlo, divide entre 1,21 (no restes el 21 %). Con tablas y ejemplos.',
       'calculadora iva, quitar iva, sumar iva, calcular iva, iva 21, precio sin iva, iva incluido',
       [('Calculadora de IVA', None)], cuerpo, faqs, fuente)
sitemap('calculadora-iva')
print(f'coste-trabajador (30.000 € → {e(c30)} €) · sueldo-por-horas · calculadora-iva')
