# Informe para prensa: «De cada 100 € que cuesta un trabajador, cuánto llega a su bolsillo» (2026).
# Datos propios calculados con el motor de la web (sueldos.json, de _herramientas/sueldos/calcular.js).
# Uso: python3 _herramientas/informe/gen-informe.py
import csv, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, REVISADO, AD, RAIZ

D = {int(k): v['base'] for k, v in json.load(open(os.path.join(AQUI, '..', 'sueldos', 'sueldos.json')))['datos'].items()}
SMI = 17094
SUELDOS = [SMI, 20000, 22000, 25000, 28000, 30000, 35000, 40000, 45000, 50000, 55000, 60000]   # hasta 60.000: por encima entra la cuota de solidaridad
SLUG = 'informe-sueldo-coste-empresa-2026'
REV = REVISADO.format(fecha='19 de octubre de 2026')

def fila(b):
    x = D[b]; ss_emp = x['coste'] - b
    return dict(bruto=b, coste=x['coste'], ss_empresa=ss_emp, ss_trabajador=x['ss'], irpf=x['irpf'], neto=x['neto'],
                pct_neto=x['neto'] / x['coste'] * 100, pct_irpf=x['irpf'] / x['coste'] * 100,
                pct_ss_trab=x['ss'] / x['coste'] * 100, pct_ss_emp=ss_emp / x['coste'] * 100)
F = {b: fila(b) for b in SUELDOS}
f30, fsmi, f60 = F[30000], F[SMI], F[60000]

