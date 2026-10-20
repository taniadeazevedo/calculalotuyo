# «Sueldo de un funcionario en 2026 por grupo»: tablas oficiales de la Secretaría de Estado de Presupuestos y Gastos
# (Retribuciones del personal funcionario 2026, Real Decreto-ley 14/2025, art. 2.1: +1,5 %). Comprobado el 20/10/2026.
# Uso: python3 _herramientas/funcionarios/gen-funcionarios.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, e, REVISADO, AD

REV = REVISADO.format(fecha='20 de octubre de 2026')
PDF = 'https://www.sepg.pap.hacienda.gob.es/sitios/sepg/es-ES/CostesPersonal/EstadisticasInformes/Documents/A%C3%91O%202026/Retribuciones%20del%20personal%20funcionario%202026.%20Real%20Decreto-ley%2014%202025%2C%20de%202%20de%20diciembre..pdf'
RDL = '<a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-24445" target="_blank" rel="noopener">Real Decreto-ley 14/2025</a>'

# Grupo: (sueldo al mes, trienio al mes, paga extra de junio y de diciembre, trienio en cada paga extra, qué titulación pide)
GRUPOS = {
    'A1': (1387.24, 53.39, 856.05, 32.96, 'Grado universitario (o licenciatura)'),
    'A2': (1199.52, 43.54, 874.83, 31.74, 'Grado universitario (o diplomatura)'),
    'B':  (1048.55, 38.20, 906.26, 33.03, 'Técnico Superior de FP'),
    'C1': (900.63, 32.96, 778.42, 28.45, 'Bachillerato o Técnico de FP'),
    'C2': (749.58, 22.44, 742.75, 22.20, 'ESO'),
    'E':  (686.07, 16.90, 686.07, 16.90, 'Sin titulación (agrupaciones profesionales)'),
}
anual = lambda g: GRUPOS[g][0] * 12 + GRUPOS[g][2] * 2                 # sueldo de 12 meses + las dos pagas extra
trienio_anual = lambda g: GRUPOS[g][1] * 12 + GRUPOS[g][3] * 2
# Complemento de destino al mes, por nivel (del 30 al 1). Se cobra en 14 pagas.
CD = [1211.77, 1086.89, 1041.22, 995.47, 873.38, 774.86, 729.14, 683.48, 637.73, 592.11, 550.01, 521.94, 493.86, 465.75, 437.73,
      409.59, 381.57, 353.44, 325.35, 297.24, 269.20, 255.17, 241.09, 227.07, 213.02, 198.97, 177.92, 156.91, 135.84, 114.81]
cd = {30 - i: v for i, v in enumerate(CD)}
assert round(anual('A1'), 2) == 18358.98 and round(anual('C2'), 2) == 10480.46      # cuadra con la tabla oficial
assert round(anual('A1') + cd[30] * 14, 2) == 35323.76 and round(anual('C1') + cd[18] * 14, 2) == 19278.44

ej = anual('C1') + cd[18] * 14                                          # ejemplo: C1 con nivel 18
filas_g = ''.join(f'<tr><td><strong>{g}</strong></td><td>{t}</td><td>{e(s, 2)} €</td><td>{e(tr, 2)} €</td><td><strong>{e(anual(g), 2)} €</strong></td></tr>' for g, (s, tr, pe, pt, t) in GRUPOS.items())
filas_cd = ''.join(f'<tr><td>{n}</td><td>{e(cd[n], 2)} €</td><td>{e(cd[n] * 14, 2)} €</td></tr>' for n in range(30, 0, -1))
barras = ''.join(f'<div class="barra-fila"><span class="barra-nombre">{g}</span><div><span class="barra" style="display:inline-block;width:{anual(g) / anual("A1") * 100:.1f}%;background:#4F46E5">{e(anual(g))} €</span></div></div>' for g in GRUPOS)   # mismo gráfico que el de días por mes, en el color de sueldos

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🏛️ Tablas oficiales 2026</div><h1>¿Cuánto cobra un funcionario en 2026?<br><span class="highlight">sueldo por grupo, trienios y nivel</span></h1><p>Un funcionario del grupo A1 tiene un sueldo base de {e(GRUPOS["A1"][0], 2)} € al mes y uno del C2, de {e(GRUPOS["C2"][0], 2)} €. A eso se suman el complemento de destino (según el nivel del puesto), el complemento específico y los trienios.</p>
            {REV}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <h2 class="puentes-titulo">💶 Sueldo base al año por grupo (2026)</h2>
        <div class="barras">{barras}</div>
        <p class="nota-corta">12 mensualidades más las pagas extra de junio y diciembre, sin trienios ni complementos.</p>
        <div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Grupo</th><th>Titulación</th><th>Sueldo al mes</th><th>Cada trienio al mes</th><th>Sueldo base al año</th></tr></thead><tbody>{filas_g}</tbody></table></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>🧮 Cómo se calcula lo que cobra un funcionario</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Sueldo base</strong><p>Depende solo del grupo (A1, A2, B, C1, C2 o E). Es la tabla de arriba.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Complemento de destino</strong><p>Depende del <strong>nivel del puesto</strong> (del 1 al 30). Se cobra en 14 pagas. Mira la tabla de abajo.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Complemento específico</strong><p>Lo fija cada puesto (responsabilidad, peligrosidad, dedicación…). Es el que más cambia de un puesto a otro y viene en la relación de puestos de trabajo.</p></div></div>
    <div class="calc-step"><span class="step-num">4</span><div><strong>Trienios</strong><p>Cada 3 años de servicio sumas un trienio, según el grupo en el que lo cumpliste.</p></div></div>
