# Guía «Qué hacer si te despiden»: los pasos y plazos en orden, con enlace a cada calculadora (23/10/2026).
# Plazos comprobados en el BOE: arts. 49.2, 53, 55, 56 y 59 del Estatuto de los Trabajadores,
# arts. 65 y 103 de la Ley reguladora de la jurisdicción social y art. 268 de la Ley General de la Seguridad Social.
# Uso: python3 _herramientas/que-hacer/gen-que-hacer.py
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))                     # carpeta de este script
sys.path.insert(0, os.path.join(AQUI, '..'))                         # para poder importar la plantilla común
from plantilla import pagina, REVISADO                               # cabecera, pie, migas y marcado para Google
RAIZ = os.path.join(AQUI, '..', '..')                                # carpeta de la web

REV = REVISADO.format(fecha='23 de octubre de 2026')                 # «Revisado el…» bajo el título
# enlace a una ley del BOE, versión consolidada
boe = lambda id_, txt: f'<a href="https://www.boe.es/buscar/act.php?id={id_}" target="_blank" rel="noopener">{txt}</a>'
ET = lambda art: boe('BOE-A-2015-11430', f'art. {art} del Estatuto de los Trabajadores')
LRJS = lambda art: boe('BOE-A-2011-15936', f'art. {art} de la Ley de la jurisdicción social')
LGSS = lambda art: boe('BOE-A-2015-11724', f'art. {art} de la Ley General de la Seguridad Social')

# Los pasos, en el orden en que hay que darlos: (título, texto)
PASOS = [
    ('Lee bien la carta de despido',
     f'Tiene que ser <strong>por escrito</strong> y decir la causa y la fecha en que tiene efecto ({ET("55.1")}). Fíjate en el tipo: <strong>disciplinario</strong> (por algo que la empresa dice que hiciste, sin indemnización) u <strong>objetivo</strong> (causas económicas, técnicas…, con 20 días por año). Guarda la carta: los plazos cuentan desde la fecha de efectos.'),
    ('Firma solo como «recibido, no conforme»',
     'Firmar la carta o el finiquito solo prueba que te lo han entregado. Escribe al lado <strong>«recibido, no conforme»</strong> y la fecha: así dejas claro que no estás de acuerdo y no renuncias a reclamar.'),
    ('Revisa el finiquito antes de firmarlo',
     f'La empresa tiene que darte una <strong>propuesta del finiquito</strong> junto con la carta, y puedes pedir que esté delante un representante de los trabajadores cuando lo firmes ({ET("49.2")}). Comprueba el sueldo de los días del mes, las vacaciones que no has disfrutado y la parte de las pagas extra con la <a href="finiquito">calculadora de finiquito</a>.'),
    ('Calcula tu indemnización',
     f'En el despido objetivo, la empresa tiene que darte <strong>20 días por año</strong> trabajado (máximo 12 mensualidades) a la vez que la carta, y avisarte con <strong>15 días</strong> de antelación ({ET("53.1")}). Si un juez declara el despido improcedente, son <strong>33 días por año</strong> (máximo 24 mensualidades) ({ET("56.1")}). Hazlo con la calculadora de <a href="despido-objetivo">despido objetivo</a> o de <a href="despido-improcedente">despido improcedente</a>.'),
    ('Pide el paro en los 15 días siguientes',
     f'Apúntate como demandante de empleo y pide la prestación en los <strong>15 días hábiles</strong> siguientes al despido. Si la pides tarde, la cobras igual, pero <strong>pierdes un día de paro por cada día de retraso</strong>. Si tienes vacaciones sin disfrutar, el plazo empieza al acabar esos días ({LGSS(268)}). Mira cuánto te toca con la <a href="paro">calculadora del paro</a>.'),
    ('Si no estás de acuerdo, presenta la papeleta de conciliación',
     f'Tienes <strong>20 días hábiles</strong> desde el despido para reclamar: no cuentan sábados, domingos ni festivos ({LRJS(103)} y {ET("59.3")}). Antes de ir al juzgado hay que presentar la <strong>papeleta de conciliación</strong> en el servicio de mediación de tu comunidad; mientras tanto, el plazo se para ({LRJS(65)}). Si no hay acuerdo, presentas la demanda con los días que te queden.'),
    ('¿Te deben dinero? Tienes un año',
     f'Para reclamar cantidades (sueldo, vacaciones, horas extra no pagadas…) el plazo es de <strong>un año</strong> ({ET("59.1")} y {ET("59.2")}). No lo confundas con los 20 días para reclamar el despido en sí.'),
]
pasos_html = '\n'.join(f'    <div class="calc-step"><span class="step-num">{i}</span><div><strong>{t}</strong><p>{x}</p></div></div>'
                       for i, (t, x) in enumerate(PASOS, 1))

