# Genera «Calendario laboral 2027 de <ciudad>» SOLO para las ciudades con fiestas locales publicadas
# en su boletín oficial (estado "publicado" en fiestas-locales-2027.json). Reutiliza el calendario,
# los puentes y la plantilla de gen-seo.py. Uso: python3 _herramientas/calendario/gen-ciudades.py [json]
import json, os, re, sys, unicodedata
AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_ARG = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None   # se calcula antes de cambiar de carpeta
fuente_gen = open(os.path.join(AQUI, 'gen-seo.py'), encoding='utf-8').read()
corte = fuente_gen.index('# ================================================================ 1) PÁGINA PRINCIPAL')
exec(fuente_gen[:corte])                              # carga datos del BOE, puentes(), calendario(), pagina()… sin generar nada

RUTA = RUTA_ARG or os.path.join(AQUI, 'fiestas-locales-2027.json')
datos = json.load(open(RUTA, encoding='utf-8'))
slugify = lambda t: re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFD', t.lower()).encode('ascii', 'ignore').decode()).strip('-')
publicadas = [c for c in datos['ciudades'] if c.get('estado') == 'publicado' and len(c.get('fiestas', [])) >= 1 and c.get('url') and c['ccaa'] not in ('ceuta', 'melilla')]   # en Ceuta y Melilla la ciudad es la comunidad: sus fiestas locales van en esa página

def slug_ciudad(c):
    s = slugify(c['ciudad'])
    return f'calendario-laboral-2027-{s}-ciudad' if s in CCAA else f'calendario-laboral-2027-{s}'   # «Madrid» ciudad ≠ Comunidad de Madrid

paginas = {}
for c in publicadas:
    cc = CCAA[c['ccaa']]; ciudad = c['ciudad']; sl = slug_ciudad(c)
    locales = {f: n for f, n in c['fiestas']}
    fest = dict(cc['festivos']); fest.update(locales)          # festivos de la comunidad + los 2 locales
    ps = puentes(fest)
    lab = [laborables_mes(fest, m) for m in range(1, 13)]
    finde_local = [f for f in locales if fecha(f).weekday() >= 5]
    tipo = lambda k: f'Local de {ciudad}' if k in locales else ('Propio de ' + CORTO[c['ccaa']] if k in cc['propios'] else 'Nacional')
    filas = ''.join(f'<tr{" class=fila-local" if k in locales else ""}><td>{cap(larga(fecha(k)))}</td><td>{H.escape(n)}</td><td>{tipo(k)}</td></tr>' for k, n in sorted(fest.items()))
    lista_loc = ' y '.join(f'{H.escape(n)} ({larga(fecha(k))})' for k, n in sorted(locales.items()))
    hermanas = [o for o in publicadas if o['ccaa'] == c['ccaa'] and o is not c]
    otras = ''.join(f'<a href="{slug_ciudad(o)}">{o["ciudad"]}</a>' for o in hermanas)
    nota_finde = f' Ojo: {"la fiesta local cae" if len(finde_local) == 1 else "las fiestas locales caen"} en fin de semana, así que no se notan en el calendario laboral.' if finde_local else ''
    mejor = max((p for p in ps if p['coger']), key=lambda p: (p['dias'] / len(p['coger']), p['dias']), default=None)
    cuerpo = hero('', f'Calendario laboral 2027 {ciudad}', 'festivos locales y puentes', f'Los {len(fest)} festivos de {ciudad} en 2027: los de {cc["nombre"]} y las fiestas locales del municipio, según su boletín oficial.') + f'''
    <section class="calc-section"><div class="container"><div class="card">
        {resumen([(len(fest), 'festivos'), (len(locales), 'locales de ' + ciudad), (sum(lab), 'días laborables*')])}
        <h2 class="puentes-titulo">🗓️ Calendario 2027 · {ciudad}</h2>
        {LEYENDA}
        {calendario(fest, {d.isoformat() for p in ps if len(p['coger']) == 1 for d in p['coger']})}
        <p class="nota-corta">* De lunes a viernes, ya descontadas las fiestas locales de {ciudad}.</p>
        <div class="result-actions"><a href="puentes-2027?ccaa={c['ccaa']}" class="btn">🏖️ Calcular mis puentes</a></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🎉 Fiestas locales de {ciudad} en 2027</h2>
<p>Las fiestas locales de {ciudad} en 2027 son <strong>{lista_loc}</strong>, según el {H.escape(c['fuente'])} (<a href="{H.escape(c['url'])}" target="_blank" rel="noopener">ver la publicación oficial</a>).{nota_finde} A ellas se suman los festivos de {cc["nombre"]}.</p>
<h2>📋 Todos los festivos de {ciudad} en 2027</h2>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Fecha</th><th>Festivo</th><th>Tipo</th></tr></thead><tbody>{filas}</tbody></table></div>
<h2>🏖️ Puentes de 2027 en {ciudad}</h2>
<p>{("El que más compensa: <strong>" + H.escape(mejor["nombre"]) + "</strong>, pidiendo " + str(len(mejor["coger"])) + (" día" if len(mejor["coger"]) == 1 else " días") + " de vacaciones para descansar " + str(mejor["dias"]) + " días seguidos.") if mejor else ""}</p>
{tarjetas([tarjeta(p, fest) for p in ps])}
<h2>💼 Días laborables por mes en {ciudad}</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Mes</th><th>Días laborables</th></tr></thead><tbody>{"".join(f"<tr><td>{cap(MESES[m])}</td><td>{lab[m]}</td></tr>" for m in range(12))}</tbody></table></div>
<p>Calendario de toda la comunidad: <a href="calendario-laboral-2027-{c['ccaa']}">calendario laboral 2027 de {cc["nombre"]}</a>.{(" Otras ciudades:</p><div class='enlaces-ccaa'>" + otras + "</div><p>") if otras else ""}</p>
</article></div></section>
'''
    faqs = [(f'¿Cuáles son las fiestas locales de {ciudad} en 2027?', f'{cap(lista_loc)}, según el {H.escape(c["fuente"])}.'),
            (f'¿Cuántos festivos hay en {ciudad} en 2027?', f'<strong>{len(fest)}</strong>: los {len(cc["festivos"])} de {cc["nombre"]} y {len(locales)} {"local" if len(locales) == 1 else "locales"}. {len(entre_semana(fest))} caen entre semana.'),
            (f'¿Cuántos días laborables tiene 2027 en {ciudad}?', f'<strong>{sum(lab)} días</strong> de lunes a viernes, descontando todos los festivos.')]
    fuente = FUENTE_BOE + f' Fiestas locales: {H.escape(c["fuente"])} (<a href="{H.escape(c["url"])}" target="_blank" rel="noopener">enlace</a>).'
    paginas[sl] = (ciudad, c['ccaa'])
    titulo = f'Calendario laboral 2027 {ciudad}: festivos locales y puentes'
    if len(titulo) > 60: titulo = f'Calendario laboral 2027 {ciudad}: festivos'   # que Google no lo corte
    pagina(sl, titulo, f'Festivos de {ciudad} en 2027: las fiestas locales oficiales, los festivos de {cc["nombre"]}, los puentes y los días laborables de cada mes.',
           f'calendario laboral 2027 {ciudad.lower()}, festivos {ciudad.lower()} 2027, fiestas locales {ciudad.lower()} 2027, puentes 2027 {ciudad.lower()}',
           ciudad, cuerpo, faqs, fuente)
json.dump(paginas, open(os.path.join(AQUI, 'ciudades-generadas.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(paginas), 'ciudades generadas ·', len(datos['ciudades']) - len(publicadas), 'pendientes')
