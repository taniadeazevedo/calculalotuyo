# Tablas que se deslizan en el móvil (02/11/2026): las tablas «info-table» y «doc-tabla» no tenían caja con
# desplazamiento, así que en pantallas estrechas se cortaban y no se podía ver la parte derecha.
# Este paso mete cada una en <div class="tabla-scroll"> (si no lo está ya). Se puede lanzar las veces que haga falta.
# Uso: python3 _herramientas/tablas.py      (regenerar.sh lo lanza después de los iconos)
import glob, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

TABLA = re.compile(r'(<div class="tabla-scroll">)?(<table class="(?:info-table|doc-tabla)[^"]*">.*?</table>)', re.S)
def envolver(m):
    if m.group(1): return m.group(0)                                    # ya estaba dentro de la caja: igual
    return '<div class="tabla-scroll">' + m.group(2) + '</div>'
cambiadas = 0
for f in glob.glob('*.html'):
    s = open(f, encoding='utf-8').read()
    n = TABLA.sub(envolver, s)
    if n != s: open(f, 'w', encoding='utf-8').write(n); cambiadas += 1
print('tablas deslizables: páginas cambiadas', cambiadas)
