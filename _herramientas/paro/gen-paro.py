# Genera las páginas SEO del paro con los datos de paro.json (que calcula calcular.js con datos-2026.js).
# Uso: node _herramientas/paro/calcular.js && python3 _herramientas/paro/gen-paro.py
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, pct, REVISADO, AD

R = json.load(open(f'{AQUI}/paro.json'))
S = {int(k) if float(k).is_integer() else float(k): v for k, v in R['sueldos'].items()}
SMI_MES, SMI_ANUAL, TOP, DUR = R['smiMes'], R['smiAnual'], R['topes'], R['duracion']
REV = REVISADO.format(fecha='19 de octubre de 2026')
FUENTE = 'Art. 270 de la <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724" target="_blank">Ley General de la Seguridad Social</a> (cuantía: 70 % los 180 primeros días y 60 % después; topes según el IPREM) y art. 269 (duración). IPREM de 2026: 600 € al mes.'
MIGA_PARO = [('Paro', 'paro')]
PAGINAS = [SMI_MES, 1300, 1400, 1500, 1600, 1700, 1800, 2000]   # sin 1.900: sale casi igual que 2.000 (los dos en el máximo)
slug = lambda s: f'paro-con-{s}-euros'
nombre_s = lambda s: f'{e(s)} €' + (' (SMI)' if s == SMI_MES else '')
anios = lambda dias: dias / 360
txt_anios = lambda d: (f'{e(anios(d), 1)} años' if anios(d) % 1 else f'{int(anios(d))} {"año" if anios(d) == 1 else "años"}')
CTA = '<div class="result-actions"><a href="paro" class="btn">📊 Calcular mi paro exacto</a></div>'
# Cuándo se llega al máximo: base ≥ tope/porcentaje. En 14 pagas, sueldo = base × 12/14
max70_14 = TOP[0]['max'] / 0.70 * 12 / 14
max60_14 = TOP[0]['max'] / 0.60 * 12 / 14
gen = []

def barras(filas, escala):
    return '<div class="barras">' + ''.join(f'<div class="barra-fila"><span class="barra-nombre barra-larga">{n}</span><span class="barra {c}" style="width:{v / escala * 100:.0f}%">{e(v)} €</span></div>' for n, v, c in filas) + '</div>'

# ================================================================ 1) UNA PÁGINA POR SUELDO
for s in PAGINAS:
    d = S[s]; c0 = d['catorce'][0]
    neto12 = d['netoMes14'] * 14 / 12                     # neto trabajando, repartido en 12 meses (para comparar con el paro)
    base14 = s * 14 / 12
    total8 = c0['m70'] * 6 + c0['m60'] * 2                # ejemplo: 2 años cotizados = 8 meses de paro
    filas_hijos = ''.join(f'<tr><td>{n}</td><td><strong>{e(d["catorce"][i]["m70"])} €</strong></td><td>{e(d["catorce"][i]["m60"])} €</td></tr>' for i, n in enumerate(['Sin hijos', '1 hijo', '2 o más hijos']))
    doce = ''
    if s * 12 >= SMI_ANUAL:
        c12 = d['doce'][0]
        doce = f'<p>Si cobras <strong>en 12 pagas</strong> (o con las pagas extra prorrateadas), tu base es de {e(s)} € y el paro queda en <strong>{e(c12["m70"])} €</strong> los 6 primeros meses y {e(c12["m60"])} € después.</p>'
    topado = c0['m70'] >= TOP[0]['max'] - 0.01
    i = PAGINAS.index(s)
    vecinos = [p for p in PAGINAS[max(0, i - 3):i + 4] if p != s]
    enl = '<div class="enlaces-sueldo">' + ''.join(f'<a href="{slug(p)}">{nombre_s(p)}</a>' for p in vecinos) + '<a href="tabla-paro-2026">Ver todos →</a></div>'
    cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro 2026</div><h1>Paro con {e(s)} € brutos al mes<br><span class="highlight">{e(c0["m70"])} € al mes</span></h1><p>Si cobrabas {e(s)} € brutos al mes en 14 pagas, te corresponden <strong>{e(c0["m70"])} € al mes</strong> los 6 primeros meses de paro y <strong>{e(c0["m60"])} €</strong> a partir del séptimo.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{e(c0["m70"])} €</strong><span>meses 1 a 6</span></div><div><strong>{e(c0["m60"])} €</strong><span>desde el mes 7</span></div><div><strong>{e(c0["m70"] / neto12 * 100)} %</strong><span>de lo que cobrabas en neto</span></div></div>
        <h2 class="puentes-titulo">📉 Trabajando y en el paro, al mes</h2>
        {barras([('Trabajando (neto)', neto12, 'b-trabajo'), ('Paro, meses 1 a 6', c0['m70'], ''), ('Paro, desde el mes 7', c0['m60'], 'b-60')], max(neto12, c0['m70']))}
        <p class="nota-corta">Sin hijos. El sueldo neto está repartido en 12 meses (incluye la parte de las pagas extra) para poder compararlo. El paro es en bruto: de él se descuenta tu cotización a la Seguridad Social (unos {e(c0["ss"])} € al mes) y, si corresponde, IRPF.</p>
        <h2 class="puentes-titulo">👨‍👩‍👧 Con hijos a tu cargo</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Situación</th><th>Meses 1 a 6</th><th>Desde el 7</th></tr></thead><tbody>{filas_hijos}</tbody></table></div>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Base reguladora:</strong><p>Con {e(s)} € en 14 pagas, tu base de cotización al mes es {e(s)} × 14 ÷ 12 = <strong>{e(base14, 2)} €</strong> (incluye la parte de las dos pagas extra).</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Primeros 6 meses (70 %):</strong><p>{e(base14, 2)} × 70 % = {e(min(base14, 5101.20) * 0.70, 2)} €{f" → se queda en el máximo de <strong>{e(TOP[0]['max'])} €</strong>" if min(base14, 5101.2) * 0.70 > TOP[0]['max'] else f" = <strong>{e(c0['m70'], 2)} €</strong>"}</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Desde el mes 7 (60 %):</strong><p>{e(base14, 2)} × 60 % = {e(min(base14, 5101.20) * 0.60, 2)} €{f" → se queda en el máximo de <strong>{e(TOP[0]['max'])} €</strong>" if min(base14, 5101.2) * 0.60 > TOP[0]['max'] else f" = <strong>{e(c0['m60'], 2)} €</strong>"}</p></div></div>
