# Sección «Novedades»: actualidad que toca el bolsillo (sueldo, paro, impuestos, pensiones), contada de forma neutra
# y con fuentes oficiales. Fórmula de cada artículo: qué ha pasado → qué cambia para ti → calcula cómo te afecta.
# Genera: cada artículo, la portada /novedades, el RSS (feed.xml), la imagen grande para Google Discover y lista.json
# (la usan el menú, la portada y el buscador). Uso: python3 _herramientas/novedades/gen-novedades.py
import datetime as dt, html as H, json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, RAIZ

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
larga = lambda f: f'{int(f[8:])} de {MESES[int(f[5:7]) - 1]} de {f[:4]}'            # «2026-10-22» → «22 de octubre de 2026»
pc = lambda x, d=1: f'{x:.{d}f}'.replace('.', ',') + ' %'
boe = lambda id_, txt, act=False: f'<a href="https://www.boe.es/{"buscar/act" if act else "diario_boe/txt"}.php?id={id_}" target="_blank" rel="noopener">{txt}</a>'
ine = lambda mes, txt: f'<a href="https://www.ine.es/dyngs/Prensa/IPC{mes}26.htm" target="_blank" rel="noopener">{txt}</a>'

# ================================================================ DATOS (todos comprobados en fuente oficial el 22/10/2026)
# IPC general, tasa anual (INE, notas de prensa de cada mes). La revalorización de las pensiones usa la media de diciembre a noviembre.
IPC = [('dic 2025', 2.9), ('ene', 2.3), ('feb', 2.3), ('mar', 3.4), ('abr', 3.2), ('may', 3.2), ('jun', 3.2), ('jul', 3.6), ('ago', 4.3), ('sep', 4.9)]
suma = sum(v for _, v in IPC)
escenario = lambda octnov: (suma + 2 * octnov) / 12                    # media de los 12 meses si octubre y noviembre quedan en ese valor
ESC = [(4.5, escenario(4.5)), (4.9, escenario(4.9)), (5.3, escenario(5.3))]
CENTRAL = ESC[1][1]
PENSION_MAX = 3359.60                                                   # 2026, RDL 3/2026

# Deducción por alquiler (LIRPF art. 68.6, añadido por el RDL 29/2026)
def base_max(bi):
    if bi <= 23007.20: return 11630
    if bi < 33007.20: return max(0, 11630 - 1.163 * (bi - 23007.20))
    return 0
ESCALA_ESTATAL = [(12450, .095), (20200, .12), (35200, .15), (60000, .185), (300000, .225), (float('inf'), .245)]
def escala(b):
    t, ant = 0, 0
    for lim, tipo in ESCALA_ESTATAL:
        if b > ant: t += (min(b, lim) - ant) * tipo
        ant = lim
    return t
cuota_estatal = lambda bi: max(0, escala(bi) - escala(5550))           # cuota íntegra estatal aproximada (mínimo personal de 5.550 €)
ALQ = 8400                                                              # 700 € al mes
# (sueldo bruto, base imponible aproximada) calculada con el motor de la web: bruto − Seguridad Social − 2.000 € − reducción por trabajo
FILAS_ALQ = [(22000, 17227.65), (25000, 21375.00), (28000, 24180.00), (30000, 26050.00), (35000, 30725.00)]
ded = lambda bi: min(0.10 * min(ALQ, base_max(bi)), cuota_estatal(bi))

