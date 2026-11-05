# Páginas «X euros brutos en netos» fuera del índice de Google (05/11/2026), mientras AdSense revisa la web.
# Son 12 páginas con la misma plantilla (solo cambian las cifras) y casi sin visitas: Google puede verlas como contenido en serie.
# Siguen en la web (se llega desde la calculadora de sueldo neto); solo Google deja de contarlas:
#   · <meta name="robots" content="noindex, follow"> (follow: Google sigue los enlaces de la página)
#   · fuera del sitemap
# PARA VOLVER A INDEXARLAS (cuando AdSense apruebe la web): quitar esta línea de regenerar.sh y lanzar regenerar.sh.
# Uso: python3 _herramientas/sueldos/noindex-brutos.py      (regenerar.sh lo lanza después de los generadores)
import glob, os, re
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
META = '<meta name="robots" content="noindex, follow">'

paginas = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(RAIZ, '*-euros-brutos-en-netos.html')))   # «30000-euros-brutos-en-netos»…
cambiadas = 0
for slug in paginas:
    f = os.path.join(RAIZ, f'{slug}.html')
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'<meta name="robots" content="[^"]*">', META, s, count=1)           # cambia el que hubiera
    if META not in s: s = s.replace('<meta name="viewport"', META + '\n    <meta name="viewport"', 1)   # o lo pone
    if s != o: open(f, 'w', encoding='utf-8').write(s); cambiadas += 1

sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
for slug in paginas:
    s = re.sub(rf'\s*<url><loc>https://calculalotuyo\.es/{re.escape(slug)}</loc>.*?</url>', '', s)   # la quita del sitemap
open(sm, 'w', encoding='utf-8').write(s)
print(f'páginas de brutos en netos sin indexar: {len(paginas)} (cambiadas {cambiadas}) · sitemap: {s.count("<loc>")} URLs')
