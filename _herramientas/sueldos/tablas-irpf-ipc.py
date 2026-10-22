# Mejora las páginas de IRPF y subida del IPC para las búsquedas que ya les dan impresiones en Google
# («calculadora irpf», «qué irpf me corresponde», «calcular subida ipc nómina», «subida ipc salarios 2026»):
#   · título, descripción y H1 con esas palabras
#   · una tabla ya calculada (retención según el sueldo / subida según el sueldo)
#   · dos preguntas frecuentes más (en el HTML y en el marcado para Google)
# Las tablas salen de sueldos.json (mismo motor que la calculadora) y de DATOS.ipc: en enero se rehacen solas.
# Se puede lanzar las veces que haga falta (lo hace regenerar.sh). Uso: python3 _herramientas/sueldos/tablas-irpf-ipc.py
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import e, RAIZ

D = json.load(open(os.path.join(AQUI, 'sueldos.json')))['datos']
datos_js = open(os.path.join(RAIZ, 'datos-2026.js'), encoding='utf-8').read()
ipc = dict((int(a), float(b)) for a, b in re.findall(r'(\d{4}):([\d.]+)', re.search(r'ipc:\{([^}]*)\}', datos_js).group(1)))
ANIO_IPC = max(ipc); IPC = ipc[ANIO_IPC]                              # último IPC de diciembre publicado (2025: 2,9 %)
SMI = 17094
SUELDOS = [SMI, 18000, 20000, 22000, 25000, 28000, 30000, 35000, 40000, 45000, 50000, 60000]
pc = lambda x: f'{x:.2f}'.replace('.', ',') + ' %'
FLECHA = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
limpio = lambda t: re.sub(r'<[^>]+>', '', t)

def poner_bloque(s, marca, html, antes_de):
    """Pone (o sustituye) el bloque entre <!-- marca --> y <!-- /marca --> justo antes de «antes_de»."""
    bloque = f'<!-- {marca} -->\n{html}\n<!-- /{marca} -->\n'
    if f'<!-- {marca} -->' in s:
        return re.sub(rf'<!-- {marca} -->.*?<!-- /{marca} -->\n', lambda m: bloque, s, flags=re.S)
    i = s.index(antes_de)
    return s[:i] + bloque + s[i:]

