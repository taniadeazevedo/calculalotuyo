# «Respuesta rápida» arriba de cada calculadora: una frase con la cifra clave y su fuente.
# Es lo que Google y las IAs (ChatGPT, Perplexity…) citan, y lo que la gente quiere leer primero.
# Se puede lanzar las veces que haga falta: si la página ya tiene respuesta, la sustituye.
# Uso: python3 _herramientas/respuestas.py      (regenerar.sh ya lo lanza). Cifras de 2026: revisar en enero.
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

RESPUESTAS = {
    'despido-improcedente': '<strong>33 días de sueldo por año trabajado</strong>, con un máximo de 24 mensualidades. Por el tiempo trabajado antes del 12 de febrero de 2012 se cuentan 45 días por año (art. 56 del Estatuto de los Trabajadores).',
    'despido-objetivo': 'Es el despido por causas <strong>económicas, técnicas, organizativas o de producción</strong>, o por ineptitud del trabajador (art. 52 del Estatuto). Te corresponden <strong>20 días de sueldo por año trabajado</strong>, con un máximo de 12 mensualidades y 15 días de preaviso, y da derecho a paro.',
    'ere': 'Como mínimo, <strong>20 días de sueldo por año trabajado</strong>, con un máximo de 12 mensualidades. En la negociación del ERE la empresa puede pactar más (art. 51 del Estatuto de los Trabajadores).',
    'finiquito': 'El finiquito suma <strong>los días trabajados del mes, las vacaciones que no has disfrutado y la parte de las pagas extra</strong> que llevas generada. Lo cobras siempre, también si te vas tú. La indemnización por despido va aparte.',
    'paro': 'Cobras el <strong>70 % de lo que cotizabas (más o menos, tu sueldo bruto) los 6 primeros meses y el 60 % después</strong>, entre 560 € y 1.225 € al mes sin hijos (2026). Con 1 año cotizado tienes 4 meses de paro; con 6 años, el máximo de 2 años.',
    'sueldo-neto': 'Con <strong>30.000 € brutos al año cobras unos 1.927 € netos al mes</strong> en 12 pagas (2026, sin hijos, contrato indefinido). Con 20.000 €, unos 1.411 €; con 40.000 €, unos 2.471 €.',
    'irpf': 'Con <strong>30.000 € brutos al año la retención es del 16,42 %</strong> (2026, sin hijos). Con el salario mínimo es muy baja, y baja más con cada hijo o con una discapacidad.',
    'horas-extra': 'Se pagan <strong>como mínimo al precio de una hora normal</strong>, o se compensan con descanso. Como máximo puedes hacer <strong>80 horas extra al año</strong> (art. 35 del Estatuto de los Trabajadores).',
    'pagas-extra': 'Tienes <strong>dos pagas extra al año como mínimo</strong>, una en Navidad. Con 30.000 € brutos en 14 pagas, cada una es de 2.143 € brutos. Si las cobras prorrateadas, van en tus 12 nóminas.',
    'vacaciones': 'Tienes <strong>30 días naturales de vacaciones al año</strong> como mínimo: 2,5 días por cada mes trabajado. Solo se pueden cambiar por dinero si se acaba el contrato (art. 38 del Estatuto de los Trabajadores).',
    'subida-ipc': 'El <strong>IPC de 2025 cerró en el 2,9 %</strong> (diciembre, INE), el que usan los convenios para 2026, y el de <strong>octubre de 2026 es del 4,9 %</strong> (adelantado). Tu empresa solo tiene que subirte el sueldo según el IPC si lo dice tu convenio o tu contrato.',   # cambiar el dato del mes cada vez que salga
    'cuota-autonomos': 'En 2026 la cuota de autónomos va de <strong>205,88 € a 607,35 € al mes</strong> según tus rendimientos netos. El primer año, con la tarifa plana, pagas <strong>88,64 € al mes</strong>.',
    'facturas': 'En una factura normal se suma el <strong>21 % de IVA</strong> y, si eres profesional, se resta una <strong>retención del 15 % de IRPF</strong> (7 % los tres primeros años de actividad).',
    'baja-medica': 'Por enfermedad común: <strong>nada los 3 primeros días, el 60 % de tu base del día 4 al 20 y el 75 % desde el día 21</strong>. Por accidente de trabajo, el 75 % desde el día siguiente a la baja.',
    'reduccion-jornada': 'Para cuidar de un hijo menor de 12 años puedes reducir <strong>entre un octavo y la mitad de tu jornada</strong>, con la misma reducción en el sueldo (art. 37.6 del Estatuto de los Trabajadores).',
    'neto-a-bruto': 'Para cobrar <strong>1.500 € netos al mes en 12 pagas necesitas unos 22.100 € brutos al año</strong> (2026, sin hijos). Para 2.000 € netos, unos 31.300 €.',
    'dias-laborables': 'Cuenta los días laborables entre dos fechas <strong>descontando los fines de semana y los festivos de tu comunidad</strong> (calendario oficial del BOE para 2026 y 2027).',
    'subida-alquiler': 'Si el año de contrato se cumple <strong>entre el 8 de octubre de 2026 y el 31 de diciembre de 2027</strong>, te pueden subir el alquiler <strong>como mucho un 2 %</strong>, salvo que pactéis otra cosa (Real Decreto-ley 29/2026). Si tu contrato no dice nada, no sube.',   # revisar si el Congreso no convalida el RDL
    'jubilacion': 'En 2027 te jubilas a los <strong>67 años, o a los 65 si tienes 38 años y 6 meses cotizados</strong>. Necesitas 15 años cotizados para tener pensión y 37 para cobrar el 100 %.',
}