</div>
{doce}
{f'<p>Con este sueldo ya llegas al <a href="paro-maximo-minimo-2026">paro máximo</a> en los primeros meses: aunque cobraras más, el paro no subiría sin hijos a cargo.</p>' if topado else ''}
<h2>⏳ Cuánto tiempo lo cobrarías</h2>
<p>Depende de los días que hayas cotizado en los últimos 6 años: con 1 año cotizado, 4 meses; con 2 años, 8 meses; y con 6 años, el máximo de 2 años. Por ejemplo, con 2 años cotizados y este sueldo cobrarías unos <strong>{e(total8)} € en total</strong>. Lo tienes todo en <a href="cuanto-paro-me-corresponde">cuánto paro me corresponde</a>.</p>
<h2>💶 Otros sueldos</h2>
{enl}
<p>¿Cobras en neto y no sabes tu bruto? Míralo en la <a href="sueldo-bruto-a-neto-2026">tabla de sueldo bruto a neto</a>.</p>
</article></div></section>
'''
    faqs = [
        (f'¿Cuánto paro me queda si cobro {e(s)} € al mes?', f'Si son {e(s)} € brutos en 14 pagas y no tienes hijos, cobrarás <strong>{e(c0["m70"])} € al mes</strong> los 6 primeros meses y <strong>{e(c0["m60"])} €</strong> a partir del séptimo (cifras de 2026, en bruto).'),
        ('¿El paro se calcula sobre el sueldo bruto o el neto?', 'Sobre el <strong>bruto</strong>: en concreto, sobre la base de cotización de los últimos 180 días, que incluye la parte de las pagas extra pero no las horas extra.'),
        ('¿Cuánto tiempo puedo cobrar el paro?', 'Entre <strong>4 meses</strong> (con 1 año cotizado) y <strong>2 años</strong> (con 6 años cotizados), según los días que hayas trabajado en los últimos 6 años.'),
        ('¿Cambia el paro si tengo hijos?', f'Sube el máximo (de {e(TOP[0]["max"])} € a {e(TOP[1]["max"])} € con un hijo y {e(TOP[2]["max"])} € con dos o más) y el mínimo (de {e(TOP[0]["min"])} € a {e(TOP[1]["min"])} €). Si tu paro no llegaba al máximo, no cambia.'),
    ]
    gen.append(pagina(slug(s), f'Paro con {e(s)} € de sueldo: {e(c0["m70"])} € al mes (2026)', f'Si cobras {e(s)} € brutos al mes, tu paro en 2026 es de {e(c0["m70"])} € al mes los 6 primeros meses y {e(c0["m60"])} € después. Con hijos, en 12 o 14 pagas y cuánto dura.', f'paro con {s} euros, cuánto cobro de paro si gano {s}, paro {s} euros brutos, prestación desempleo {s}', MIGA_PARO + [('Tabla del paro', 'tabla-paro-2026'), (f'Paro con {e(s)} €', None)], cuerpo, faqs, FUENTE, 'Paro y finiquito'))

# ================================================================ 2) TABLA DEL PARO
filas = ''
for s in sorted(S):
    d = S[s]; c14, c12 = d['catorce'][0], d['doce'][0]
    nom = f'<a href="{slug(s)}">{nombre_s(s)}</a>' if s in PAGINAS else nombre_s(s)
    doce = f'<td>{e(c12["m70"])} €</td><td>{e(c12["m60"])} €</td>' if s * 12 >= SMI_ANUAL else '<td>—</td><td>—</td>'
    filas += f'<tr><td>{nom}</td><td><strong>{e(c14["m70"])} €</strong></td><td>{e(c14["m60"])} €</td>{doce}</tr>'
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro 2026</div><h1>Tabla del paro 2026<br><span class="highlight">cuánto cobras según tu sueldo</span></h1><p>El paro que te corresponde con cada sueldo, de {e(SMI_MES)} € (el salario mínimo) a 5.000 € brutos al mes.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>70 %</strong><span>de tu base, meses 1 a 6</span></div><div><strong>60 %</strong><span>desde el mes 7</span></div><div><strong>{e(TOP[0]["max"])} €</strong><span>máximo sin hijos</span></div></div>
        <h2 class="puentes-titulo">📋 Paro según tu sueldo bruto al mes</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th rowspan="2">Sueldo/mes</th><th colspan="2">En 14 pagas</th><th colspan="2">En 12 pagas</th></tr><tr><th>Meses 1-6</th><th>Desde el 7</th><th>Meses 1-6</th><th>Desde el 7</th></tr></thead><tbody>{filas}</tbody></table></div>
        <p class="nota-corta">Sin hijos a cargo, jornada completa, cifras en bruto. «—»: en 12 pagas ese sueldo no llega al salario mínimo.</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📖 Cómo leer la tabla</h2>
<p>El paro se calcula sobre tu <strong>base de cotización</strong> de los últimos 180 días: tu sueldo bruto mensual más la parte de las pagas extra. Por eso, con el mismo sueldo, cobras más paro si te pagan en 14 pagas que si las extra ya van incluidas en 12.</p>
<p>Los 6 primeros meses cobras el 70 % de esa base y después el 60 %, pero siempre entre un mínimo y un máximo. Sin hijos, a partir de unos {e(max70_14)} € brutos al mes en 14 pagas ya cobras el máximo los primeros meses, y desde unos {e(max60_14)} € también después. Mira los <a href="paro-maximo-minimo-2026">topes del paro de 2026</a> y <a href="cuanto-paro-me-corresponde">cuánto tiempo te corresponde</a>.</p>
<h2>🔎 Sueldos más buscados</h2>
<div class="enlaces-sueldo">{"".join(f'<a href="{slug(p)}">{nombre_s(p)}</a>' for p in PAGINAS)}</div>
</article></div></section>
'''
faqs = [
    ('¿Cuánto se cobra de paro con el salario mínimo?', f'Con el salario mínimo de 2026 ({e(SMI_MES)} € en 14 pagas) cobras <strong>{e(S[SMI_MES]["catorce"][0]["m70"])} € al mes</strong> los 6 primeros meses y {e(S[SMI_MES]["catorce"][0]["m60"])} € después.'),
    ('¿Cuánto es el paro máximo en 2026?', f'<strong>{e(TOP[0]["max"])} € al mes</strong> sin hijos, {e(TOP[1]["max"])} € con un hijo y {e(TOP[2]["max"])} € con dos o más.'),
    ('¿Por qué cobro menos paro a partir del séptimo mes?', 'Porque la ley fija el 70 % de la base los 180 primeros días y el <strong>60 %</strong> a partir del día 181.'),
]
gen.append(pagina('tabla-paro-2026', 'Tabla del paro 2026: cuánto cobras según tu sueldo', f'Tabla del paro 2026: cuánto cobras de prestación por desempleo con cada sueldo, de {e(SMI_MES)} a 5.000 € brutos al mes, en 12 y 14 pagas.', 'tabla paro 2026, cuánto cobro de paro, prestación por desempleo 2026, paro según sueldo', MIGA_PARO + [('Tabla del paro 2026', None)], cuerpo, faqs, FUENTE, 'Paro y finiquito'))