def poner_faqs(s, faqs):
    """Añade preguntas al acordeón y al JSON-LD FAQPage, si aún no están."""
    for q, a in faqs:
        if q in s: continue
        item = f'<div class="faq-item"><button class="faq-q"><span>{q}</span>{FLECHA}</button><div class="faq-a"><p>{a}</p></div></div>\n'
        s = s.replace('<div class="faq-list">', '<div class="faq-list">\n' + item, 1)            # la primera de la lista
        ld = json.dumps({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': limpio(a)}}, ensure_ascii=False)
        s = s.replace('"mainEntity": [', '"mainEntity": [\n  ' + ld + ',', 1)
    return s

def cabecera(s, titulo, desc, h1):
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\g<1>{titulo}', s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', rf'\g<1>{titulo}', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', rf'\g<1>{desc}', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', rf'\g<1>{desc}', s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', rf'\g<1>{desc}', s, count=1)
    s = re.sub(r'("@type": "WebApplication",\s*"name": ")[^"]*(",\s*"url": "[^"]*",\s*"description": ")[^"]*', rf'\g<1>{titulo}\g<2>{desc}', s, count=1)
    return re.sub(r'<h1>.*?</h1>', h1, s, count=1, flags=re.S)

# ================================================================ IRPF
f = os.path.join(RAIZ, 'irpf.html'); s = open(f, encoding='utf-8').read()
t30 = D['30000']['base']['tipo']
s = cabecera(s, 'Calculadora IRPF 2026: calcula la retención de tu nómina',
    f'Calcula qué IRPF te corresponde en 2026 con el mismo algoritmo que Hacienda. Con 30.000 € brutos, un {pc(t30)}. Tabla de retención por sueldo e hijos.',
    '<h1>Calculadora de IRPF 2026<br><span class="highlight">¿qué retención te corresponde?</span></h1>')
filas = ''.join(f'<tr><td>{e(b)} €{" (SMI)" if b == SMI else ""}</td><td><strong>{pc(D[str(b)]["base"]["tipo"])}</strong></td><td>{pc(D[str(b)]["hijo1"]["tipo"])}</td><td>{pc(D[str(b)]["hijos2"]["tipo"])}</td><td>{e(D[str(b)]["base"]["irpf"] / 12)} €</td></tr>' for b in SUELDOS)
tabla = f'''    <section class="section"><div class="container"><article class="seo-section">
<h2>📊 ¿Qué IRPF me corresponde? Retención según tu sueldo (2026)</h2>
<p>El porcentaje que te retienen en la nómina depende sobre todo de tu sueldo bruto al año y de tus hijos. Así queda en 2026, calculado con el <strong>mismo algoritmo que usa la Agencia Tributaria</strong> (el de su calculadora de retenciones):</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Sueldo bruto al año</th><th>Sin hijos</th><th>1 hijo</th><th>2 hijos</th><th>IRPF al mes (sin hijos, 12 pagas)</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota-corta">Contrato indefinido y menor de 65 años. Con hijos, el mínimo por descendientes se reparte con el otro progenitor (lo habitual). Para tu caso exacto, usa la calculadora de arriba.</p>
<h3>Cómo saber qué IRPF te corresponde</h3>
<ol><li>Busca tu <strong>sueldo bruto al año</strong>, con las pagas extra (en la nómina: el bruto del mes × 12 o × 14).</li><li>Mira la fila de tu sueldo en la tabla, o pon tus datos en la calculadora para tener en cuenta tu situación familiar, discapacidad o tu edad.</li><li>Compara con el porcentaje de IRPF de tu nómina. Si te retienen menos, en la <a href="obligado-a-declarar-renta">declaración de la renta</a> te puede salir a pagar; si te retienen más, a devolver. Puedes pedir a tu empresa que te suba el porcentaje (modelo 145).</li></ol>
</article></div></section>
'''
s = poner_bloque(s, 'TABLA-IRPF', tabla, '    <div class="container"><div class="ad"></div></div>\n\n    <!-- EJEMPLO PRÁCTICO -->')
s = poner_faqs(s, [
    ('¿Cómo sé qué IRPF me corresponde?', f'Depende de tu sueldo bruto anual, tus hijos y tu situación familiar. Como referencia, en 2026 y sin hijos: un <strong>{pc(D["20000"]["base"]["tipo"])}</strong> con 20.000 €, un <strong>{pc(t30)}</strong> con 30.000 € y un <strong>{pc(D["40000"]["base"]["tipo"])}</strong> con 40.000 €. Para tu caso exacto, usa la calculadora.'),
    ('¿Cuánto IRPF me quitan con 30.000 € brutos?', f'Un <strong>{pc(t30)}</strong> en 2026 si no tienes hijos: unos <strong>{e(D["30000"]["base"]["irpf"])} € al año</strong> ({e(D["30000"]["base"]["irpf"] / 12)} € al mes en 12 pagas). Con un hijo, un {pc(D["30000"]["hijo1"]["tipo"])}.'),
])
open(f, 'w', encoding='utf-8').write(s)

# ================================================================ SUBIDA DEL IPC
f = os.path.join(RAIZ, 'subida-ipc.html'); s = open(f, encoding='utf-8').read()
nuevo = lambda b: b * (1 + IPC / 100)
ipc_txt = f'{IPC:g}'.replace('.', ',') + ' %'                       # «2,9 %»
factor = f'{1 + IPC / 100:.3f}'.replace('.', ',')                   # «1,029»
s = cabecera(s, f'Subida salarial IPC {ANIO_IPC + 1}: calcula cuánto sube tu nómina',
    f'Calcula cuánto debe subir tu nómina con el IPC: con el {ipc_txt} de {ANIO_IPC}, 28.000 € pasan a {e(nuevo(28000))} €. Tabla por sueldo y cómo negociar la subida salarial.',
    f'<h1>Calcula la subida del IPC en tu nómina<br><span class="highlight">¿cuánto debería subir tu sueldo en {ANIO_IPC + 1}?</span></h1>')
filas = ''.join(f'<tr><td>{e(b)} €</td><td><strong>{e(nuevo(b))} €</strong></td><td>+{e(nuevo(b) - b)} €</td><td>+{e((nuevo(b) - b) / 14)} €</td><td>+{e((nuevo(b) - b) / 12)} €</td></tr>' for b in [18000, 20000, 22000, 25000, 28000, 30000, 35000, 40000, 45000, 50000])
tabla = f'''<!-- tabla de subida con el último IPC -->
<h2>📋 Tu subida con el IPC de {ANIO_IPC} ({ipc_txt})</h2>
<p>Para no perder poder de compra en {ANIO_IPC + 1}, tu sueldo bruto tendría que subir un <strong>{ipc_txt}</strong>, el IPC de diciembre de {ANIO_IPC} (INE). Así queda cada sueldo:</p>
<div class="tabla-wrap"><table class="tabla-festivos tabla-sueldos"><thead><tr><th>Sueldo bruto al año</th><th>Con la subida</th><th>Al año</th><th>Al mes (14 pagas)</th><th>Al mes (12 pagas)</th></tr></thead><tbody>{filas}</tbody></table></div>
<p><strong>Cómo calcularlo a mano:</strong> multiplica tu sueldo bruto por {factor}. Por ejemplo, 28.000 € × {factor} = {e(nuevo(28000))} €. En la nómina de cada mes lo notarás en el salario base y los complementos que suban por convenio; el neto sube algo menos, porque una parte se va en IRPF y Seguridad Social (mírala en la <a href="sueldo-neto">calculadora de sueldo neto</a>).</p>
'''
s = poner_bloque(s, 'TABLA-IPC', tabla, '<h2><svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-file-text"/></svg> Cómo suben los sueldos en la práctica</h2>')
s = poner_faqs(s, [
    (f'¿Cuánto me sube la nómina con el IPC de {ANIO_IPC}?', f'Un <strong>{ipc_txt}</strong> del bruto si tu convenio o tu contrato lo actualizan con el IPC. Con 28.000 € brutos al año, son {e(nuevo(28000) - 28000)} € más al año, unos {e((nuevo(28000) - 28000) / 14)} € al mes en 14 pagas.'),
    (f'¿Cuál será el IPC de {ANIO_IPC + 1}?', f'El INE publica el dato adelantado de diciembre a finales de ese mes y el definitivo a mediados de enero de {ANIO_IPC + 2}. Es el que usan muchos convenios para la revisión salarial; hasta entonces, la referencia es el {ipc_txt} de {ANIO_IPC}.'),
])
open(f, 'w', encoding='utf-8').write(s)
print(f'irpf y subida-ipc actualizadas · IPC {ANIO_IPC}: {ipc_txt} · retención 30.000 €: {pc(t30)}')
