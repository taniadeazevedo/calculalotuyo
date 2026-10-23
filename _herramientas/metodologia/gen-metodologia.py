# «Cómo calculamos»: fuentes oficiales y método de trabajo de CalculaLoTuyo (21/10/2026).
# Google y las IAs valoran ver de dónde salen los datos; se enlaza desde el pie y desde «Revisado el…» de cada página.
# Uso: python3 _herramientas/metodologia/gen-metodologia.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO

REV = REVISADO.format(fecha='21 de octubre de 2026')
boe = lambda id_, txt, act=True: f'<a href="https://www.boe.es/{"buscar/act" if act else "diario_boe/txt"}.php?id={id_}" target="_blank" rel="noopener">{txt}</a>'
SEPG = 'https://www.sepg.pap.hacienda.gob.es/sitios/sepg/es-ES/CostesPersonal/EstadisticasInformes/Documents/A%C3%91O%202026/Retribuciones%20del%20personal%20funcionario%202026.%20Real%20Decreto-ley%2014%202025%2C%20de%202%20de%20diciembre..pdf'

# (tema, [calculadoras], fuentes)
FUENTES = [
    ('⚖️ Despido, finiquito, vacaciones, horas extra y pagas extra', 'despido-improcedente">despido</a>, <a href="finiquito">finiquito</a>, <a href="vacaciones">vacaciones</a>, <a href="horas-extra">horas extra</a>, <a href="pagas-extra">pagas extra</a>, <a href="reduccion-jornada">reducción de jornada',
     f'{boe("BOE-A-2015-11430", "Estatuto de los Trabajadores")} (Real Decreto Legislativo 2/2015), versión consolidada.'),
    ('📊 Paro, baja médica y jubilación', 'paro">paro</a>, <a href="baja-medica">baja médica</a>, <a href="jubilacion">jubilación',
     f'{boe("BOE-A-2015-11724", "Ley General de la Seguridad Social")} (Real Decreto Legislativo 8/2015) y pensión máxima de 2026 del {boe("BOE-A-2026-2548", "Real Decreto-ley 3/2026", False)}.'),
    ('🏦 Sueldo neto, IRPF y nómina', 'sueldo-neto">sueldo neto</a>, <a href="neto-a-bruto">neto a bruto</a>, <a href="irpf">retención de IRPF',
     f'Algoritmo de cálculo de retenciones de 2026 de la Agencia Tributaria, {boe("BOE-A-2006-20764", "Ley 35/2006 del IRPF")}, bases y tipos de cotización de 2026 (Orden PJC/297/2026) y salario mínimo del {boe("BOE-A-2026-3815", "Real Decreto 126/2026", False)}.'),
    ('🧾 Renta y lotería', 'obligado-a-declarar-renta">¿tengo que hacer la renta?</a>, <a href="loteria-navidad-hacienda">lotería',
     f'{boe("BOE-A-2006-20764", "Ley 35/2006 del IRPF")}: artículo 96 (obligación de declarar) y disposición adicional 33.ª (premios de lotería), y {boe("BOE-A-2021-21007", "Ley 19/2021 del ingreso mínimo vital")}.'),
    ('💼 Autónomos', 'cuota-autonomos">cuota de autónomos</a>, <a href="facturas">facturas',
     'Tramos de cotización por rendimientos de 2026 de la Ley General de la Seguridad Social y tipos de IVA y retención de IRPF vigentes.'),
    ('🏛️ Funcionarios', 'sueldo-funcionario-2026">sueldo de funcionarios',
     f'<a href="{SEPG}" target="_blank" rel="noopener">Retribuciones del personal funcionario 2026</a> del Ministerio de Hacienda y {boe("BOE-A-2025-24445", "Real Decreto-ley 14/2025", False)}.'),
    ('📅 Calendario laboral', 'calendario-laboral-2027">calendario 2027</a>, <a href="puentes-2027">puentes</a>, <a href="dias-laborables">días laborables',
     f'Fiestas laborales de 2027: {boe("BOE-A-2026-21254", "Resolución de 8 de octubre de 2026", False)}. Fiestas locales: el boletín oficial de cada provincia o comunidad, enlazado en la página de cada ciudad.'),
]
filas = ''.join(f'<tr><td><strong>{t}</strong><br><small><a href="{c}</a></small></td><td>{f}</td></tr>' for t, c, f in FUENTES)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🔍 Método y fuentes</div><h1>Cómo calculamos<br><span class="highlight">de dónde sale cada cifra</span></h1><p>Todas las calculadoras usan la ley publicada en el BOE y las cifras oficiales del año. Aquí tienes las fuentes de cada una y cómo las mantenemos al día.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<h2>✅ Cómo trabajamos</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Leemos la norma en el BOE</strong><p>Siempre la versión consolidada (la que está en vigor), no resúmenes de terceros. Si una cifra no se puede comprobar en una fuente oficial, no la publicamos.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Las cifras del año, en un solo sitio</strong><p>Salario mínimo, IPREM, bases y tipos de cotización, topes del paro, pensión máxima… están en un único archivo que usan todas las calculadoras. Así una cifra no puede estar bien en una página y mal en otra.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Pruebas automáticas</strong><p>Cada calculadora se comprueba con casos calculados a mano según la ley (por ejemplo, un despido de 5 años con 28.000 € al año). Si algún cambio altera un resultado, lo sabemos antes de publicarlo.</p></div></div>
    <div class="calc-step"><span class="step-num">4</span><div><strong>Revisión continua</strong><p>Revisamos el BOE cada mes y actualizamos las cifras de cada año en cuanto se publican (normalmente en enero). Cada página muestra la fecha de su última revisión.</p></div></div>