# ================================================================ ARTÍCULOS (el más nuevo, primero)
ARTICULOS = [
 dict(slug='subida-pensiones-2027', fecha='2026-10-22', actualizado='2026-10-22', tema='Pensiones',
  titulo='Subida de las pensiones en 2027: cuánto subirán',
  desc=f'Con el IPC de 2026, las pensiones subirían en enero de 2027 en torno a un {pc(CENTRAL)}. Cómo se calcula, escenarios y cuánto más cobrarás al mes.',
  h1='¿Cuánto subirán las pensiones en 2027?', sub=f'En torno a un {pc(CENTRAL)}, según el IPC de 2026',
  img=['Pensiones 2027', f'subirían en torno a un {pc(CENTRAL)}'],
  resumen=[f'Las pensiones contributivas suben cada enero lo mismo que la <strong>media del IPC de diciembre a noviembre</strong> (art. 58 de la Ley General de la Seguridad Social).',
           f'Con los datos del INE hasta septiembre, la subida de 2027 rondaría el <strong>{pc(ESC[0][1])}–{pc(ESC[2][1])}</strong>.',
           'El dato exacto se sabrá a <strong>mediados de diciembre</strong>, cuando el INE publique el IPC de noviembre.'],
  calculadoras=[('jubilacion', '🌅 Calcula tu jubilación'), ('obligado-a-declarar-renta', '🧾 Con pensión, ¿tienes que hacer la renta?')],
  cuerpo=lambda: f'''
<h2>📌 Qué dice la ley</h2>
<p>Desde 2024, las pensiones contributivas de la Seguridad Social se revalorizan al empezar cada año en el porcentaje del <strong>valor medio de las tasas anuales del IPC de los doce meses anteriores a diciembre</strong>: de diciembre del año anterior a noviembre. Si esa media fuera negativa, las pensiones no bajarían. La pensión máxima y las mínimas se actualizan en ese mismo porcentaje en los Presupuestos.</p>
<h2>📊 El IPC de 2026 mes a mes</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Mes</th><th>IPC anual</th></tr></thead><tbody>{''.join(f'<tr><td>{m}</td><td>{pc(v)}</td></tr>' for m, v in IPC)}<tr><td>oct y nov</td><td>pendientes</td></tr></tbody></table></div>
<p>La media de los diez meses conocidos es del <strong>{pc(suma / len(IPC), 2)}</strong>. Faltan octubre y noviembre, y como la inflación ha subido en los últimos meses, la media final será algo mayor.</p>
<h2>🔮 Tres escenarios para 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Si el IPC de octubre y noviembre es del…</th><th>Las pensiones subirían</th><th>Pensión máxima en 2027</th></tr></thead><tbody>{''.join(f'<tr><td>{pc(o)}</td><td><strong>{pc(r, 2)}</strong></td><td>{e(PENSION_MAX * (1 + r / 100), 2)} € al mes</td></tr>' for o, r in ESC)}</tbody></table></div>
<p class="nota-corta">Cálculo propio con los datos oficiales del INE. Es una estimación: el porcentaje definitivo lo fija el Gobierno con el IPC de noviembre.</p>
<h2>💶 Cuánto más cobrarías al mes</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Pensión en 2026</th><th>Con una subida del {pc(CENTRAL)}</th><th>Al mes</th><th>Al año (14 pagas)</th></tr></thead><tbody>{''.join(f'<tr><td>{e(p)} €</td><td><strong>{e(p * (1 + CENTRAL / 100), 2)} €</strong></td><td>+{e(p * CENTRAL / 100, 2)} €</td><td>+{e(p * CENTRAL / 100 * 14)} €</td></tr>' for p in (800, 1000, 1200, 1500, 2000, 2500))}</tbody></table></div>
<h2>⏳ Qué falta por saber</h2>
<ul><li>El <strong>IPC de octubre</strong> (adelantado a finales de octubre) y el de <strong>noviembre</strong> (a mediados de diciembre).</li><li>El porcentaje lo aprueba el Gobierno y se aplica en la nómina de <strong>enero de 2027</strong>.</li><li>Las pensiones <strong>no contributivas</strong> y las mínimas pueden tener subidas distintas: se fijan aparte.</li></ul>
<p>Actualizaremos este artículo con cada dato nuevo del INE.</p>''',
  faqs=[('¿Cuánto subirán las pensiones en 2027?', f'Con los datos del IPC hasta septiembre, en torno a un <strong>{pc(CENTRAL)}</strong> (entre un {pc(ESC[0][1])} y un {pc(ESC[2][1])} según el IPC de octubre y noviembre). El dato exacto se sabrá a mediados de diciembre.'),
        ('¿Cómo se calcula la subida de las pensiones?', 'Es la media de las tasas anuales del IPC de diciembre del año anterior a noviembre del año en curso (art. 58 de la Ley General de la Seguridad Social).'),
        ('¿Cuándo se cobra la subida de las pensiones de 2027?', 'En la nómina de enero de 2027, una vez el Gobierno apruebe el porcentaje con el IPC de noviembre.')],
  fuentes=f'{boe("BOE-A-2015-11724", "Ley General de la Seguridad Social, art. 58", True)}; {ine("09", "INE: IPC de septiembre de 2026")} y notas de enero a agosto; pensión máxima de 2026: {boe("BOE-A-2026-2548", "Real Decreto-ley 3/2026")}.',
  kw='subida pensiones 2027, cuánto suben las pensiones 2027, revalorización pensiones 2027, pensión máxima 2027'),

 dict(slug='deduccion-alquiler-renta', fecha='2026-10-22', actualizado='2026-10-22', tema='Renta',
  titulo='Nueva deducción del 10 % por alquiler en la renta',
  desc='Quien vive de alquiler y tiene una base imponible de menos de 33.007 € puede deducirse el 10 % de lo que paga. Requisitos, ejemplos y qué falta por aprobar.',
  h1='Nueva deducción del 10 % por el alquiler en la renta', sub='Quién puede aplicarla y cuánto ahorras',
  img=['Deducción por alquiler', 'el 10 % de lo que pagas'],
  resumen=['El <strong>Real Decreto-ley 29/2026</strong> (BOE del 7 de octubre) crea una deducción estatal del <strong>10 % del alquiler de tu vivienda habitual</strong>.',
           'Es para quien tiene una <strong>base imponible de menos de 33.007,20 €</strong>, con un máximo de 11.630 € de alquiler al año (1.163 € de deducción).',
           'Está en vigor desde el 8 de octubre de 2026, pero <strong>el Congreso tiene que convalidarlo</strong>: un decreto parecido de septiembre fue derogado.'],
  calculadoras=[('obligado-a-declarar-renta', '🧾 ¿Tienes que hacer la renta?'), ('irpf', '📑 Calcula tu retención de IRPF'), ('sueldo-neto', '🏦 Tu sueldo neto')],
  cuerpo=lambda: f'''
<h2>📌 Qué ha pasado</h2>
<p>El 7 de octubre de 2026 el BOE publicó el Real Decreto-ley 29/2026, de medidas sobre vivienda. Entre otras cosas, añade a la Ley del IRPF una <strong>deducción por alquiler de la vivienda habitual</strong> (nuevo apartado 6 del artículo 68), que se resta de la parte estatal del impuesto.</p>
<h2>✅ Quién puede aplicarla</h2>
<ul>
<li>Quien paga el <strong>alquiler de su vivienda habitual</strong>.</li>
<li>Con una <strong>base imponible de menos de 33.007,20 € al año</strong>. La base imponible no es el sueldo bruto: es lo que queda tras restar la Seguridad Social y algunos gastos (sale en tu declaración).</li>
<li>Que durante al menos la mitad del año ni tú ni tu unidad familiar seáis dueños de <strong>otra vivienda a menos de 50 km</strong> de la alquilada (salvo que no podáis usarla por una resolución administrativa o judicial).</li>
</ul>
<h2>🧮 Cuánto puedes deducirte</h2>
<p>El <strong>10 % de lo que pagas de alquiler</strong>, con un límite de alquiler que depende de tu base imponible:</p>
<ul><li>Base imponible de hasta 23.007,20 €: hasta <strong>11.630 €</strong> de alquiler al año (deducción máxima de 1.163 €).</li><li>Entre 23.007,20 € y 33.007,20 €: el límite baja poco a poco (11.630 € menos 1,163 veces lo que pases de 23.007,20 €).</li><li>Desde 33.007,20 €: no hay deducción.</li></ul>
<h3>Ejemplos con un alquiler de 700 € al mes (8.400 € al año)</h3>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Sueldo bruto al año</th><th>Base imponible aprox.</th><th>Deducción aproximada</th></tr></thead><tbody>{''.join(f'<tr><td>{e(b)} €</td><td>{e(bi)} €</td><td><strong>{e(ded(bi))} €</strong></td></tr>' for b, bi in FILAS_ALQ)}</tbody></table></div>
<p class="nota-corta">Persona sola, sin hijos ni otros ingresos, contrato indefinido. Cálculo propio y aproximado: la deducción no puede ser mayor que la parte estatal del impuesto, así que con sueldos bajos el ahorro real puede ser menor.</p>
<h2>⏳ Qué falta por saber</h2>
<ul>
<li><strong>La convalidación:</strong> un real decreto-ley tiene que ser convalidado por el Congreso en unos 30 días. El anterior (Real Decreto-ley 26/2026, de 29 de septiembre) <strong>fue derogado</strong>, así que hasta entonces esta deducción no es segura.</li>
<li><strong>Desde cuándo cuenta el alquiler:</strong> está en vigor desde el 8 de octubre de 2026. Falta que Hacienda aclare si en la renta de 2026 cuentan todos los alquileres del año o solo los pagados desde esa fecha.</li>
<li>Es una deducción <strong>estatal</strong>: muchas comunidades autónomas tienen además las suyas propias.</li>
</ul>
<p>Guarda los recibos o transferencias del alquiler y el contrato. Actualizaremos este artículo cuando el Congreso vote y cuando Hacienda publique los modelos de la renta.</p>''',
  faqs=[('¿Quién puede deducirse el alquiler en la renta de 2026?', 'Quien paga el alquiler de su vivienda habitual y tiene una <strong>base imponible de menos de 33.007,20 €</strong>, siempre que no tenga otra vivienda a menos de 50 km. Depende de que el Congreso convalide el Real Decreto-ley 29/2026.'),
        ('¿Cuánto se puede deducir por el alquiler?', 'El <strong>10 %</strong> de lo pagado, con un máximo de 11.630 € de alquiler al año (1.163 € de deducción) si la base imponible es de hasta 23.007,20 €. Por encima, el límite baja hasta desaparecer en 33.007,20 €.'),
        ('¿Está ya aprobada la deducción por alquiler?', 'Está en vigor desde el 8 de octubre de 2026 por el Real Decreto-ley 29/2026, pero el Congreso tiene que convalidarlo. El decreto anterior, de septiembre, fue derogado.')],
  fuentes=f'{boe("BOE-A-2026-20823", "Real Decreto-ley 29/2026, de 6 de octubre")} (art. 6, apartado segundo, cuatro: nuevo artículo 68.6 de la Ley 35/2006 del IRPF); {boe("BOE-A-2006-20764", "Ley 35/2006 del IRPF", True)}.',
  kw='deducción alquiler renta 2026, deducción alquiler vivienda habitual, real decreto ley 29/2026, desgravar alquiler renta'),

 dict(slug='ipc-septiembre-2026-sueldo', fecha='2026-10-22', actualizado='2026-10-22', tema='Sueldo',
  titulo='IPC al 4,9 % en septiembre: qué significa para tu sueldo',
  desc='La inflación sube al 4,9 % en septiembre de 2026, la más alta desde 2023. Qué pasa con las subidas de sueldo, los convenios, los funcionarios y las pensiones.',
  h1='IPC al 4,9 %: qué significa para tu sueldo', sub='La inflación más alta desde febrero de 2023',
  img=['IPC al 4,9 %', 'qué significa para tu sueldo'],
  resumen=['El IPC de septiembre de 2026 fue del <strong>4,9 %</strong> (INE), seis décimas más que en agosto y el más alto desde febrero de 2023.',
           'Para no perder poder de compra, un sueldo tendría que subir más o menos lo mismo. <strong>Nadie está obligado por ley a subirlo</strong>: depende de tu convenio o tu contrato.',
           'Los <strong>funcionarios</strong> tienen asegurado un 0,5 % extra si el IPC de 2026 llega al 1,5 %, y las <strong>pensiones</strong> subirán en enero según la media del año.'],
  calculadoras=[('subida-ipc', '📈 Calcula cuánto debería subir tu sueldo'), ('sueldo-neto', '🏦 Tu sueldo neto'), ('subida-pensiones-2027', '👵 Cuánto subirán las pensiones')],
  cuerpo=lambda: f'''
<h2>📌 Qué ha pasado</h2>
<p>Según el INE, la tasa anual del IPC subió en septiembre de 2026 hasta el <strong>4,9 %</strong>. La subyacente (sin alimentos frescos ni energía) quedó en el 3,1 %. El grupo que más subió fue el transporte, por los carburantes.</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Mes de 2026</th><th>IPC anual</th></tr></thead><tbody>{''.join(f'<tr><td>{m}</td><td>{pc(v)}</td></tr>' for m, v in IPC[1:])}</tbody></table></div>
<h2>💼 Qué significa para tu sueldo</h2>
<ul>
<li><strong>Por ley, la empresa no está obligada a subirte el sueldo con el IPC.</strong> Solo si lo dice tu convenio o tu contrato.</li>
<li>Muchos convenios tienen una <strong>cláusula de revisión</strong>: si el IPC del año (normalmente el de diciembre) supera la subida pactada, se cobra la diferencia. Mira la de tu convenio en el boletín de tu provincia o comunidad.</li>
<li>Para no perder poder de compra con un IPC del 4,9 %, un sueldo de 28.000 € brutos tendría que pasar a unos <strong>{e(28000 * 1.049)} €</strong>. Calcúlalo con tu sueldo en la calculadora de subida por IPC (opción «Personalizado»).</li>
</ul>
<h2>🏛️ Funcionarios: el 0,5 % extra</h2>
<p>El Real Decreto-ley 14/2025 subió los sueldos públicos un 1,5 % en 2026 y prevé <strong>un 0,5 % más si el IPC de 2026 llega al 1,5 %</strong>. Con la inflación actual todo apunta a que se cumplirá: se aprobaría con el dato del INE de 2026 y se cobraría en el primer trimestre de 2027. Mira las tablas en <a href="sueldo-funcionario-2026">sueldo de un funcionario en 2026</a>.</p>
<h2>👵 Pensiones</h2>
<p>Las pensiones subirán en enero de 2027 según la media del IPC de diciembre de 2025 a noviembre de 2026. Con estos datos, rondaría el {pc(CENTRAL)}: lo explicamos en <a href="subida-pensiones-2027">cuánto subirán las pensiones en 2027</a>.</p>
<h2>⏳ Qué falta por saber</h2>
<p>El dato adelantado de octubre sale a finales de mes y el de diciembre, que es el que usan muchos convenios, a mediados de enero de 2027. Actualizaremos este artículo con cada dato nuevo.</p>''',
  faqs=[('¿Cuánto es el IPC de septiembre de 2026?', 'Un <strong>4,9 %</strong> de tasa anual, según el INE: seis décimas más que en agosto y el más alto desde febrero de 2023.'),
        ('¿Me tienen que subir el sueldo con el IPC?', 'No por ley. Solo si lo dice tu convenio colectivo o tu contrato; muchos convenios tienen una cláusula de revisión según el IPC de diciembre.'),
        ('¿Cobrarán los funcionarios el 0,5 % extra de 2026?', 'Lo prevé el Real Decreto-ley 14/2025 si el IPC de 2026 llega al 1,5 %. Con la inflación actual todo apunta a que sí; se aprobaría con el dato de 2026 y se cobraría a principios de 2027.')],
  fuentes=f'{ine("09", "INE: IPC de septiembre de 2026")} (14 de octubre de 2026) y notas de enero a agosto; {boe("BOE-A-2025-24445", "Real Decreto-ley 14/2025")} (art. 2.2).',
  kw='ipc septiembre 2026, inflación septiembre 2026, subida sueldo ipc 2026, ipc 4,9'),
]

