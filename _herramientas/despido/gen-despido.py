# Genera las páginas «Indemnización por despido con N años» y la tabla general (datos de despido.json,
# que calcula calcular.js con el motor despido.js de la web).
# Uso: node _herramientas/despido/calcular.js && python3 _herramientas/despido/gen-despido.py
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, REVISADO, AD

R = json.load(open(f'{AQUI}/despido.json'))
D = {int(k): v for k, v in R['datos'].items()}
SM = R['sueldosMes']
EJ = 2000                                               # sueldo de ejemplo (brutos al mes en 14 pagas)
REV = REVISADO.format(fecha='19 de octubre de 2026')
FUENTE = 'Arts. 49.1.c, 53.1.b y 56 del <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430" target="_blank">Estatuto de los Trabajadores</a> (12, 20 y 33 días por año) y su disposición transitoria 11.ª (45 días por año hasta el 11 de febrero de 2012). Mismo cálculo que nuestra calculadora de despido improcedente.'
PAGINAS = []   # 24/10/2026: «despido con X años» unidas en tabla-indemnizacion-despido (ver consolidar.py)
slug = lambda a: f'indemnizacion-despido-{a}-anos'
anos = lambda a: f'{a} {"año" if a == 1 else "años"}'
dias_txt = lambda d: e(d, 0 if float(d).is_integer() else 2)
MESES_PARO = lambda a: min(a, 6) * 4                     # 360 días cotizados → 4 meses; 6 años o más → 24 (el máximo)
CTA = '<div class="result-actions"><a href="despido-improcedente" class="btn">⚖️ Calcular mi indemnización exacta</a></div>'
MIGA = [('Despido improcedente', 'despido-improcedente')]
gen = []

def barras(filas, escala):
    return '<div class="barras">' + ''.join(f'<div class="barra-fila"><span class="barra-nombre barra-larga">{n}</span><span class="barra {c}" style="width:{v / escala * 100:.0f}%">{e(v)} €</span></div>' for n, v, c in filas) + '</div>'

# ================================================================ UNA PÁGINA POR ANTIGÜEDAD
for a in PAGINAS:
    x = D[a]['sueldos']; ej = x[str(EJ)]
    d_imp, d_obj, d_tem = ej['impDias'], min(20 * a, 365), 12 * a   # objetivo: máximo 12 mensualidades = un año de salario (365 días)
    filas = ''.join(f'<tr><td>{e(sm)} €</td><td><strong>{e(x[str(sm)]["imp"])} €</strong></td><td>{e(x[str(sm)]["obj"])} €</td></tr>' for sm in SM)
    i = PAGINAS.index(a)
    vecinos = [p for p in PAGINAS[max(0, i - 3):i + 4] if p != a]
    enl = '<div class="enlaces-sueldo">' + ''.join(f'<a href="{slug(p)}">{anos(p)}</a>' for p in vecinos) + '<a href="tabla-indemnizacion-despido">Ver tabla →</a></div>'
    if ej['pre']:
        pre = f'''<h2>📅 Si empezaste antes de 2012</h2>
<p>Con {anos(a)} de antigüedad empezaste a trabajar antes del <strong>12 de febrero de 2012</strong>, cuando cambió la ley. Por eso el despido improcedente se calcula en dos tramos:</p>
<ul><li><strong>Hasta el 11/02/2012:</strong> 45 días por año ({ej["mesesPre"]} meses) = {e(ej["tramoPre"])} € con un sueldo de {e(EJ)} €.</li><li><strong>Desde el 12/02/2012:</strong> 33 días por año ({ej["mesesPost"]} meses) = {e(ej["tramoPost"])} €.</li></ul>
<p>{"En total pasaría de 720 días de salario, que es el máximo, así que se queda en <strong>720 días</strong> (24 mensualidades)." if ej["tope"] == "720 días" else f"En total, <strong>{dias_txt(d_imp)} días de salario</strong>."} El despido objetivo no cambia: siempre son 20 días por año{", con un máximo de 12 mensualidades" if a * 20 > 365 else ""}.</p>'''
        cuenta_imp = f'{dias_txt(d_imp)} días (tramos de 45 y 33 días)'
    else:
        pre = ''
        cuenta_imp = f'33 × {a} = {dias_txt(d_imp)} días'
    cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">⚖️ Despido 2026</div><h1>Despido con {anos(a)} de antigüedad<br><span class="highlight">{dias_txt(d_imp)} días de salario</span></h1><p>Si te despiden después de {anos(a)} en la empresa, te corresponden <strong>{dias_txt(d_imp)} días de salario</strong> si el despido es improcedente y <strong>{dias_txt(d_obj)}</strong> si es objetivo.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{dias_txt(d_imp)} días</strong><span>improcedente</span></div><div><strong>{dias_txt(d_obj)} días</strong><span>objetivo o ERE</span></div>{f"<div><strong>{dias_txt(d_tem)} días</strong><span>fin de contrato temporal</span></div>" if a <= 2 else f"<div><strong>{MESES_PARO(a)} meses</strong><span>de paro</span></div>"}</div>
        <h2 class="puentes-titulo">💶 Con un sueldo de {e(EJ)} € brutos al mes</h2>
        {barras([('Improcedente', ej['imp'], ''), ('Objetivo o ERE', ej['obj'], 'b-60')] + ([('Fin de temporal', ej['temporal'], 'b-trabajo')] if a <= 2 else []), ej['imp'])}   
        <p class="nota-corta">En 14 pagas ({e(ej["anual"])} € al año, {e(ej["diario"], 2)} € de salario diario). Despido el 19 de octubre de 2026.</p>
        <h2 class="puentes-titulo">📋 Según tu sueldo</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Sueldo/mes</th><th>Improcedente</th><th>Objetivo</th></tr></thead><tbody>{filas}</tbody></table></div>
        <p class="nota-corta">Sueldo bruto al mes en 14 pagas. Indemnización legal mínima: tu convenio o tu contrato pueden mejorarla.</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Salario diario:</strong><p>Sueldo bruto anual con pagas extra ÷ 365. Con {e(EJ)} € al mes en 14 pagas: {e(ej["anual"])} ÷ 365 = <strong>{e(ej["diario"], 2)} €</strong>.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Días que te corresponden:</strong><p>Improcedente: {cuenta_imp}. Objetivo: 20 × {a}{" = " + str(20 * a) + ", pero el máximo son 12 mensualidades:" if a * 20 > 365 else " ="} {dias_txt(d_obj)} días.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Indemnización:</strong><p>Improcedente: {e(ej["diario"], 2)} × {dias_txt(d_imp)} = <strong>{e(ej["imp"])} €</strong>. Objetivo: <strong>{e(ej["obj"])} €</strong>.</p></div></div>
