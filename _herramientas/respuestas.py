# «Respuesta rápida» arriba de cada calculadora: una frase con la cifra clave y su fuente.
# Es lo que Google y las IAs (ChatGPT, Perplexity…) citan, y lo que la gente quiere leer primero.
# Se puede lanzar las veces que haga falta: si la página ya tiene respuesta, la sustituye.
# Uso: python3 _herramientas/respuestas.py      (regenerar.sh ya lo lanza). Cifras de 2026: revisar en enero.
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

RESPUESTAS = {
    'despido-improcedente': '<strong>33 días de sueldo por año trabajado</strong>, con un máximo de 24 mensualidades. Por el tiempo trabajado antes del 12 de febrero de 2012 se cuentan 45 días por año (art. 56 del Estatuto de los Trabajadores).',
    'despido-objetivo': '<strong>20 días de sueldo por año trabajado</strong>, con un máximo de 12 mensualidades, y 15 días de preaviso (art. 53 del Estatuto de los Trabajadores).',
    'ere': 'Como mínimo, <strong>20 días de sueldo por año trabajado</strong>, con un máximo de 12 mensualidades. En la negociación del ERE la empresa puede pactar más (art. 51 del Estatuto de los Trabajadores).',
    'finiquito': 'El finiquito suma <strong>los días trabajados del mes, las vacaciones que no has disfrutado y la parte de las pagas extra</strong> que llevas generada. Lo cobras siempre, también si te vas tú. La indemnización por despido va aparte.',
    'paro': 'Cobras el <strong>70 % de lo que cotizabas (más o menos, tu sueldo bruto) los 6 primeros meses y el 60 % después</strong>, entre 560 € y 1.225 € al mes sin hijos (2026). Con 1 año cotizado tienes 4 meses de paro; con 6 años, el máximo de 2 años.',
    'sueldo-neto': 'Con <strong>30.000 € brutos al año cobras unos 1.927 € netos al mes</strong> en 12 pagas (2026, sin hijos, contrato indefinido). Con 20.000 €, unos 1.411 €; con 40.000 €, unos 2.471 €.',
    'irpf': 'Con <strong>30.000 € brutos al año la retención es del 16,42 %</strong> (2026, sin hijos). Con el salario mínimo es muy baja, y baja más con cada hijo o con una discapacidad.',
    'horas-extra': 'Se pagan <strong>como mínimo al precio de una hora normal</strong>, o se compensan con descanso. Como máximo puedes hacer <strong>80 horas extra al año</strong> (art. 35 del Estatuto de los Trabajadores).',
    'pagas-extra': 'Tienes <strong>dos pagas extra al año como mínimo</strong>, una en Navidad. Con 30.000 € brutos en 14 pagas, cada una es de 2.143 € brutos. Si las cobras prorrateadas, van en tus 12 nóminas.',
    'vacaciones': 'Tienes <strong>30 días naturales de vacaciones al año</strong> como mínimo: 2,5 días por cada mes trabajado. Solo se pueden cambiar por dinero si se acaba el contrato (art. 38 del Estatuto de los Trabajadores).',
    'subida-ipc': 'El <strong>IPC de 2025 cerró en el 2,9 %</strong> (diciembre, INE). Tu empresa solo tiene que subirte el sueldo según el IPC si lo dice tu convenio o tu contrato.',
    'cuota-autonomos': 'En 2026 la cuota de autónomos va de <strong>205,88 € a 607,35 € al mes</strong> según tus rendimientos netos. El primer año, con la tarifa plana, pagas <strong>88,64 € al mes</strong>.',
    'facturas': 'En una factura normal se suma el <strong>21 % de IVA</strong> y, si eres profesional, se resta una <strong>retención del 15 % de IRPF</strong> (7 % los tres primeros años de actividad).',
    'baja-medica': 'Por enfermedad común: <strong>nada los 3 primeros días, el 60 % de tu base del día 4 al 20 y el 75 % desde el día 21</strong>. Por accidente de trabajo, el 75 % desde el día siguiente a la baja.',
    'reduccion-jornada': 'Para cuidar de un hijo menor de 12 años puedes reducir <strong>entre un octavo y la mitad de tu jornada</strong>, con la misma reducción en el sueldo (art. 37.6 del Estatuto de los Trabajadores).',
    'neto-a-bruto': 'Para cobrar <strong>1.500 € netos al mes en 12 pagas necesitas unos 22.100 € brutos al año</strong> (2026, sin hijos). Para 2.000 € netos, unos 31.300 €.',
    'dias-laborables': 'Cuenta los días laborables entre dos fechas <strong>descontando los fines de semana y los festivos de tu comunidad</strong> (calendario oficial del BOE para 2026 y 2027).',
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