hechas = 0
for pag, texto in RESPUESTAS.items():
    f = f'{pag}.html'
    s = o = open(f, encoding='utf-8').read()
    caja = f'<p class="respuesta-corta"><span>⚡ Respuesta rápida</span>{texto}</p>\n            '
    s = re.sub(r'<p class="respuesta-corta">.*?</p>\n\s*', '', s, count=1)                    # quita la anterior, si la hay
    s = s.replace('<p class="hero-meta">', caja + '<p class="hero-meta">', 1)                 # la pone justo encima de «Revisado el…»
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); hechas += 1
print('respuestas rápidas en', hechas, 'páginas')

# ================================================================ GUÍAS: preguntas y respuestas cortas arriba del todo
# Para las búsquedas que suben en Google Trends (05/11/2026). Van en una caja al principio del contenido y en el
# marcado FAQPage para Google y las IAs. Se pone entre <!-- RESPUESTAS --> y <!-- /RESPUESTAS --> (y se sustituye).
import json
limpio = lambda t: re.sub(r'<[^>]+>', '', t)
GUIAS = {
    'guia-despido-disciplinario': [
        ('¿El despido disciplinario tiene paro?', '<strong>Sí.</strong> Es una situación legal de desempleo: cobras el paro si has cotizado al menos <strong>360 días en los últimos 6 años</strong>, aunque no lo recurras.'),
        ('¿Hay indemnización?', '<strong>No</strong>, salvo que un juez o la propia empresa lo declaren <strong>improcedente</strong>: entonces son 33 días de sueldo por año. El finiquito lo cobras siempre.'),
        ('¿Cuánto tiempo tengo para reclamar?', '<strong>20 días hábiles</strong> desde la fecha del despido, empezando por la papeleta de conciliación.'),
        ('¿Qué es la audiencia previa?', 'Desde la sentencia del Tribunal Supremo de 18 de noviembre de 2024, la empresa tiene que <strong>dejarte defenderte antes de despedirte</strong> por tu conducta.'),
    ],
    'guia-paro': [
        ('¿Cuánto tiempo hay que trabajar para cobrar el paro?', 'Al menos <strong>360 días cotizados en los últimos 6 años</strong> (unos 12 meses). Con 360 días cobras 4 meses de paro; con 6 años o más, el máximo de <strong>2 años</strong>.'),
        ('¿Cómo funciona el paro?', 'Lo pides al <strong>SEPE en los 15 días hábiles</strong> siguientes a quedarte sin trabajo. Cobras el <strong>70 % de tu base</strong> los 6 primeros meses y el 60 % después (entre 560 € y 1.225 € al mes sin hijos) y se paga hacia el <strong>día 10 de cada mes</strong>.'),
        ('¿Me quedo sin paro si me voy yo?', '<strong>Sí</strong>, si te das de baja voluntaria no hay paro, salvo en algunos casos (por ejemplo, un cambio grave de condiciones o impagos).'),
    ],
}
hechas = 0
for pag, preguntas in GUIAS.items():
    f = f'{pag}.html'
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- RESPUESTAS -->.*?<!-- /RESPUESTAS -->\n?', '', s, flags=re.S)          # fuera las de una pasada anterior
    caja = '<div class="respuesta-corta"><span>⚡ Respuesta rápida</span><ul>' + ''.join(f'<li><strong>{q}</strong> {a}</li>' for q, a in preguntas) + '</ul></div>'
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': limpio(a)}} for q, a in preguntas]}, ensure_ascii=False, indent=1)
    i = s.index('<section id=', s.index('class="guide-content"'))                                 # delante del primer apartado de la guía
    s = s[:i] + f'<!-- RESPUESTAS -->{caja}<!-- /RESPUESTAS -->\n' + s[i:]
    s = s.replace('</head>', f'<!-- RESPUESTAS --><script type="application/ld+json">\n{ld}\n</script><!-- /RESPUESTAS -->\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); hechas += 1
print('respuestas de guías en', hechas, 'páginas')