# ---- Datos descargables para periodistas (CSV)
os.makedirs(os.path.join(RAIZ, 'datos'), exist_ok=True)
with open(os.path.join(RAIZ, 'datos', 'sueldo-coste-empresa-2026.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['sueldo_bruto_anual', 'coste_empresa', 'cotizacion_empresa', 'cotizacion_trabajador', 'retencion_irpf', 'neto_anual', 'neto_mes_12_pagas', 'porcentaje_neto_sobre_coste'])
    for b in SUELDOS:
        f = F[b]; w.writerow([b, round(f['coste'], 2), round(f['ss_empresa'], 2), round(f['ss_trabajador'], 2), round(f['irpf'], 2), round(f['neto'], 2), round(f['neto'] / 12, 2), round(f['pct_neto'], 1)])

pct = lambda n: e(n, 1) + ' %'
barras = ''.join(f'''<div class="inf-fila"><span class="inf-nombre">{e(b)} €{' (SMI)' if b == SMI else ''}</span><div class="reparto inf-barra">
<span class="r-neto" style="width:{F[b]["pct_neto"]:.1f}%" title="Neto: {pct(F[b]["pct_neto"])}">{e(F[b]["pct_neto"])} %</span><span class="r-irpf" style="width:{F[b]["pct_irpf"]:.1f}%" title="IRPF"></span><span class="r-ss" style="width:{F[b]["pct_ss_trab"]:.1f}%" title="Seguridad Social del trabajador"></span><span class="r-emp" style="width:{F[b]["pct_ss_emp"]:.1f}%" title="Seguridad Social de la empresa"></span></div></div>''' for b in SUELDOS)
tabla = ''.join(f'<tr><td>{e(b)} €</td><td>{e(F[b]["coste"])} €</td><td>{e(F[b]["ss_empresa"])} €</td><td>{e(F[b]["ss_trabajador"])} €</td><td>{e(F[b]["irpf"])} €</td><td><strong>{e(F[b]["neto"])} €</strong></td><td>{pct(F[b]["pct_neto"])}</td></tr>' for b in SUELDOS)
cita = f'CalculaLoTuyo (2026). «De cada 100 € que cuesta un trabajador, cuánto llega a su bolsillo». https://calculalotuyo.es/{SLUG}'

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📰 Informe 2026</div><h1>De cada 100 € que cuesta un trabajador<br><span class="highlight">solo {e(f30["pct_neto"])} llegan a su bolsillo</span></h1><p>Un sueldo de 30.000 € brutos le cuesta {e(f30["coste"])} € a la empresa, pero el trabajador se queda con {e(f30["neto"])} €. Lo calculamos para cada sueldo con las cifras oficiales de 2026.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="cifras"><div><strong>{pct(fsmi["pct_neto"])}</strong><span>llega al bolsillo con el salario mínimo</span></div><div><strong>{pct(f30["pct_neto"])}</strong><span>con 30.000 € brutos</span></div><div><strong>{pct(f60["pct_neto"])}</strong><span>con 60.000 € brutos</span></div></div>
        <h2 class="puentes-titulo">📊 Adónde va el coste de un trabajador</h2>
        <div class="reparto-leyenda"><span><i class="r-neto"></i>Para el trabajador (neto)</span><span><i class="r-irpf"></i>IRPF</span><span><i class="r-ss"></i>Seguridad Social del trabajador</span><span><i class="r-emp"></i>Seguridad Social de la empresa</span></div>
        <div class="inf-barras">{barras}</div>
        <p class="nota-corta">Cada barra es el 100 % de lo que el trabajador le cuesta a la empresa al año. Persona sin hijos, contrato indefinido, 2026.</p>
        <div class="result-actions"><a href="datos/sueldo-coste-empresa-2026.csv" class="btn" download>📥 Descargar los datos (CSV)</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🔑 Lo más importante</h2>
<ul>
<li>Un trabajador con <strong>30.000 € brutos</strong> le cuesta a la empresa <strong>{e(f30["coste"])} €</strong> al año. De ellos, {e(f30["ss_empresa"])} € son cotizaciones de la empresa, {e(f30["ss_trabajador"])} € cotizaciones del trabajador y {e(f30["irpf"])} € retención de IRPF. Le quedan <strong>{e(f30["neto"])} €</strong>: {e(f30["neto"] / 12)} € al mes en 12 pagas.</li>
<li>Con el <strong>salario mínimo</strong> ({e(SMI)} € al año), llega al bolsillo el <strong>{pct(fsmi["pct_neto"])}</strong> del coste. Con <strong>60.000 €</strong>, el <strong>{pct(f60["pct_neto"])}</strong>.</li>
<li>Las <strong>cotizaciones de la empresa</strong> (un 30,65 % del bruto) son la parte más grande de la diferencia en los sueldos bajos y medios: con 30.000 € suponen {pct(f30["pct_ss_emp"])} del coste, más que el IRPF ({pct(f30["pct_irpf"])}).</li>
<li>El IRPF es lo que más crece con el sueldo: pasa del {pct(F[20000]["pct_irpf"])} del coste con 20.000 € al {pct(f60["pct_irpf"])} con 60.000 €.</li>
</ul>
<h2>📋 Los datos completos</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Bruto/año</th><th>Coste empresa</th><th>SS empresa</th><th>SS trabajador</th><th>IRPF</th><th>Neto</th><th>Neto/coste</th></tr></thead><tbody>{tabla}</tbody></table></div>
<h2>🧪 Metodología</h2>
<ul>
<li><strong>Cotización de la empresa:</strong> 30,65 % del bruto (contingencias comunes 23,60 %, desempleo 5,50 %, FOGASA 0,20 %, formación 0,60 % y MEI 0,75 %), con la base máxima de 2026 (Orden PJC/297/2026). No incluye accidentes de trabajo y enfermedades profesionales, que dependen de la actividad.</li>
<li><strong>Cotización del trabajador:</strong> 6,50 % (contrato indefinido).</li>
<li><strong>IRPF:</strong> retención calculada con el algoritmo de la Agencia Tributaria para 2026, para una persona sin hijos, menor de 65 años. Es la retención de la nómina, no el impuesto final de la renta. Con el salario mínimo, la retención se recupera en la renta gracias a la deducción de 2026.</li>
<li>Llega hasta 60.000 €: por encima se aplica la cuota de solidaridad, que no está incluida en este cálculo.</li>
<li>Calculado con el mismo motor que nuestra <a href="sueldo-neto">calculadora de sueldo neto</a>. Puedes ver cada sueldo en detalle en la <a href="sueldo-bruto-a-neto-2026">tabla de sueldo bruto a neto</a>.</li>
</ul>
<h2>📰 Cómo citar este informe</h2>
<div class="aviso-ccaa">Puedes usar estos datos y gráficos libremente citando la fuente con un enlace (licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es" target="_blank" rel="noopener">CC BY 4.0</a>):<br><strong>{cita}</strong></div>
<p>Si eres periodista y necesitas otro cálculo (otro sueldo, con hijos, con contrato temporal…), escríbenos desde la página de <a href="contacto">contacto</a>.</p>
</article></div></section>
'''
faqs = [('¿Cuánto le cuesta a una empresa un trabajador de 30.000 € brutos?', f'Unos <strong>{e(f30["coste"])} € al año</strong>, sumando el sueldo bruto y las cotizaciones de la empresa a la Seguridad Social (un 30,65 %).'),
        ('¿Qué parte del coste de un trabajador llega a su bolsillo?', f'Depende del sueldo: el <strong>{pct(fsmi["pct_neto"])}</strong> con el salario mínimo, el <strong>{pct(f30["pct_neto"])}</strong> con 30.000 € y el <strong>{pct(f60["pct_neto"])}</strong> con 60.000 € brutos.'),
        ('¿Puedo usar estos datos?', 'Sí, libremente, citando la fuente con un enlace a esta página. Puedes descargar los datos en CSV.')]
pagina(SLUG, 'Informe 2026: lo que cuesta un trabajador y lo que cobra',
       f'De cada 100 € que cuesta un trabajador con 30.000 € brutos, solo {e(f30["pct_neto"])} llegan a su bolsillo. Coste para la empresa, cotizaciones, IRPF y neto de cada sueldo.',
       'coste empresa trabajador 2026, cuánto cuesta un trabajador a la empresa, cuña fiscal España, cotizaciones empresa 2026, informe sueldo neto',
       [('Informe 2026', None)], cuerpo, faqs,
       'Cálculo propio de CalculaLoTuyo con las cifras oficiales de 2026: Orden PJC/297/2026 (cotizaciones) y algoritmo de retenciones de la Agencia Tributaria.', 'Nómina')
# Marcado «Dataset»: Google sabe que el CSV son datos citables (sale en Google Dataset Search)
ld_datos = json.dumps({'@context': 'https://schema.org', '@type': 'Dataset', 'name': 'Coste de un trabajador para la empresa y sueldo neto por salario bruto (España, 2026)',
    'description': f'Para cada sueldo bruto anual de {e(SMI)} € a 60.000 €: coste para la empresa, cotizaciones de empresa y trabajador, retención de IRPF, neto anual y porcentaje del coste que llega al trabajador. Cálculo con las cifras oficiales de 2026.',
    'url': f'https://calculalotuyo.es/{SLUG}', 'keywords': ['sueldo neto', 'coste empresa', 'cotizaciones', 'IRPF', 'España', '2026'],
    'license': 'https://creativecommons.org/licenses/by/4.0/', 'isAccessibleForFree': True, 'inLanguage': 'es-ES',
    'temporalCoverage': '2026', 'spatialCoverage': {'@type': 'Place', 'name': 'España'},
    'creator': {'@type': 'Organization', 'name': 'CalculaLoTuyo', 'url': 'https://calculalotuyo.es/'},
    'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'text/csv', 'contentUrl': 'https://calculalotuyo.es/datos/sueldo-coste-empresa-2026.csv'}]}, ensure_ascii=False, indent=1)
ruta = os.path.join(RAIZ, SLUG + '.html'); html = open(ruta, encoding='utf-8').read()
open(ruta, 'w', encoding='utf-8').write(html.replace('</head>', f'    <script type="application/ld+json">\n{ld_datos}\n    </script>\n</head>', 1))
print('creado:', SLUG, '· neto/coste 30.000 =', round(f30['pct_neto'], 1))
