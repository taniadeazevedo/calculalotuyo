# Poda temporal (17/11/2026): páginas débiles fuera del índice de Google para que la web parezca más sólida.
# Search Console: Google visitó las páginas buenas ya mejoradas (12/11) y aun así no las indexó. Juzga la web entera,
# y casi la mitad de lo que veía eran páginas casi iguales entre sí o muy cortas.
# Siguen en la web y enlazadas (los visitantes llegan igual); solo Google deja de contarlas:
#   · <meta name="robots" content="noindex, follow"> (follow: Google sigue los enlaces de la página)
#   · fuera del sitemap
# PARA VOLVER A INDEXARLAS (cuando Google indexe bien las principales): quitar esta línea de regenerar.sh y lanzar regenerar.sh.
# Uso: python3 _herramientas/noindex-poda.py      (regenerar.sh lo lanza después de los generadores)
import glob, os, re
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
META = '<meta name="robots" content="noindex, follow">'

GRUPOS = {
    # «Despido con X años»: la misma plantilla con otras cifras (90-100 % iguales)
    'despido por años': glob.glob(os.path.join(RAIZ, 'indemnizacion-despido-*-anos.html')),
    # Calendario de cada comunidad: 70-85 % iguales entre sí (solo cambian unos festivos). Queda el general.
    'calendarios de comunidades': glob.glob(os.path.join(RAIZ, 'calendario-laboral-2027-*.html')),
    # Cortas y repiten lo que ya cuenta una página más completa (entre paréntesis)
    'cortas o repetidas': [os.path.join(RAIZ, f'{s}.html') for s in [
        'paro-maximo-minimo-2026',      # (paro, tabla-paro-2026)
        'cuanto-paro-me-corresponde',   # (paro)
        'tabla-paro-2026',              # (paro)
        'dias-laborables-2027',         # (dias-laborables)
        'edad-jubilacion-2027',         # (jubilacion)
        'tramos-irpf-madrid-2026',      # (tramos-irpf-2026)
        'tramos-irpf-bizkaia-2026',     # (tramos-irpf-2026)
        'consumo-radiador-electrico',   # (fuera del tema de la web: trabajo y dinero)
    ]],
}

cambiadas, slugs = 0, []
for grupo, ficheros in GRUPOS.items():
    for f in sorted(ficheros):
        if not os.path.exists(f): print('⚠️  no existe', f); continue
        s = o = open(f, encoding='utf-8').read()
        if META not in s and 'noindex' in s: continue                                   # ya era otra cosa (redirección…)
        s = re.sub(r'<meta name="robots" content="[^"]*">', META, s, count=1)           # cambia el que hubiera
        if META not in s: s = s.replace('<meta name="viewport"', META + '\n    <meta name="viewport"', 1)   # o lo pone
        if s != o: open(f, 'w', encoding='utf-8').write(s); cambiadas += 1
        slugs.append(os.path.basename(f)[:-5])

sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
for slug in slugs:
    s = re.sub(rf'\s*<url><loc>https://calculalotuyo\.es/{re.escape(slug)}</loc>.*?</url>', '', s)   # la quita del sitemap
open(sm, 'w', encoding='utf-8').write(s)
print(f'poda: {len(slugs)} páginas fuera del índice (cambiadas {cambiadas}) · sitemap: {s.count("<loc>")} URLs')
