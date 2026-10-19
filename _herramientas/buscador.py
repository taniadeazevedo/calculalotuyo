# Crea buscar.json: el índice que usa el buscador de la web (título, descripción y palabras clave de cada página).
# Lo lanza regenerar.sh. Uso suelto: python3 _herramientas/buscador.py
import glob, html as H, json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FUERA = {'404', 'gracias'}                              # páginas que no deben salir en el buscador

def tipo(slug):
    """Categoría, icono y peso (las calculadoras salen antes que las páginas de detalle)."""
    calc = {'despido-improcedente', 'despido-objetivo', 'ere', 'finiquito', 'paro', 'sueldo-neto', 'irpf', 'horas-extra', 'pagas-extra',
            'vacaciones', 'subida-ipc', 'cuota-autonomos', 'facturas', 'baja-medica', 'reduccion-jornada', 'neto-a-bruto', 'dias-laborables', 'puentes-2027', 'jubilacion'}
    if slug in calc: return 'Calculadora', '🧮', 3
    if slug.startswith('modelo'): return 'Modelo gratis', '📄', 2.2
    if slug.startswith('guia') or slug == 'guias': return 'Guía', '📚', 1.6
    if slug.startswith(('calendario-laboral', 'semana-santa', 'dias-laborables-', 'trabajar-en-festivo')): return 'Calendario', '📅', 1.5
    if slug.startswith(('tabla', 'sueldo-bruto', 'paro-maximo', 'cuanto-paro', 'smi', 'iprem')): return 'Tabla y datos', '📊', 2
    if re.match(r'\d+-euros|paro-con|indemnizacion-despido', slug): return 'Respuesta rápida', '⚡', 1.2
    if slug in ('index',): return 'Inicio', '🏠', 1
    return 'Información', 'ℹ️', 0.6

limpio = lambda t: re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', t or ''))).strip()
indice = []
for f in sorted(glob.glob('*.html')):
    slug = f[:-5]
    if slug in FUERA: continue
    s = open(f, encoding='utf-8').read()
    g = lambda p: (re.search(p, s, re.S) or [None, ''])[1]
    titulo = limpio(g(r'<title>(.*?)</title>')) or limpio(g(r'<h1[^>]*>(.*?)</h1>'))   # el título corto de la pestaña se lee mejor
    cat, icono, peso = tipo(slug)
    indice.append({
        'u': '' if slug == 'index' else slug,              # dirección (sin .html, como en la web)
        't': titulo,                                       # título que se enseña
        'd': limpio(g(r'name="description" content="(.*?)"'))[:160],   # descripción corta
        'k': limpio(g(r'name="keywords" content="(.*?)"')) + ' ' + limpio(g(r'<h1[^>]*>(.*?)</h1>')),   # palabras para buscar (y el titular grande)
        'c': cat, 'i': icono, 'p': peso,
    })
json.dump(indice, open('buscar.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(f'buscar.json: {len(indice)} páginas, {os.path.getsize("buscar.json") // 1024} KB')