# ================================================================ PÁGINAS
from plantilla import REVISADO
CAJA_RESUMEN = lambda items: '<div class="respuesta-corta"><span>⚡ En 30 segundos</span><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
FLECHA = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def imagen(a):
    """Imagen grande (1200×630) para Google Discover y para compartir; se hace con Chrome solo si no existe."""
    carpeta = os.path.join(RAIZ, 'img', 'novedades'); os.makedirs(carpeta, exist_ok=True)
    png = os.path.join(carpeta, a['slug'] + '.png')
    if not os.path.exists(png):
        plantilla_og = open(os.path.join(RAIZ, '_herramientas', 'og', 'og-image.html'), encoding='utf-8').read()
        import re
        h = re.sub(r'<h1>.*?</h1><div class="s">.*?</div><div class="p">.*?</div>',
                   f'<h1 style="font-size:72px">{H.escape(a["img"][0])}</h1><div class="s">{H.escape(a["img"][1])}</div><div class="p">Novedades · {larga(a["fecha"])}</div>', plantilla_og, flags=re.S)
        tmp = os.path.join(AQUI, '_og-tmp.html'); open(tmp, 'w', encoding='utf-8').write(h)
        subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless=new', '--hide-scrollbars', '--window-size=1200,630', f'--screenshot={png}', 'file://' + tmp], capture_output=True, timeout=60)
        os.remove(tmp)
    return f'https://calculalotuyo.es/img/novedades/{a["slug"]}.png'