# Tabla resumen de plazos: (qué, plazo, desde cuándo)
PLAZOS = [
    ('Reclamar el despido (papeleta de conciliación)', '20 días hábiles', 'El día siguiente al despido'),
    ('Pedir el paro', '15 días hábiles', 'El despido, o el final de las vacaciones no disfrutadas'),
    ('Preaviso en el despido objetivo', '15 días naturales', 'La entrega de la carta'),
    ('Reclamar dinero que te deben', '1 año', 'El día en que podías reclamarlo'),
]
filas = ''.join(f'<tr><td>{a}</td><td><strong>{b}</strong></td><td>{c}</td></tr>' for a, b, c in PLAZOS)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧭 Paso a paso</div><h1>Qué hacer si te despiden<br><span class="highlight">los pasos y los plazos, en orden</span></h1><p>Lo primero que tienes que hacer al recibir la carta de despido, qué firmar, cuánto te corresponde y hasta cuándo puedes reclamar, según el Estatuto de los Trabajadores.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Firma la carta y el finiquito como <strong>«recibido, no conforme»</strong>.</li>
<li>Pide el paro en los <strong>15 días hábiles</strong> siguientes.</li>
<li>Para reclamar el despido tienes <strong>20 días hábiles</strong>: empieza por la papeleta de conciliación.</li>
<li>Indemnización: <strong>20 días por año</strong> (objetivo) o <strong>33</strong> (improcedente).</li>
</ul></div>

<h2>✅ Los pasos, en orden</h2>
<div class="calc-steps">
{pasos_html}
</div>

<h2>⏱️ Todos los plazos de un vistazo</h2>
<table class="info-table"><tr><th>Qué</th><th>Plazo</th><th>Desde</th></tr>{filas}</table>

<h2>🧮 Pon cifras a tu caso</h2>
<p>Con tu sueldo y tus años en la empresa: <a href="despido-objetivo">indemnización por despido objetivo</a>, <a href="despido-improcedente">despido improcedente</a>, <a href="finiquito">finiquito</a> y <a href="paro">paro</a>. Si el despido es disciplinario, lee la <a href="guia-despido-disciplinario">guía del despido disciplinario</a>; para todo lo demás, la <a href="guia-despido">guía del despido</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li>Los <strong>20 días para reclamar no se amplían</strong>: si se pasan, ya no se puede discutir el despido. No esperes al último día.</li>
<li>Tu <strong>convenio colectivo</strong> puede añadir requisitos a la carta de despido o mejorar las cantidades.</li>
<li>Esta guía es orientativa. Para decidir si reclamar, consulta con un abogado laboralista, un graduado social o tu sindicato.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Qué es lo primero que tengo que hacer si me despiden?',
     'Leer la carta (tipo de despido y fecha), firmarla como <strong>«recibido, no conforme»</strong>, revisar el finiquito y pedir el paro en los <strong>15 días hábiles</strong> siguientes. Si no estás de acuerdo, tienes <strong>20 días hábiles</strong> para presentar la papeleta de conciliación.'),
    ('¿Si firmo el finiquito pierdo el derecho a reclamar?',
     'Si escribes <strong>«recibido, no conforme»</strong> al firmar, dejas claro que solo lo has recibido y que no estás de acuerdo. Además, puedes pedir que esté presente un representante de los trabajadores (artículo 49.2 del Estatuto de los Trabajadores).'),
    ('¿Cuántos días tengo para reclamar un despido?',
     '<strong>20 días hábiles</strong> desde el día siguiente al despido, sin contar sábados, domingos ni festivos. Al presentar la papeleta de conciliación el plazo se para y se reanuda después del acto de conciliación.'),
    ('¿Qué pasa si pido el paro tarde?',
     'Lo cobras igualmente, pero desde el día en que lo pides: <strong>pierdes un día de prestación por cada día de retraso</strong> desde que acabó el plazo de 15 días (artículo 268 de la Ley General de la Seguridad Social).'),
]
pagina('que-hacer-si-me-despiden', 'Qué hacer si te despiden: pasos y plazos (2026)',
    'Me han despedido, ¿y ahora qué? Firma «no conforme», pide el paro en 15 días hábiles y reclama en 20 días hábiles. Los pasos en orden, con la ley.',
    'qué hacer si me despiden, me han despedido qué hago, plazo reclamar despido, papeleta de conciliación, firmar finiquito no conforme',
    [('Guías', 'guias'), ('Qué hacer si te despiden', None)], cuerpo, faqs,
    'Estatuto de los Trabajadores (arts. 49, 53, 55, 56 y 59), Ley reguladora de la jurisdicción social (arts. 65 y 103) y Ley General de la Seguridad Social (art. 268), versiones consolidadas del BOE.',
    menu_activo='Guías')

# Sitemap: se añade la página si aún no está (sitemap.py pone la fecha)
sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
if '/que-hacer-si-me-despiden<' not in s:
    linea = '    <url><loc>https://calculalotuyo.es/que-hacer-si-me-despiden</loc><lastmod>2026-10-23</lastmod><priority>0.8</priority></url>\n'
    s = s.replace('</urlset>', linea + '</urlset>'); open(sm, 'w', encoding='utf-8').write(s)

# Tarjeta en la página de Guías, la primera de «Despido y fin del contrato» (solo si no está)
g = os.path.join(RAIZ, 'guias.html'); s = open(g, encoding='utf-8').read()
if 'href="que-hacer-si-me-despiden"' not in s:
    tarjeta = '''<a href="que-hacer-si-me-despiden" class="guide-card">
                    <span class="guide-icon">🧭</span>
                    <h3>Qué hacer si te despiden</h3>
                    <p>Los pasos en orden: qué firmar, cuándo pedir el paro y hasta cuándo puedes reclamar.</p>
                    <span class="guide-link">Leer guía →</span>
                </a>
                '''
    s = re.sub(r'(<h2>Despido y fin del contrato</h2>\s*<div class="guides-grid">\s*)', lambda m: m.group(1) + tarjeta, s, count=1)
    open(g, 'w', encoding='utf-8').write(s)
print('creada: que-hacer-si-me-despiden')