# ================================================================ 3) PARO MÁXIMO Y MÍNIMO
filas = ''.join(f'<tr><td>{n}</td><td><strong>{e(TOP[i]["max"])} €</strong></td><td>{e(TOP[i]["min"])} €</td></tr>' for i, n in enumerate(['Sin hijos', '1 hijo', '2 o más hijos']))
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro 2026</div><h1>Paro máximo y mínimo 2026<br><span class="highlight">de {e(TOP[0]["min"])} € a {e(TOP[2]["max"])} € al mes</span></h1><p>Lo máximo y lo mínimo que puedes cobrar de paro en 2026, según tengas hijos o no.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{e(TOP[0]["max"])} €</strong><span>máximo sin hijos</span></div><div><strong>{e(TOP[2]["max"])} €</strong><span>máximo con 2 o más hijos</span></div><div><strong>{e(TOP[0]["min"])} €</strong><span>mínimo sin hijos</span></div></div>
        <h2 class="puentes-titulo">📊 Topes del paro en 2026</h2>
        {barras([('Máx. 2+ hijos', TOP[2]['max'], ''), ('Máx. 1 hijo', TOP[1]['max'], ''), ('Máx. sin hijos', TOP[0]['max'], ''), ('Mín. con hijos', TOP[1]['min'], 'b-60'), ('Mín. sin hijos', TOP[0]['min'], 'b-60')], TOP[2]['max'])}
        <div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Situación</th><th>Máximo</th><th>Mínimo</th></tr></thead><tbody>{filas}</tbody></table></div>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>❔ De dónde salen estas cifras</h2>