def marcado(a, img):
    return json.dumps({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': a['titulo'], 'description': a['desc'],
        'image': [img], 'datePublished': a['fecha'] + 'T09:00:00+02:00', 'dateModified': a['actualizado'] + 'T09:00:00+02:00',
        'mainEntityOfPage': f'https://calculalotuyo.es/{a["slug"]}', 'inLanguage': 'es-ES', 'articleSection': a['tema'],
        'author': {'@type': 'Organization', 'name': 'CalculaLoTuyo', 'url': 'https://calculalotuyo.es/sobre-el-proyecto'},
        'publisher': {'@type': 'Organization', 'name': 'CalculaLoTuyo', 'logo': {'@type': 'ImageObject', 'url': 'https://calculalotuyo.es/logo-512.png'}}},
        ensure_ascii=False, indent=1)

def cabeza_extra(s, a, img):
    """Marcado de noticia, imagen grande para Discover y enlace al RSS (se añaden al <head> de la página generada)."""
    extra = (f'    <meta name="robots" content="max-image-preview:large">\n    <meta property="article:published_time" content="{a["fecha"]}T09:00:00+02:00">\n'
             f'    <meta property="article:modified_time" content="{a["actualizado"]}T09:00:00+02:00">\n'
             f'    <link rel="alternate" type="application/rss+xml" title="Novedades de CalculaLoTuyo" href="https://calculalotuyo.es/feed.xml">\n'
             f'    <script type="application/ld+json">\n{marcado(a, img)}\n    </script>\n')
    s = s.replace('</head>', extra + '</head>', 1)
    return s.replace('https://calculalotuyo.es/og-image.png', img)                          # su propia imagen al compartir