</div>
<p><strong>Ejemplo:</strong> un funcionario del grupo C1 en un puesto de nivel 18 cobra {e(GRUPOS["C1"][0] + cd[18], 2)} € al mes de sueldo y destino, y <strong>{e(ej, 2)} € al año</strong>, antes de sumar el complemento específico y los trienios. Para saber cuánto le queda en neto, usa la <a href="sueldo-neto">calculadora de sueldo neto</a>.</p>

<h2>📊 Complemento de destino por nivel (2026)</h2>
<div class="tabla-wrap"><table class="tabla-festivos tabla-corta"><thead><tr><th>Nivel</th><th>Al mes</th><th>Al año (14 pagas)</th></tr></thead><tbody>{filas_cd}</tbody></table></div>

<h2>📈 Subida de 2026</h2>
<p>En 2026 los sueldos públicos suben un <strong>1,5 %</strong> desde enero. Habrá otro <strong>0,5 %</strong> más si el IPC de 2026 llega al 1,5 %, que se cobraría en el primer trimestre de 2027 ({RDL}).</p>
<p class="nota-corta">Estas son las cuantías de la Administración General del Estado. Las comunidades autónomas y los ayuntamientos aplican el mismo sueldo base y trienios, pero sus complementos pueden ser distintos.</p>
</article></div></section>
'''
faqs = [
    ('¿Cuánto cobra un funcionario A1 en 2026?', f'El sueldo base es de <strong>{e(GRUPOS["A1"][0], 2)} € al mes</strong> ({e(anual("A1"), 2)} € al año con las pagas extra). Con el complemento de destino de nivel 30, {e(anual("A1") + cd[30] * 14, 2)} € al año, sin contar el complemento específico ni los trienios.'),
    ('¿Cuánto cobra un funcionario C1 en 2026?', f'El sueldo base es de <strong>{e(GRUPOS["C1"][0], 2)} € al mes</strong> ({e(anual("C1"), 2)} € al año). En un puesto de nivel 18, con el complemento de destino, {e(ej, 2)} € al año, más el complemento específico y los trienios.'),
    ('¿Cuánto es un trienio en 2026?', f'Al mes: A1 {e(GRUPOS["A1"][1], 2)} €, A2 {e(GRUPOS["A2"][1], 2)} €, B {e(GRUPOS["B"][1], 2)} €, C1 {e(GRUPOS["C1"][1], 2)} €, C2 {e(GRUPOS["C2"][1], 2)} € y E {e(GRUPOS["E"][1], 2)} €.'),
    ('¿Cuánto han subido los sueldos de los funcionarios en 2026?', 'Un <strong>1,5 %</strong> desde el 1 de enero, y un 0,5 % más si el IPC de 2026 llega al 1,5 % (se pagaría a principios de 2027).'),
]
pagina('sueldo-funcionario-2026', 'Sueldo de un funcionario en 2026: tabla por grupos A1, A2, C1 y C2',
    f'Cuánto cobra un funcionario en 2026: sueldo base del A1 ({e(GRUPOS["A1"][0], 2)} €/mes) al E, trienios, pagas extra y complemento de destino por nivel. Tablas oficiales de Hacienda.',
    'sueldo funcionario 2026, cuánto cobra un funcionario, sueldo funcionario A1 2026, sueldo C1 2026, trienios 2026, complemento de destino 2026',
    [('Sueldo de un funcionario 2026', None)], cuerpo, faqs,
    f'<a href="{PDF}" target="_blank" rel="noopener">Retribuciones del personal funcionario 2026</a> (Secretaría de Estado de Presupuestos y Gastos, Ministerio de Hacienda), según el {RDL}, art. 2.1.')
print('creada: sueldo-funcionario-2026')
