import glob, json, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(S, '..', '..'))   # la raíz de la web (dos carpetas por encima de este script)
r = lambda n: open(f'{S}/{n}', encoding='utf-8').read()

# ---- 1) Menú: "Puentes 2027" debajo de "Días laborables" en todas las páginas
for f in glob.glob('*.html'):
    s = open(f, encoding='utf-8').read()
    if 'noindex' in s and 'nav-link' not in s: continue   # páginas de traslado (consolidar.py): sin menú
    if 'puentes-2027"' not in s:
        p = '/' if f == '404.html' else ''
        a = f'<a href="{p}dias-laborables"'
        esc = re.search(re.escape(a) + r'( aria-current="page")?>📅 Días laborables</a>', s)
        mov = re.search(re.escape(a) + r' class="mobile-nav-link"( aria-current="page")?>📅 Días laborables</a>', s)
        assert esc and mov, f
        s = s[:mov.end()] + f'\n            <a href="{p}puentes-2027" class="mobile-nav-link">🗓️ Puentes 2027</a>' + s[mov.end():]
        s = s[:esc.end()] + f'\n                    <a href="{p}puentes-2027">🗓️ Puentes 2027</a>' + s[esc.end():]
    s = s.replace('styles.css?v=20261018a', 'styles.css?v=20261018b')
    open(f, 'w', encoding='utf-8').write(s)

# ---- 2) Tabla de festivos propios de cada comunidad (HTML estático, bueno para Google)
d = json.load(open(f'{S}/boe/f2027.json'))
nombres = {'Com. de Madrid': 'Comunidad de Madrid', 'Región Murcia': 'Región de Murcia', 'C. Foral Navarra': 'Navarra', 'Ciudad de Ceuta': 'Ceuta', 'Ciudad de Melilla': 'Melilla'}
limpio = {'Lunes siguiente a asunción de la Virgen': 'Lunes siguiente al 15 de agosto', 'Aniversario 1er Gobierno Euskadi': 'Aniversario del primer Gobierno Vasco', 'Sustitución 15 de agosto': 'Sustituye al 15 de agosto'}
comunes = {'01-01', '01-06', '03-26', '05-01', '10-12', '11-01', '12-06', '12-08', '12-25'}
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
filas = []
for k in sorted(d, key=lambda x: nombres.get(x, x)):
    items = [f'{limpio.get(n, n)} ({int(f[8:])} de {meses[int(f[5:7]) - 1]})' for f, n, _ in d[k] if f[5:] not in comunes]
    if k == 'Canarias':
        items.append('fiesta de cada isla')
    slug = {'Andalucía': 'andalucia', 'Aragón': 'aragon', 'Asturias': 'asturias', 'Illes Balears': 'baleares', 'Canarias': 'canarias', 'Cantabria': 'cantabria', 'Castilla-La Mancha': 'castilla-la-mancha', 'Castilla y León': 'castilla-y-leon', 'Cataluña': 'cataluna', 'Extremadura': 'extremadura', 'Galicia': 'galicia', 'Com. de Madrid': 'madrid', 'Región Murcia': 'murcia', 'C. Foral Navarra': 'navarra', 'País Vasco': 'pais-vasco', 'La Rioja': 'la-rioja', 'Comunitat Valenciana': 'valencia', 'Ciudad de Ceuta': 'ceuta', 'Ciudad de Melilla': 'melilla'}[k]
    filas.append(f'<tr><td><a href="calendario-laboral-2027-{slug}">{nombres.get(k, k)}</a></td><td>{"; ".join(items)}</td></tr>')