for a in ARTICULOS:
    img = imagen(a)
    fecha_txt = f'📅 Publicado el {larga(a["fecha"])}' + (f' · actualizado el {larga(a["actualizado"])}' if a['actualizado'] != a['fecha'] else '')
    botones = ''.join(f'<a href="{h}" class="btn">{t}</a>' for h, t in a['calculadoras'])
    cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📰 Novedades · {a["tema"]}</div><h1>{a["h1"]}<br><span class="highlight">{a["sub"]}</span></h1>
            {CAJA_RESUMEN(a["resumen"])}
            <p class="hero-meta">{fecha_txt} · ✍️ <a href="sobre-el-proyecto">CalculaLoTuyo</a></p></div></section>

    <section class="section"><div class="container"><article class="seo-section novedad">
{a["cuerpo"]()}
<h2>🧮 Calcula cómo te afecta</h2>
<div class="novedad-botones">{botones}</div>
<p class="nota-corta">Información neutral basada en las normas y los datos oficiales citados. No opinamos sobre las medidas: contamos qué dicen y a quién afectan. <a href="novedades">Más novedades</a>.</p>
</article></div></section>
'''
    pagina(a['slug'], a['titulo'], a['desc'], a['kw'], [('Novedades', 'novedades'), (a['titulo'], None)], cuerpo, a['faqs'], a['fuentes'])
    f = os.path.join(RAIZ, a['slug'] + '.html')
    texto = cabeza_extra(open(f, encoding='utf-8').read(), a, img)          # primero se lee (abrir para escribir lo vaciaría)
    open(f, 'w', encoding='utf-8').write(texto)

# ---- Portada de Novedades
tarjetas = ''.join(f'''<a href="{a["slug"]}" class="novedad-tarjeta"><span class="novedad-meta">{a["tema"]} · {larga(a["fecha"])}</span><strong>{a["titulo"]}</strong><span>{a["desc"]}</span><span class="novedad-leer">Leer {FLECHA}</span></a>''' for a in ARTICULOS)
cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">📰 Actualidad</div><h1>Novedades<br><span class="highlight">lo que cambia en tu sueldo, tu paro y tus impuestos</span></h1><p>Las noticias que afectan a tu bolsillo, explicadas fácil y con la fuente oficial. Sin opiniones: qué ha pasado, qué cambia para ti y cómo calcularlo.</p></div></section>
    <section class="section"><div class="container"><div class="novedades-lista">{tarjetas}</div>
    <p class="nota-corta" style="margin-top:24px">Síguelas también por <a href="feed.xml">RSS</a>.</p></div></section>
'''
pagina('novedades', 'Novedades laborales y fiscales 2026 explicadas fácil', 'Lo que cambia en tu sueldo, tu paro, tus impuestos y tu pensión, explicado fácil y con la fuente oficial: pensiones 2027, IPC, deducciones en la renta y más.',
       'novedades laborales, noticias sueldo, pensiones 2027, ipc 2026, renta 2026', [('Novedades', None)], cuerpo,
       [('¿Qué son las Novedades de CalculaLoTuyo?', 'Artículos breves sobre cambios que afectan a tu sueldo, tu paro, tus impuestos o tu pensión, con la fuente oficial y una calculadora para ver cómo te afectan.')],
       'BOE, INE, Seguridad Social y Agencia Tributaria, citados en cada artículo.')