</div>
{pre}
<h2>❔ Qué tipo de despido es el tuyo</h2>
<ul><li><strong>Improcedente (33 días por año):</strong> cuando el despido no está justificado o no se hizo bien, porque lo reconoce la empresa o lo dice un juez.</li><li><strong>Objetivo o ERE (20 días por año):</strong> por causas económicas, técnicas, organizativas o de producción, o por ineptitud del trabajador.</li><li><strong>Disciplinario procedente:</strong> sin indemnización. Si no está justificado, pasa a ser improcedente.</li><li><strong>Fin de contrato temporal (12 días por año):</strong> cuando se acaba un contrato temporal.</li></ul>
<p>Además de la indemnización, te tienen que pagar el <a href="finiquito">finiquito</a> (sueldo del mes, vacaciones pendientes y parte de las pagas extra). La indemnización legal no paga IRPF (hasta 180.000 €). Y con {anos(a)} cotizados {"te corresponden" if a < 6 else "te corresponde el máximo de"} <strong>{MESES_PARO(a)} meses de paro</strong>: mira <a href="tabla-paro-2026">cuánto cobrarías</a>.</p>
<h2>📅 Otras antigüedades</h2>
{enl}
</article></div></section>
'''
    faqs = [
        (f'¿Cuánto me corresponde de despido con {anos(a)} de antigüedad?', f'Si es improcedente, <strong>{dias_txt(d_imp)} días de salario</strong>; si es objetivo, {dias_txt(d_obj)} días. Con un sueldo de {e(EJ)} € brutos al mes en 14 pagas, son {e(ej["imp"])} € y {e(ej["obj"])} €.'),
        (f'¿Cuánto es la indemnización con {anos(a)} y 1.500 € de sueldo?', f'Con 1.500 € brutos al mes en 14 pagas: <strong>{e(x["1500"]["imp"])} €</strong> si el despido es improcedente y {e(x["1500"]["obj"])} € si es objetivo.'),
        ('¿La indemnización por despido paga IRPF?', 'No, la indemnización legal obligatoria está exenta hasta <strong>180.000 €</strong>. Si la empresa paga más de lo que marca la ley, el exceso sí tributa.'),
        (f'¿Tengo derecho a paro con {anos(a)} trabajados?', f'Sí, si has cotizado al menos 360 días. Con {anos(a)} cotizados te {"corresponden" if a < 6 else "corresponde el máximo:"} <strong>{MESES_PARO(a)} meses</strong> de paro.'),
    ]
    gen.append(pagina(slug(a), f'Indemnización por despido con {anos(a)} de antigüedad (2026)', f'Despido con {anos(a)} de antigüedad: {dias_txt(d_imp)} días de salario si es improcedente y {dias_txt(d_obj)} si es objetivo. Con 2.000 € al mes, {e(ej["imp"])} €. Tabla por sueldo y cálculo paso a paso.', f'indemnización despido {a} años, despido improcedente {a} años antigüedad, despido objetivo {a} años, cuánto me corresponde de despido {a} años', MIGA + [('Tabla de indemnizaciones', 'tabla-indemnizacion-despido'), (f'Despido con {anos(a)}', None)], cuerpo, faqs, FUENTE, 'Despido'))

# ================================================================ TABLA GENERAL
filas = ''
for a in sorted(D):
    ej = D[a]['sueldos'][str(EJ)]
    nom = f'<a href="{slug(a)}">{anos(a)}</a>' if a in PAGINAS else anos(a)
    filas += f'<tr><td>{nom}{" *" if ej["pre"] else ""}</td><td>{dias_txt(ej["impDias"])}</td><td><strong>{e(ej["imp"])} €</strong></td><td>{dias_txt(min(20 * a, 365))}</td><td>{e(ej["obj"])} €</td></tr>'
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">⚖️ Despido 2026</div><h1>Tabla de indemnización por despido<br><span class="highlight">de 1 a 25 años</span></h1><p>Cuántos días de salario y cuánto dinero te corresponden según tu antigüedad, si el despido es improcedente u objetivo.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>33 días</strong><span>por año, improcedente</span></div><div><strong>20 días</strong><span>por año, objetivo o ERE</span></div><div><strong>12 días</strong><span>por año, fin de temporal</span></div></div>
        <h2 class="puentes-titulo">📋 Indemnización según antigüedad</h2>
        <div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th rowspan="2">Antigüedad</th><th colspan="2">Improcedente</th><th colspan="2">Objetivo</th></tr><tr><th>Días</th><th>Euros</th><th>Días</th><th>Euros</th></tr></thead><tbody>{filas}</tbody></table></div>
        <p class="nota-corta">Ejemplo con 2.000 € brutos al mes en 14 pagas y despido el 19/10/2026. * Empezó antes del 12/02/2012: el tramo anterior se paga a 45 días por año. Máximos: 720 días (improcedente) y 12 mensualidades, 365 días (objetivo).</p>
        {CTA}
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📖 Cómo usar la tabla</h2>
<p>Busca tu antigüedad y mira los días de salario que te corresponden. Para pasarlos a euros, multiplícalos por tu <strong>salario diario</strong>: tu sueldo bruto anual con pagas extra dividido entre 365. Si llevas años sueltos y meses, cuentan también los meses: cada mes suma la doceava parte de un año.</p>
<p>Para tu caso exacto, con tus fechas, usa la calculadora de <a href="despido-improcedente">despido improcedente</a>, la de <a href="despido-objetivo">despido objetivo</a> o la del <a href="ere">ERE</a>. Y no olvides el <a href="finiquito">finiquito</a>, que se cobra aparte.</p>
<h2>📅 Antigüedades más buscadas</h2>
<div class="enlaces-sueldo">{"".join(f'<a href="{slug(p)}">{anos(p)}</a>' for p in PAGINAS)}</div>
</article></div></section>
'''
faqs = [
    ('¿Cuántos días de indemnización son por año trabajado?', '<strong>33 días</strong> por año si el despido es improcedente, <strong>20</strong> si es objetivo o un ERE y <strong>12</strong> al terminar un contrato temporal.'),
    ('¿Cuál es el máximo de indemnización por despido?', 'En el improcedente, <strong>24 mensualidades</strong> (720 días de salario), salvo que el tramo anterior a 2012 ya supere esa cifra. En el objetivo, <strong>12 mensualidades</strong>.'),
    ('¿Qué pasa si empecé a trabajar antes de 2012?', 'El tiempo trabajado hasta el 11 de febrero de 2012 se paga a <strong>45 días por año</strong> en el despido improcedente, y el resto a 33.'),
]
gen.append(pagina('tabla-indemnizacion-despido', 'Tabla de indemnización por despido 2026 (1 a 25 años)', 'Tabla de indemnización por despido 2026: días de salario y euros según tu antigüedad, de 1 a 25 años, si el despido es improcedente (33 días) u objetivo (20 días).', 'tabla indemnización despido, indemnización por despido 2026, días por año despido, cuánto me corresponde de despido', MIGA + [('Tabla de indemnizaciones', None)], cuerpo, faqs, FUENTE, 'Despido'))

json.dump(gen, open(f'{AQUI}/generadas.json', 'w'))
print(len(gen), 'páginas')
