# Enlaces internos hacia las páginas que Google ya coloca bien (Search Console, 04/11/2026):
# cuantos más enlaces reciben desde las páginas grandes, más importantes le parecen a Google.
#   · bloque «También te puede interesar» al final de varias calculadoras (entre <!-- ENLACES --> y <!-- /ENLACES -->)
#   · lista «Despido con X años» en las calculadoras y la guía de despido
#   · atajos de la portada («Respuestas rápidas») hacia esas páginas
# Se puede lanzar las veces que haga falta: si el bloque ya está, lo sustituye. Lo lanza regenerar.sh después de iconos.py.
# Uso: python3 _herramientas/enlaces-internos.py
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

ANOS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20]                            # = PAGINAS de despido/gen-despido.py
anos = lambda a: f'{a} {"año" if a == 1 else "años"}'                         # «1 año», «7 años»

# Porcentaje de subida de las pensiones, leído del propio artículo (así cambia solo cuando cambia el IPC)
_pen = open('subida-pensiones-2027.html', encoding='utf-8').read()
PENSIONES = re.search(r'Subida de las pensiones 2027: un ([\d,]+ %)', _pen).group(1)   # «3,59 %»

# Página → enlaces del bloque «También te puede interesar» (dirección, texto)
TAMBIEN = {
    'jubilacion': [('subida-pensiones-2027', f'Cuánto subirán las pensiones en 2027 (≈ {PENSIONES})'), ('obligado-a-declarar-renta', 'Con pensión, ¿tengo que hacer la renta?')],
    'subida-ipc': [('subida-pensiones-2027', f'Pensiones 2027: ≈ {PENSIONES} con el IPC'), ('ipc-septiembre-2026-sueldo', 'IPC al 4,9 %: qué significa para tu sueldo'), ('sueldo-funcionario-2026', 'Sueldo de un funcionario 2026')],
    'paro': [('iprem-2026', 'IPREM 2026: 600 € al mes'), ('tabla-paro-2026', 'Tabla del paro 2026'), ('paro-maximo-minimo-2026', 'Paro máximo y mínimo 2026')],
    'vacaciones': [('puente-diciembre-2026', 'Puente de diciembre 2026: ¿es festivo el 7?'), ('puentes-2027', 'Los mejores puentes de 2027')],
    'dias-laborables': [('puente-diciembre-2026', 'Puente de diciembre 2026: ¿es festivo el 7?'), ('calendario-laboral-2027', 'Calendario laboral 2027')],
    'calendario-laboral-2027': [('puente-diciembre-2026', 'Puente de diciembre 2026: dónde es festivo el lunes 7'), ('puentes-2027', 'Los mejores puentes de 2027')],
    'sueldo-neto': [('subida-ipc', 'Cuánto debería subir tu sueldo con el IPC'), ('sueldo-funcionario-2026', 'Sueldo de un funcionario 2026'), ('reduccion-jornada', 'Reducción de jornada: cuánto cobras')],
    'finiquito': [('tabla-indemnizacion-despido', 'Tabla de indemnización por despido'), ('indemnizacion-despido-7-anos', 'Despido con 7 años'), ('indemnizacion-despido-10-anos', 'Despido con 10 años')],
}
# Páginas con la lista de antigüedades (debajo del enlace a la tabla de indemnización)
CON_ANOS = ['despido-improcedente', 'despido-objetivo', 'ere', 'guia-despido']
TRAS_TABLA = 'tabla de indemnización por despido</a>.</p>'

# Portada: atajo → dónde lleva ahora (antes iba a una fila de la tabla o a una página que Google no coloca)
PORTADA = [
    ('href="tabla-indemnizacion-despido#anos-5" class="rapida"', 'href="indemnizacion-despido-5-anos" class="rapida"'),
    ('<a href="cuanto-paro-me-corresponde" class="rapida"><span class="rapida-pregunta">2 años cotizados</span><strong class="rapida-respuesta">8 meses de paro</strong><span class="rapida-enlace">Cuánto paro me corresponde →</span></a>',
     f'<a href="subida-pensiones-2027" class="rapida"><span class="rapida-pregunta">Subida de las pensiones 2027</span><strong class="rapida-respuesta">≈ {PENSIONES}</strong><span class="rapida-enlace">Cuánto subirán y por qué →</span></a>'),
]

def bloque(marca, html):
    return f'<!-- {marca} -->\n{html}\n<!-- /{marca} -->\n'

def quitar(s, marca):
    return re.sub(rf'<!-- {marca} -->.*?<!-- /{marca} -->\n', '', s, flags=re.S)   # quita la versión anterior, si la hay

cambiadas = 0
for pag, enlaces in TAMBIEN.items():
    f = f'{pag}.html'
    s = o = quitar(open(f, encoding='utf-8').read(), 'ENLACES')
    lista = ''.join(f'<a href="{h}">{t}</a>' for h, t in enlaces)
    html = f'    <section class="section"><div class="container"><article class="seo-section"><h2><svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-pin"/></svg> También te puede interesar</h2><div class="enlaces-sueldo">{lista}</div></article></div></section>'
    s = s.replace('<footer', bloque('ENLACES', html) + '<footer', 1)              # justo antes del pie
    if s != open(f, encoding='utf-8').read(): open(f, 'w', encoding='utf-8').write(s); cambiadas += 1

lista_anos = '<div class="enlaces-sueldo">' + ''.join(f'<a href="indemnizacion-despido-{a}-anos">{anos(a)}</a>' for a in ANOS) + '</div>'
for pag in CON_ANOS:
    f = f'{pag}.html'
    s = quitar(open(f, encoding='utf-8').read(), 'ENLACES-ANOS')
    if TRAS_TABLA in s:
        s = s.replace(TRAS_TABLA, TRAS_TABLA + '\n' + bloque('ENLACES-ANOS', lista_anos).rstrip('\n'), 1)
    else:
        print('⚠️  sin sitio para la lista de años en', f)
    if s != open(f, encoding='utf-8').read(): open(f, 'w', encoding='utf-8').write(s); cambiadas += 1

s = o = open('index.html', encoding='utf-8').read()
s = re.sub(r'<a href="subida-pensiones-2027" class="rapida">.*?</a>', PORTADA[1][0], s)   # vuelve al estado original y lo cambia otra vez (cifra al día)
for antes, despues in PORTADA:
    s = s.replace(antes, despues)
if s != o: open('index.html', 'w', encoding='utf-8').write(s); cambiadas += 1
print('enlaces internos en', cambiadas, 'páginas · pensiones', PENSIONES)