f = os.path.join(RAIZ, 'novedades.html')
s = open(f, encoding='utf-8').read().replace('</head>', '    <link rel="alternate" type="application/rss+xml" title="Novedades de CalculaLoTuyo" href="https://calculalotuyo.es/feed.xml">\n</head>', 1)
open(f, 'w', encoding='utf-8').write(s)

# ---- RSS (lectores de noticias y agregadores)
rfc = lambda f: dt.datetime.strptime(f, '%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 +0200')
items = ''.join(f'''  <item><title>{H.escape(a["titulo"])}</title><link>https://calculalotuyo.es/{a["slug"]}</link><guid>https://calculalotuyo.es/{a["slug"]}</guid><pubDate>{rfc(a["fecha"])}</pubDate><category>{a["tema"]}</category><description>{H.escape(a["desc"])}</description></item>
''' for a in ARTICULOS)
open(os.path.join(RAIZ, 'feed.xml'), 'w', encoding='utf-8').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Novedades de CalculaLoTuyo</title><link>https://calculalotuyo.es/novedades</link>
  <description>Lo que cambia en tu sueldo, tu paro, tus impuestos y tu pensión, con la fuente oficial.</description><language>es-es</language>
{items}</channel></rss>
''')
# ---- Bloque «Novedades» en la portada y en Guías (las 3 últimas), entre marcas para poder rehacerlo
import re
def poner_bloque(archivo, html, antes_de=None, despues_de=None):
    ruta = os.path.join(RAIZ, archivo); s = open(ruta, encoding='utf-8').read()
    bloque = f'<!-- NOVEDADES -->\n{html}\n<!-- /NOVEDADES -->\n'
    if '<!-- NOVEDADES -->' in s: s = re.sub(r'<!-- NOVEDADES -->.*?<!-- /NOVEDADES -->\n', lambda m: bloque, s, flags=re.S)
    elif antes_de: i = s.index(antes_de); s = s[:i] + bloque + s[i:]
    else: i = s.index(despues_de) + len(despues_de); s = s[:i] + '\n' + bloque + s[i:]
    open(ruta, 'w', encoding='utf-8').write(s)
mini = ''.join(f'<a href="{a["slug"]}" class="novedad-tarjeta"><span class="novedad-meta">{a["tema"]} · {larga(a["fecha"])}</span><strong>{a["titulo"]}</strong><span class="novedad-leer">Leer {FLECHA}</span></a>' for a in ARTICULOS[:3])
bloque = f'''    <section class="section-flat" id="novedades-portada"><div class="container">
            <h2 class="bloque-titulo">📰 Novedades</h2>
            <p class="bloque-desc">Lo que cambia en tu sueldo, tu paro y tus impuestos, con la fuente oficial</p>
            <div class="novedades-lista">{mini}</div>
            <a href="novedades" class="calc-group-guide">Ver todas las novedades →</a>
    </div></section>'''
poner_bloque('index.html', bloque, antes_de='    <!-- GUÍAS Y MODELOS')
poner_bloque('guias.html', bloque, despues_de='</section>')            # justo después de la cabecera de Guías

json.dump([{k: a[k] for k in ('slug', 'titulo', 'desc', 'fecha', 'actualizado', 'tema')} for a in ARTICULOS], open(os.path.join(AQUI, 'lista.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('novedades:', len(ARTICULOS), 'artículos · pensiones 2027 ≈', pc(CENTRAL, 2), '· deducción alquiler 25.000 € ≈', e(ded(21375.0)), '€')
