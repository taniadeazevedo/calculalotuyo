# Páginas de plantilla consolidadas en sus tablas (24/10/2026, tras el rechazo de AdSense por posible «contenido de poco valor»).
# Muchas páginas casi iguales (solo cambia la cifra) pesan en contra. Las que se quitan:
#   · ya no las crean los generadores (sus listas PAGINAS son más cortas)
#   · su dirección antigua no da error: es una página mínima que lleva a la tabla (sin índice para Google)
#   · salen del sitemap y del buscador
# Para recuperar una página: añadirla otra vez a la lista PAGINAS de su generador y quitarla de aquí.
# Uso: python3 _herramientas/consolidar.py      (regenerar.sh lo lanza después de los generadores)
import glob, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

# Página quitada → (tabla a la que lleva, nombre de la tabla)
TABLA_SUELDOS = ('sueldo-bruto-a-neto-2026', 'la tabla de sueldo bruto a neto 2026')
TABLA_PARO = ('tabla-paro-2026', 'la tabla del paro 2026')
TABLA_DESPIDO = ('tabla-indemnizacion-despido', 'la tabla de indemnización por despido')
SUELDOS_QUE_QUEDAN = {18000, 20000, 22000, 24000, 25000, 28000, 30000, 35000, 40000, 45000, 50000, 60000}   # = PAGINAS de gen-sueldos.py

DESTINO = {}
for f in glob.glob('*-euros-brutos-en-netos.html'):                     # sueldos que ya no tienen página propia
    if int(f.split('-')[0]) not in SUELDOS_QUE_QUEDAN: DESTINO[f[:-5]] = TABLA_SUELDOS
for f in glob.glob('paro-con-*-euros.html'): DESTINO[f[:-5]] = TABLA_PARO               # todas las de «paro con X €»
for f in glob.glob('indemnizacion-despido-*-ano*.html'): DESTINO[f[:-5]] = TABLA_DESPIDO   # todas las de «X años»

def pagina_traslado(destino, nombre):
    """Página mínima: lleva al momento a la tabla y le dice a Google que no la guarde (y cuál es la buena)."""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Esta página está ahora en {nombre}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://calculalotuyo.es/{destino}">
<meta http-equiv="refresh" content="0; url=/{destino}">
</head>
<body>
<p>Esta página se ha unido a <a href="/{destino}">{nombre}</a>, con todas las cifras juntas.</p>
</body>
</html>
'''

for slug, (destino, nombre) in DESTINO.items():
    open(f'{slug}.html', 'w', encoding='utf-8').write(pagina_traslado(destino, nombre))

# Fuera del sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
for slug in DESTINO:
    sm = re.sub(rf'\s*<url><loc>https://calculalotuyo\.es/{re.escape(slug)}</loc>.*?</url>', '', sm)
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('consolidadas:', len(DESTINO), 'páginas → tablas · sitemap:', sm.count('<loc>'), 'URLs')

# Enlaces a las páginas quitadas → a su tabla; y las listas de cifras que solo llevaban a esas páginas, fuera
def enlace_a_tabla(m):
    return f'href="{DESTINO[m.group(1)][0]}"'
patron = re.compile(r'href="/?(' + '|'.join(re.escape(x) for x in sorted(DESTINO, key=len, reverse=True)) + r')"')
cambiadas = 0
for f in glob.glob('*.html'):
    s = o = open(f, encoding='utf-8').read()
    if 'noindex' in s: continue                                         # las propias páginas de traslado
    # listas «1 año · 2 años…» o «1.300 € · 1.400 €…» cuyos enlaces son todos a páginas quitadas
    s = re.sub(r'<div class="enlaces-sueldo">((?:<a href="/?(?:' + '|'.join(re.escape(x) for x in DESTINO) + r')">[^<]*</a>)+)</div>\n?', '', s)
    s = patron.sub(enlace_a_tabla, s)                                    # el resto de enlaces sueltos, a la tabla
    if s != o: open(f, 'w', encoding='utf-8').write(s); cambiadas += 1
t = open('llms.txt', encoding='utf-8').read()
t2 = re.sub(r'calculalotuyo\.es/(' + '|'.join(re.escape(x) for x in DESTINO) + r')\b', lambda m: 'calculalotuyo.es/' + DESTINO[m.group(1)][0], t)
if t2 != t: open('llms.txt', 'w', encoding='utf-8').write(t2)
print('enlaces cambiados a las tablas en', cambiadas, 'páginas')