<p>Los topes del paro se calculan con el <strong>IPREM</strong>, que en 2026 sigue en 600 € al mes. La ley lo aumenta en una sexta parte (600 × 7 ÷ 6 = {e(R["iprem"])} €) y aplica estos porcentajes:</p>
<ul><li><strong>Máximo:</strong> 175 % sin hijos ({e(TOP[0]["max"])} €), 200 % con un hijo ({e(TOP[1]["max"])} €) y 225 % con dos o más ({e(TOP[2]["max"])} €).</li><li><strong>Mínimo:</strong> 80 % sin hijos ({e(TOP[0]["min"])} €) y 107 % con hijos ({e(TOP[1]["min"])} €).</li></ul>
<h2>💶 Con qué sueldo se cobra el máximo</h2>
<p>Sin hijos, cobras el máximo los 6 primeros meses si ganabas unos <strong>{e(max70_14)} € brutos al mes</strong> o más (en 14 pagas), y también a partir del séptimo mes desde unos <strong>{e(max60_14)} €</strong>. Por encima de eso, aunque ganaras mucho más, el paro no sube. Míralo sueldo a sueldo en la <a href="tabla-paro-2026">tabla del paro 2026</a>.</p>
<p>Si trabajabas a tiempo parcial, los topes se reducen en proporción a tus horas.</p>
</article></div></section>
'''
faqs = [
    ('¿Cuál es el paro máximo en 2026?', f'<strong>{e(TOP[0]["max"])} € al mes</strong> sin hijos a cargo, {e(TOP[1]["max"])} € con un hijo y {e(TOP[2]["max"])} € con dos o más hijos.'),
    ('¿Cuál es el paro mínimo en 2026?', f'<strong>{e(TOP[0]["min"])} € al mes</strong> sin hijos y {e(TOP[1]["min"])} € con hijos a cargo, a jornada completa.'),
    ('¿Por qué no ha subido el paro máximo?', 'Porque depende del IPREM, que lleva varios años congelado en 600 € al mes. Si sube el IPREM, suben los topes.'),
]
gen.append(pagina('paro-maximo-minimo-2026', f'Paro máximo y mínimo 2026: de {e(TOP[0]["min"])} a {e(TOP[2]["max"])} € al mes', f'Paro máximo 2026: {e(TOP[0]["max"])} € sin hijos, {e(TOP[1]["max"])} € con un hijo y {e(TOP[2]["max"])} € con dos. Paro mínimo: {e(TOP[0]["min"])} € o {e(TOP[1]["min"])} € con hijos. Y desde qué sueldo se cobra.', 'paro máximo 2026, paro mínimo 2026, tope paro 2026, cuánto es lo máximo de paro', MIGA_PARO + [('Paro máximo y mínimo 2026', None)], cuerpo, faqs, FUENTE, 'Paro y finiquito'))

# ================================================================ 4) CUÁNTO PARO ME CORRESPONDE (DURACIÓN)
filas = ''.join(f'<tr><td>{"Desde " if j == len(DUR) - 1 else ""}{e(c)} días <small>({txt_anios(c)})</small></td><td><strong>{e(p / 30)} meses</strong></td></tr>' for j, (c, p) in enumerate(DUR))
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📊 Paro 2026</div><h1>¿Cuánto paro me corresponde?<br><span class="highlight">de 4 meses a 2 años</span></h1><p>Cuánto tiempo puedes cobrar el paro según los días que hayas trabajado en los últimos 6 años.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>1 año</strong><span>cotizado = 4 meses de paro</span></div><div><strong>2 años</strong><span>= 8 meses</span></div><div><strong>6 años</strong><span>= 2 años (el máximo)</span></div></div>
        <h2 class="puentes-titulo">⏳ Meses de paro según lo que has cotizado</h2>
        <div class="barras">{"".join(f'<div class="barra-fila"><span class="barra-nombre barra-larga">{txt_anios(c)}</span><span class="barra" style="width:{p / 720 * 100:.0f}%">{e(p / 30)} meses</span></div>' for c, p in DUR)}</div>
        <p class="nota-corta">Años cotizados en los últimos 6, contando 360 días por año. Por cada 180 días más cotizados, 2 meses más de paro.</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📋 Tabla de duración del paro</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Días cotizados</th><th>Paro</th></tr></thead><tbody>{filas}</tbody></table></div>
<h2>📖 Qué días cuentan</h2>
<ul><li>Cuentan los días cotizados por desempleo en los <strong>últimos 6 años</strong> antes de quedarte en paro.</li><li><strong>No cuentan</strong> los días que ya usaste para cobrar un paro anterior.</li><li>Necesitas como mínimo <strong>360 días</strong>. Si no llegas, puede que tengas derecho a un subsidio: consúltalo en el SEPE o en nuestra <a href="guia-paro">guía del paro</a>.</li></ul>
<h2>💶 ¿Y cuánto cobraré?</h2>
<p>La cantidad depende de tu sueldo, no del tiempo trabajado. Mira la <a href="tabla-paro-2026">tabla del paro 2026</a> o calcula tu caso en la <a href="paro">calculadora del paro</a>.</p>
</article></div></section>
'''
faqs = [
    ('Si he trabajado 1 año, ¿cuánto paro me corresponde?', 'Con 360 días cotizados te corresponden <strong>4 meses</strong> de paro (120 días).'),
    ('Si he trabajado 2 años, ¿cuánto paro tengo?', 'Con 720 días cotizados, <strong>8 meses</strong> de paro (240 días).'),
    ('¿Cuál es el máximo de paro que se puede cobrar?', '<strong>2 años</strong> (720 días), si has cotizado 6 años (2.160 días) o más en los últimos 6 años.'),
    ('¿Qué pasa si no he cotizado 360 días?', 'No tienes derecho al paro contributivo, pero puedes tener derecho a un <strong>subsidio por desempleo</strong> si cumples sus requisitos. Pregunta en el SEPE.'),
]
gen.append(pagina('cuanto-paro-me-corresponde', '¿Cuánto paro me corresponde? Tabla de duración 2026', 'Cuánto paro te corresponde según lo cotizado: con 1 año, 4 meses; con 2 años, 8 meses; con 6 años, el máximo de 2 años. Tabla completa y qué días cuentan.', 'cuánto paro me corresponde, duración del paro, si he trabajado 1 año cuánto paro me corresponde, días cotizados paro', MIGA_PARO + [('Cuánto paro me corresponde', None)], cuerpo, faqs, FUENTE, 'Paro y finiquito'))

json.dump(gen, open(f'{AQUI}/generadas.json', 'w'))
print(len(gen), 'páginas:', ', '.join(gen))