</div>

<h2>🔎 Última comprobación completa</h2>
<p>El <strong>23 de octubre de 2026</strong> contrastamos una a una, con el texto del BOE, todas las cifras que usa el cálculo del sueldo neto y del IRPF: la escala de retención y el tope del 43 % (arts. 85 y 86 del Reglamento del IRPF), los importes por debajo de los cuales no se retiene (art. 81), los 2.000 € de gastos y su aumento por discapacidad (art. 19 de la Ley del IRPF), la reducción por rendimientos del trabajo (art. 20), los mínimos personal, por hijos, por ascendientes y por discapacidad (arts. 57 a 60) y los tipos de cotización y la cuota de solidaridad de 2026 (Orden PJC/297/2026). Todas coinciden.</p>

<h2>📚 Fuentes de cada calculadora</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Tema</th><th>Fuente oficial</th></tr></thead><tbody>{filas}</tbody></table></div>

<h2>⚠️ Lo que no podemos calcular</h2>
<ul>
<li><strong>Tu convenio colectivo:</strong> puede mejorar lo que dice la ley (más días de vacaciones, pagas extra más altas, complementos en la baja…). Las calculadoras usan la ley y te dejan cambiar esas cifras en «Más opciones».</li>
<li><strong>Casos muy particulares:</strong> despidos con salarios variables, contratos a tiempo parcial con cambios de jornada, situaciones fiscales poco habituales…</li>
<li>Por eso los resultados son <strong>orientativos</strong>. Para decisiones importantes, como firmar un finiquito o reclamar un despido, contrasta con un abogado laboralista, un graduado social o tu sindicato.</li>
</ul>

<h2>📬 ¿Has visto un error?</h2>
<p>Escríbenos desde la página de <a href="contacto">contacto</a> con la calculadora y los datos que usaste. Lo revisamos con la norma y, si hay un error, lo corregimos y actualizamos la fecha de revisión. Más sobre quién hay detrás en <a href="sobre-el-proyecto">sobre el proyecto</a>.</p>
</article></div></section>
'''
faqs = [
    ('¿De dónde salen las cifras de CalculaLoTuyo?', 'De la ley publicada en el <strong>BOE</strong> (Estatuto de los Trabajadores, Ley General de la Seguridad Social, Ley del IRPF…) y de las cifras oficiales de cada año: salario mínimo, cotizaciones, topes del paro y algoritmo de retenciones de la Agencia Tributaria.'),
    ('¿Cada cuánto se actualizan las calculadoras?', 'Revisamos el BOE cada mes y actualizamos las cifras de cada año en cuanto se publican, normalmente en enero. Cada página muestra la fecha de su última revisión.'),
    ('¿Son exactos los resultados?', 'Siguen la ley al pie de la letra, pero son orientativos: tu convenio colectivo o tu situación concreta pueden cambiar el resultado.'),
]
pagina('como-calculamos', 'Cómo calculamos: fuentes oficiales y método | CalculaLoTuyo',
    'De dónde sale cada cifra de CalculaLoTuyo: Estatuto de los Trabajadores, Seguridad Social, Ley del IRPF y BOE. Cómo revisamos y probamos las calculadoras.',
    'cómo se calcula, fuentes calculadora laboral, BOE, metodología', [('Cómo calculamos', None)], cuerpo, faqs,
    'Las normas enlazadas en la tabla, en su versión consolidada del BOE, y las cifras oficiales de 2026.')
print('creada: como-calculamos')
