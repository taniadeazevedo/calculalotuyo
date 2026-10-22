# Pone al día la fecha <lastmod> de cada página del sitemap: el día del último cambio de ese archivo en git
# (o hoy, si tiene cambios sin guardar). Google usa esa fecha para saber qué páginas volver a visitar.
# Uso: python3 _herramientas/sitemap.py      (regenerar.sh ya lo lanza al final)
import datetime as dt, os, re, subprocess
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web
HOY = dt.date.today().isoformat()
pendientes = set(subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.split())   # archivos con cambios sin guardar

def fecha(archivo):
    if archivo in pendientes: return HOY
    f = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', archivo], capture_output=True, text=True).stdout.strip()
    return f or HOY                                                   # archivo nuevo, aún sin guardar en git

s = open('sitemap.xml', encoding='utf-8').read()
cambiadas = 0
def poner(m):
    global cambiadas
    pag = m.group(1) or 'index'
    nueva = fecha(pag + '.html')
    if nueva != m.group(2): cambiadas += 1
    return f'<loc>https://calculalotuyo.es/{m.group(1)}</loc><lastmod>{nueva}</lastmod>'
s = re.sub(r'<loc>https://calculalotuyo\.es/([^<]*)</loc><lastmod>([^<]*)</lastmod>', poner, s)
open('sitemap.xml', 'w', encoding='utf-8').write(s)
print('sitemap: fechas cambiadas en', cambiadas, 'páginas')