# ---- 3) Página nueva, con el menú y el pie de vacaciones.html
v = open('vacaciones.html', encoding='utf-8').read()
nav = v[v.index('<body>') + len('<body>\n'):v.index('<main')]
nav = nav.replace(' aria-current="page"', '').replace('class="nav-link active" data-dropdown-btn>Nómina', 'class="nav-link" data-dropdown-btn>Nómina')
nav = nav.replace('class="nav-link" data-dropdown-btn>📅 Calendario', 'class="nav-link active" data-dropdown-btn>📅 Calendario')
nav = nav.replace('<a href="puentes-2027">', '<a href="puentes-2027" aria-current="page">')
nav = nav.replace('<a href="puentes-2027" class="mobile-nav-link">', '<a href="puentes-2027" class="mobile-nav-link" aria-current="page">')
foot = v[v.index('<footer'):v.index('<script src="site.js')]
# ---- Tarjetas de los grandes puentes (mismo dibujo que las de la calculadora)
import datetime as dt
def tarjeta(nombre, ini, fin, festivos, coger, nota=''):
    d0 = dt.date.fromisoformat(ini); d1 = dt.date.fromisoformat(fin)
    dias = (d1 - d0).days + 1
    tira = ''
    for i in range(dias):
        d = d0 + dt.timedelta(days=i); k = d.isoformat()
        clase = 'cal-festivo' if k in festivos else 'cal-puente' if k in coger else 'cal-finde'
        tira += f'<span class="tira-dia {clase}"><small>{"LMXJVSD"[d.weekday()]}</small>{d.day}</span>'
    pides = f'Si pides <strong>{len(coger)} {"día" if len(coger) == 1 else "días"}</strong> de vacaciones' if coger else '<strong>Sin gastar vacaciones</strong>'
    extra = f'<p class="puente-nota">{nota}</p>' if nota else ''
    gratis = '' if coger else ' puente-gratis'
    return f'<div class="puente{gratis}"><div class="puente-dias"><strong>{dias}</strong><span>días libres</span></div><div class="puente-info"><p class="puente-nombre">{nombre}</p><p>{pides}</p>{extra}</div><div class="tira">{tira}</div></div>'
grandes = [
    tarjeta('Año Nuevo y Reyes', '2027-01-01', '2027-01-06', {'2027-01-01', '2027-01-06'}, {'2027-01-04', '2027-01-05'}),
    tarjeta('Semana Santa', '2027-03-25', '2027-03-28', {'2027-03-25', '2027-03-26'}, set(), 'En 6 comunidades el lunes 29 también es festivo'),
    tarjeta('Fiesta Nacional', '2027-10-09', '2027-10-12', {'2027-10-12'}, {'2027-10-11'}),
    tarjeta('Todos los Santos', '2027-10-30', '2027-11-01', {'2027-11-01'}, set()),
    tarjeta('Constitución e Inmaculada', '2027-12-04', '2027-12-12', {'2027-12-06', '2027-12-08'}, {'2027-12-07', '2027-12-09', '2027-12-10'}, 'El mejor puente del año'),
]
main = r('p-main.html').replace('{{TABLA}}', '\n'.join(filas)).replace('{{GRANDES}}', '<div class="puentes-lista">' + ''.join(grandes) + '</div>')
open('puentes-2027.html', 'w', encoding='utf-8').write(r('p-head.html') + nav + main + '\n' + foot + r('p-script.html'))

# ---- 4) Portada: segunda fila en el apartado Calendario
s = open('index.html', encoding='utf-8').read()
if 'href="puentes-2027" class="calc-item"' not in s:
    fila = '''                    <a href="puentes-2027" class="calc-item">
                        <div class="calc-item-info">
                            <h3>Puentes 2027 por comunidad</h3>
                            <p>Festivos oficiales del BOE · Días puente para enlazar · Calendario anual</p>
                        </div>
                        <svg class="calc-item-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
                    </a>
'''
    ancla = '<a href="dias-laborables" class="calc-item">'
    assert s.count(ancla) == 1
    s = s.replace(ancla, fila.lstrip() + '                    ' + ancla)
    open('index.html', 'w', encoding='utf-8').write(s)

# ---- 5) Días laborables: el Real Decreto vuelve a llevar enlace (ahora con el identificador correcto)
s = open('dias-laborables.html', encoding='utf-8').read()
s = s.replace('art. 45 del Real Decreto 2001/1983', 'art. 45 del <a href="https://www.boe.es/buscar/act.php?id=BOE-A-1983-20906" target="_blank">Real Decreto 2001/1983</a>')
s = s.replace('<p>Si buscas cuántos días de vacaciones te quedan, usa la <a href="vacaciones">calculadora de vacaciones</a>.</p>',
              '<p>Si quieres ver los festivos de tu comunidad y cómo enlazarlos, mira los <a href="puentes-2027">puentes de 2027</a>. Si buscas cuántos días de vacaciones te quedan, usa la <a href="vacaciones">calculadora de vacaciones</a>.</p>')
open('dias-laborables.html', 'w', encoding='utf-8').write(s)

# ---- 6) Sitemap
x = open('sitemap.xml', encoding='utf-8').read()
if 'puentes-2027' not in x:
    x = x.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/puentes-2027</loc><lastmod>2026-10-18</lastmod><priority>0.9</priority></url>\n</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write(x)
print('ok')
