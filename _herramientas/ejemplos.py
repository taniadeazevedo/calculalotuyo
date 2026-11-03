# Ejemplos («Laura, camarera en Barcelona…»): qué va dentro del círculo de cada persona (03/11/2026).
#   · Si hay una foto en img/personas/<nombre>.jpg (o .webp / .png), por ejemplo img/personas/laura.jpg, sale la foto.
#   · Si no, el icono de persona de siempre.
# Las fotos tienen que poder usarse (bancos gratuitos como Unsplash o Pexels, o propias). Se puede lanzar las veces que haga falta.
# Uso: python3 _herramientas/ejemplos.py      (regenerar.sh lo lanza después de los iconos)
import glob, os, re, unicodedata
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

ICONO = '<span class="example-icon"><svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-user"/></svg></span>'
# el círculo (con lo que tenga dentro) y, justo después, el nombre en negrita
CIRCULO = re.compile(r'<span class="example-icon[^"]*"[^>]*>(?:(?!</span>).)*</span>(\s*<div>\s*<strong>)([^<,]+)', re.S)

def sin_tildes(t):
    """«Ainhoa» → «ainhoa», «Íñigo» → «inigo»: el nombre del archivo de la foto."""
    return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')

def circulo(m):
    nombre = m.group(2).strip()
    for ext in ('webp', 'jpg', 'jpeg', 'png'):
        foto = f'img/personas/{sin_tildes(nombre)}.{ext}'
        if os.path.exists(foto):                                        # hay foto: se usa (decorativa, el nombre ya va al lado)
            return f'<span class="example-icon example-foto"><img src="{foto}" alt="" width="56" height="56" loading="lazy"></span>{m.group(1)}{m.group(2)}'
    return ICONO + m.group(1) + m.group(2)                              # sin foto: el icono de siempre

cambiadas = 0
for f in glob.glob('*.html'):
    s = open(f, encoding='utf-8').read()
    n = CIRCULO.sub(circulo, s)
    if n != s: open(f, 'w', encoding='utf-8').write(n); cambiadas += 1
fotos = len(glob.glob('img/personas/*'))
print('ejemplos: círculos revisados · páginas cambiadas', cambiadas, '· fotos disponibles', fotos)
