# Calendarios de ciudades fuera del índice de Google (05/11/2026), mientras AdSense revisa la web.
# Son ~35 páginas casi iguales (solo cambian dos fiestas locales) y Google puede verlas como contenido hecho en masa.
# Siguen en la web y se llega a ellas desde el calendario de su comunidad; solo Google deja de contarlas:
#   · <meta name="robots" content="noindex, follow"> (follow: Google sigue los enlaces de la página)
#   · fuera del sitemap
# PARA VOLVER A INDEXARLAS (cuando AdSense apruebe la web): quitar esta línea de regenerar.sh y lanzar regenerar.sh.
# Uso: python3 _herramientas/calendario/noindex-ciudades.py      (regenerar.sh lo lanza después de los generadores)
import json, os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..', '..')
ciudades = json.load(open(os.path.join(AQUI, 'ciudades-generadas.json'), encoding='utf-8'))   # las páginas que crea gen-ciudades.py
META = '<meta name="robots" content="noindex, follow">'

cambiadas = 0
for slug in ciudades:
    f = os.path.join(RAIZ, f'{slug}.html')
    if not os.path.exists(f): continue
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'<meta name="robots" content="[^"]*">', META, s, count=1)           # cambia el que hubiera
    if META not in s: s = s.replace('<meta name="viewport"', META + '\n    <meta name="viewport"', 1)   # o lo pone
    if s != o: open(f, 'w', encoding='utf-8').write(s); cambiadas += 1

sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
for slug in ciudades:
    s = re.sub(rf'\s*<url><loc>https://calculalotuyo\.es/{re.escape(slug)}</loc>.*?</url>', '', s)
open(sm, 'w', encoding='utf-8').write(s)
print(f'calendarios de ciudades sin indexar: {len(ciudades)} (cambiadas {cambiadas}) · sitemap: {s.count("<loc>")} URLs')
