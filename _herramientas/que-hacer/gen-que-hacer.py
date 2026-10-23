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

def registrar(slug, seccion, icono, titulo, resumen):
    """Añade la guía al sitemap (si falta) y su tarjeta, la primera de su sección en la página de Guías."""
    sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    if f'/{slug}<' not in s:                                            # sitemap.py pone luego la fecha buena
        s = s.replace('</urlset>', f'    <url><loc>https://calculalotuyo.es/{slug}</loc><lastmod>2026-10-23</lastmod><priority>0.8</priority></url>\n</urlset>')
        open(sm, 'w', encoding='utf-8').write(s)
    g = os.path.join(RAIZ, 'guias.html'); s = open(g, encoding='utf-8').read()
    if f'href="{slug}"' not in s:                                       # la tarjeta, solo una vez
        tarjeta = f"""<a href="{slug}" class="guide-card">
                    <span class="guide-icon">{icono}</span>
                    <h3>{titulo}</h3>
                    <p>{resumen}</p>
                    <span class="guide-link">Leer guía →</span>
                </a>
                """
        s = re.sub(rf'(<h2>{seccion}</h2>\s*<div class="guides-grid">\s*)', lambda m: m.group(1) + tarjeta, s, count=1)
        open(g, 'w', encoding='utf-8').write(s)

registrar('que-hacer-si-me-despiden', 'Despido y fin del contrato', '🧭', 'Qué hacer si te despiden',
          'Los pasos en orden: qué firmar, cuándo pedir el paro y hasta cuándo puedes reclamar.')
print('creada: que-hacer-si-me-despiden')

# ===================== «Qué hacer si te pones de baja» =====================
# Datos: arts. 169, 172, 173 y 174 de la LGSS (duración, 180 días cotizados, quién paga cada día, extinción) y los
# porcentajes (60 % y 75 %) de la guía de la baja médica, ya revisada contra el BOE el 14/10/2026.
PASOS_BAJA = [
    ('Ve al médico que te corresponde',
     'Si es una <strong>enfermedad común</strong> o un accidente fuera del trabajo, al médico de cabecera de la sanidad pública. Si es un <strong>accidente de trabajo</strong> (también yendo o volviendo) o una enfermedad profesional, a la <strong>mutua</strong> de tu empresa. Es quien te da el parte de baja.'),
    ('Avisa a la empresa, pero no le lleves el parte',
     'Desde abril de 2023 el parte <strong>le llega a la empresa por vía telemática</strong>: tú solo te quedas tu copia. Aun así, avisa cuanto antes de que estás de baja; tu convenio puede pedirlo.'),
    ('Calcula cuánto vas a cobrar',
     f'Con enfermedad común, los <strong>3 primeros días no se cobran</strong> (salvo convenio), del 4 al 20 cobras el <strong>60 %</strong> de tu base reguladora y desde el 21, el <strong>75 %</strong>. Con accidente de trabajo, el 75 % desde el día siguiente. Para la enfermedad común necesitas <strong>180 días cotizados en los últimos 5 años</strong> ({LGSS(172)}). Hazlo con la <a href="baja-medica">calculadora de la baja médica</a>.'),
    ('Mira tu convenio',
     'Muchos convenios obligan a la empresa a <strong>completar hasta el 100 % del sueldo</strong>, a veces desde el primer día. Es lo que más cambia lo que cobras.'),
    ('Sigue cobrando en tu nómina',
     f'La empresa te adelanta el dinero en la nómina. En la enfermedad común, los días 4 a 15 los paga ella y desde el 16, la Seguridad Social o la mutua ({LGSS(173)}). Si se acaba tu contrato estando de baja, pasas a cobrar directamente de la Seguridad Social o la mutua.'),
    ('Acude a todas las revisiones',
     f'Ve a las revisiones del médico y a las citas de la mutua. <strong>No presentarte sin una causa justificada</strong> puede hacer que pierdas la prestación ({LGSS(174)}).'),
    ('Cuando te den el alta, vuelve al trabajo',
     f'Te incorporas al día siguiente del alta. La baja dura como mucho <strong>365 días</strong>, ampliables otros 180 ({LGSS(169)}). Si después de los 365 días el INSS te da el alta y no estás de acuerdo, tienes solo <strong>4 días naturales</strong> para decirlo ante la inspección médica.'),
]
pasos_baja = '\n'.join(f'    <div class="calc-step"><span class="step-num">{i}</span><div><strong>{t}</strong><p>{x}</p></div></div>'
                        for i, (t, x) in enumerate(PASOS_BAJA, 1))
# Cuánto se cobra según el día de baja: (días, enfermedad común, accidente de trabajo)
COBRO = [('Del 1 al 3', 'Nada (salvo convenio)', '75 % (el día del accidente, la empresa)'),
         ('Del 4 al 20', '60 %', '75 %'), ('Desde el 21', '75 %', '75 %')]
filas_baja = ''.join(f'<tr><td>{a}</td><td><strong>{b}</strong></td><td><strong>{c}</strong></td></tr>' for a, b, c in COBRO)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧭 Paso a paso</div><h1>Qué hacer si te pones de baja<br><span class="highlight">los pasos, en orden</span></h1><p>A qué médico ir, qué hacer con el parte, cuánto vas a cobrar y qué tienes que cumplir mientras estás de baja, según la Ley General de la Seguridad Social.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Enfermedad común: médico de cabecera. Accidente de trabajo: <strong>la mutua</strong>.</li>
<li>El parte ya <strong>no tienes que llevarlo</strong> a la empresa.</li>
<li>Cobras <strong>nada los 3 primeros días</strong>, el 60 % hasta el día 20 y el 75 % después (salvo convenio).</li>
<li>Acude a todas las revisiones: si faltas sin motivo, puedes perder la prestación.</li>
</ul></div>

<h2>✅ Los pasos, en orden</h2>
<div class="calc-steps">
{pasos_baja}
</div>

<h2>💶 Cuánto cobras según el día de baja</h2>
<table class="info-table"><tr><th>Días de baja</th><th>Enfermedad común</th><th>Accidente de trabajo</th></tr>{filas_baja}</table>
<p>Porcentajes sobre tu base reguladora: la base de cotización del mes anterior a la baja dividida entre 30.</p>

<h2>🧮 Pon cifras a tu caso</h2>
<p>Calcula lo que vas a cobrar con la <a href="baja-medica">calculadora de la baja médica</a>. Todo el detalle (bajas especiales, controles de la mutua, qué pasa a partir de los 365 días) está en la <a href="guia-baja-medica">guía de la baja médica</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li>Tu <strong>convenio colectivo</strong> puede mejorar mucho estas cantidades: revísalo.</li>
<li>Esta guía es orientativa. Ante dudas con un alta o una revisión, consulta con tu médico, la mutua, un graduado social o tu sindicato.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Qué tengo que hacer si me pongo de baja?',
     'Ir al médico de cabecera (o a la <strong>mutua</strong> si es un accidente de trabajo), avisar a la empresa, revisar tu convenio y acudir a todas las revisiones. El parte ya no tienes que llevarlo: le llega a la empresa por vía telemática.'),
    ('¿Tengo que llevar el parte de baja a la empresa?',
     '<strong>No.</strong> Desde abril de 2023 el servicio de salud o la mutua se lo comunica a la empresa por vía telemática. Tú solo recibes tu copia.'),
    ('¿Cuánto cobro los primeros días de baja?',
     'Con enfermedad común, <strong>nada los 3 primeros días</strong> (salvo que tu convenio lo mejore), el <strong>60 %</strong> de la base reguladora del día 4 al 20 y el <strong>75 %</strong> desde el 21. Con accidente de trabajo, el 75 % desde el día siguiente.'),
    ('¿Quién me paga la baja?',
     'Lo cobras en tu nómina. En la enfermedad común, los días 4 a 15 los paga la empresa y desde el día 16, la Seguridad Social o la mutua (artículo 173 de la Ley General de la Seguridad Social).'),
]
pagina('que-hacer-si-me-pongo-de-baja', 'Qué hacer si te pones de baja: pasos (2026)',
    'Me he puesto de baja, ¿qué hago? A qué médico ir, si llevar el parte a la empresa, cuánto cobras (60 % y 75 %) y las revisiones. Paso a paso, con la ley.',
    'qué hacer si me pongo de baja, baja médica qué hacer, parte de baja empresa, cuánto se cobra de baja',
    [('Guías', 'guias'), ('Qué hacer si te pones de baja', None)], cuerpo, faqs,
    'Ley General de la Seguridad Social (arts. 169, 172, 173 y 174), versión consolidada del BOE, y normativa de los partes de incapacidad temporal.',
    menu_activo='Guías')
registrar('que-hacer-si-me-pongo-de-baja', 'Salud y familia', '🧭', 'Qué hacer si te pones de baja',
          'Los pasos en orden: a qué médico ir, qué hacer con el parte, cuánto cobras y las revisiones.')
print('creada: que-hacer-si-me-pongo-de-baja')

# ===================== «Qué hacer si vas a tener un hijo» =====================
# Datos de la guía del permiso por nacimiento (revisada contra el BOE el 14/10/2026) y comprobados el 23/10/2026:
# art. 48.4 ET (19 semanas), art. 37.4 ET (lactancia hasta los 9 meses), arts. 177-179 LGSS (prestación del 100 %).
PASOS_HIJO = [
    ('Decide cuándo contarlo en el trabajo',
     'No estás obligada a comunicar el embarazo, y la protección frente al despido existe aunque la empresa no lo sepa. Pero decirlo <strong>por escrito</strong> te permite pedir que adapten tu puesto si tiene riesgos y deja constancia de la fecha.'),
    ('Usa tus permisos durante el embarazo',
     'Tienes <strong>permiso retribuido</strong> para los exámenes prenatales y la preparación al parto si son en horario de trabajo. Si tu puesto supone un riesgo y no pueden cambiarlo, existe la prestación por riesgo durante el embarazo, al 100 %.'),
    ('Planifica las 19 semanas de cada progenitor',
     f'Cada progenitor tiene <strong>19 semanas</strong> ({ET("48.4")}): <strong>6 obligatorias</strong> justo después del parto, <strong>11 flexibles</strong> hasta que el bebé cumple 12 meses (avisando a la empresa con 15 días de antelación) y <strong>2 más</strong> hasta los 8 años. En familias monoparentales son 32 semanas. No se pueden ceder al otro progenitor.'),
    ('Pide la prestación al INSS',
     f'Durante el permiso no cobras sueldo, sino una prestación del <strong>100 % de tu base reguladora</strong> ({LGSS(179)}) que paga directamente el INSS, por internet o en una oficina. <strong>No paga IRPF.</strong> Necesitas haber cotizado 180 días en los últimos 7 años (menos si tienes menos de 26 años).'),
    ('Inscribe al bebé y avisa de los cambios',
     'Inscribe el nacimiento en el Registro Civil (en muchos hospitales se tramita desde allí) y comunica a la empresa el nacimiento para que lo tenga en cuenta en la nómina: los hijos <strong>bajan la retención de IRPF</strong>.'),
    ('Aprovecha la lactancia al volver',
     f'Hasta que el bebé cumple <strong>9 meses</strong>, cada progenitor tiene una <strong>hora diaria retribuida</strong> ({ET("37.4")}), que puede cambiar por media hora menos de jornada o <strong>acumular en días completos</strong>.'),
    ('Conoce tus opciones después',
     'Puedes <strong>reducir la jornada</strong> hasta que tu hijo cumpla 12 años (con la parte proporcional de sueldo) o pedir una <strong>excedencia</strong> de hasta 3 años. Y el despido es nulo durante el embarazo, el permiso y hasta 12 meses después del nacimiento, salvo causa real ajena a la maternidad o paternidad.'),
]
pasos_hijo = '\n'.join(f'    <div class="calc-step"><span class="step-num">{i}</span><div><strong>{t}</strong><p>{x}</p></div></div>'
                       for i, (t, x) in enumerate(PASOS_HIJO, 1))
SEMANAS = [('Obligatorias', '6', 'Seguidas, justo después del parto'),
           ('Flexibles', '11', 'Por semanas, hasta los 12 meses del bebé'),
           ('Cuidado del menor', '2', 'Por semanas, hasta los 8 años')]
filas_hijo = ''.join(f'<tr><td>{a}</td><td><strong>{b} semanas</strong></td><td>{c}</td></tr>' for a, b, c in SEMANAS)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧭 Paso a paso</div><h1>Qué hacer si vas a tener un hijo<br><span class="highlight">permisos y trámites, en orden</span></h1><p>Desde el embarazo hasta la vuelta al trabajo: qué permisos tienes, cuánto cobras, qué pedir al INSS y qué opciones tienes después, según el Estatuto de los Trabajadores.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Cada progenitor tiene <strong>19 semanas</strong> de permiso (32 en familias monoparentales).</li>
<li>Cobras el <strong>100 % de tu base reguladora</strong>, lo paga el INSS y <strong>no tributa en el IRPF</strong>.</li>
<li>Al volver, <strong>1 hora diaria de lactancia</strong> hasta los 9 meses, que se puede acumular en días.</li>
<li>El despido es <strong>nulo</strong> desde el embarazo hasta 12 meses después del nacimiento, salvo causa ajena.</li>
</ul></div>

<h2>✅ Los pasos, en orden</h2>
<div class="calc-steps">
{pasos_hijo}
</div>

<h2>📆 Cómo se reparten las 19 semanas</h2>
<table class="info-table"><tr><th>Tramo</th><th>Semanas</th><th>Cuándo</th></tr>{filas_hijo}</table>
<p>La madre biológica puede adelantar hasta 4 semanas antes de la fecha prevista de parto. Hay semanas extra por parto múltiple, discapacidad o bebés prematuros u hospitalizados.</p>

<h2>🧮 Pon cifras a tu caso</h2>
<p>Si vas a reducir la jornada, mira cuánto cobrarías con la <a href="reduccion-jornada">calculadora de reducción de jornada</a>. Todo el detalle (requisitos por edad, riesgo durante el embarazo, excedencia y autónomos) está en la <a href="guia-nacimiento">guía del permiso por nacimiento</a> y en la <a href="guia-permisos">guía de permisos</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li>Tu <strong>convenio colectivo</strong> puede mejorar estos permisos o complementar la prestación.</li>
<li>Esta guía es orientativa. Para tu caso concreto, consulta con el INSS, un graduado social o tu sindicato.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Qué tengo que hacer si voy a tener un hijo?',
     'Planificar las <strong>19 semanas</strong> de permiso de cada progenitor, pedir la <strong>prestación al INSS</strong>, inscribir al bebé en el Registro Civil y avisar a la empresa. Al volver, puedes usar la hora de lactancia, reducir la jornada o pedir una excedencia.'),
    ('¿Cuánto se cobra durante el permiso por nacimiento?',
     'El <strong>100 % de tu base reguladora</strong> (la base de cotización del mes anterior), que paga directamente el INSS. Está <strong>exenta de IRPF</strong>.'),
    ('¿Cuántas semanas de permiso tiene cada progenitor en 2026?',
     '<strong>19 semanas</strong>: 6 obligatorias después del parto, 11 flexibles hasta los 12 meses y 2 hasta que el menor cumple 8 años (artículo 48.4 del Estatuto de los Trabajadores). En familias monoparentales, 32.'),
    ('¿Me pueden despedir si estoy embarazada?',
     'El despido es <strong>nulo</strong> durante el embarazo (aunque la empresa no lo sepa), el permiso y hasta 12 meses después del nacimiento, salvo que la empresa demuestre una causa real ajena a la maternidad o paternidad. Nulo significa readmisión y pago de los salarios no cobrados.'),
]
pagina('que-hacer-si-voy-a-tener-un-hijo', 'Qué hacer si vas a tener un hijo: permisos y trámites',
    'Vas a tener un hijo: 19 semanas de permiso por progenitor, prestación del 100 % sin IRPF, lactancia y trámites en orden. Paso a paso, con la ley del BOE.',
    'qué hacer si voy a tener un hijo, permiso por nacimiento 2026, baja por maternidad paternidad, trámites nacimiento',
    [('Guías', 'guias'), ('Qué hacer si vas a tener un hijo', None)], cuerpo, faqs,
    'Estatuto de los Trabajadores (arts. 37.4 y 48.4) y Ley General de la Seguridad Social (arts. 177 a 179), versiones consolidadas del BOE.',
    menu_activo='Guías')
registrar('que-hacer-si-voy-a-tener-un-hijo', 'Salud y familia', '🧭', 'Qué hacer si vas a tener un hijo',
          'Los pasos en orden: las 19 semanas de permiso, la prestación del INSS, la lactancia y tus opciones después.')
print('creada: que-hacer-si-voy-a-tener-un-hijo')

# ===================== «Qué hacer si te quedas en paro» =====================
# Datos de la guía del paro (revisada contra el BOE el 14/10/2026) y art. 268 LGSS (15 días, inscripción y acuerdo
# de actividad, pérdida de días si se pide tarde), comprobado el 23/10/2026.
PASOS_PARO = [
    ('Comprueba que tienes derecho',
     'Necesitas estar en <strong>situación legal de desempleo</strong> (despido, fin de contrato, ERE…) y haber cotizado <strong>al menos 360 días en los últimos 6 años</strong>. Si te has ido tú de forma voluntaria, en general <strong>no hay paro</strong>, salvo casos como un traslado o una modificación de condiciones que te perjudica.'),
    ('Apúntate y pide el paro en 15 días hábiles',
     f'Inscríbete como <strong>demandante de empleo</strong> en el servicio de empleo de tu comunidad y pide la prestación al SEPE en los <strong>15 días hábiles</strong> siguientes a quedarte sin trabajo. Al pedirla firmas el <strong>acuerdo de actividad</strong> (el compromiso de buscar empleo) ({LGSS(268)}). Si tenías vacaciones sin disfrutar, el plazo empieza cuando acaban.'),
    ('Si lo pides tarde, pierdes días',
     'Lo cobras igualmente, pero desde el día en que lo pides: <strong>pierdes un día de paro por cada día de retraso</strong>. Por eso conviene no esperar al último momento.'),
    ('Calcula cuánto vas a cobrar',
     'Los <strong>6 primeros meses</strong> cobras el <strong>70 %</strong> de tu base reguladora (la media de lo cotizado en los últimos 180 días) y después el <strong>60 %</strong>, con un mínimo y un máximo según tus hijos. Hazlo con la <a href="paro">calculadora del paro</a>.'),
    ('Mira cuánto tiempo lo cobrarás',
     'Depende de lo cotizado en los últimos 6 años: <strong>4 meses</strong> con 360 días y hasta <strong>24 meses</strong> con 2.160 días o más. Lo tienes en la <a href="tabla-paro-2026">tabla del paro 2026</a>.'),
    ('Cumple tus obligaciones mientras cobras',
     'Mantén la <strong>inscripción como demandante de empleo</strong> durante todo el paro (si no, se suspende el pago), acude a las citas del servicio de empleo y comunica cualquier cambio, como empezar a trabajar.'),
    ('Cuando se acabe, mira el subsidio',
     'Si agotas el paro, o no llegas a los 360 días cotizados, puedes tener derecho a un <strong>subsidio por desempleo</strong> si cumples sus requisitos. Infórmate en el SEPE antes de que termine.'),
]
pasos_paro = '\n'.join(f'    <div class="calc-step"><span class="step-num">{i}</span><div><strong>{t}</strong><p>{x}</p></div></div>'
                       for i, (t, x) in enumerate(PASOS_PARO, 1))
TOPES = [('Sin hijos', '560 €', '1.225 €'), ('Con 1 hijo', '749 €', '1.400 €'), ('Con 2 o más hijos', '749 €', '1.575 €')]
filas_paro = ''.join(f'<tr><td>{a}</td><td>{b}</td><td><strong>{c}</strong></td></tr>' for a, b, c in TOPES)

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🧭 Paso a paso</div><h1>Qué hacer si te quedas en paro<br><span class="highlight">los pasos y los plazos, en orden</span></h1><p>Si tienes derecho, dónde apuntarte, el plazo para pedirlo, cuánto y cuánto tiempo cobrarás y qué tienes que cumplir, según la Ley General de la Seguridad Social.</p>
            {REV}</div></section>

    <section class="section"><div class="container"><article class="seo-section">
<div class="respuesta-corta"><strong>⚡ En 30 segundos</strong><ul>
<li>Necesitas <strong>360 días cotizados</strong> en los últimos 6 años y no haberte ido de forma voluntaria.</li>
<li>Pídelo en los <strong>15 días hábiles</strong> siguientes: si tardas, pierdes días de paro.</li>
<li>Cobras el <strong>70 %</strong> de tu base los 6 primeros meses y el <strong>60 %</strong> después, con un máximo de 1.225 € sin hijos.</li>
<li>Dura de <strong>4 a 24 meses</strong>, según lo cotizado.</li>
</ul></div>

<h2>✅ Los pasos, en orden</h2>
<div class="calc-steps">
{pasos_paro}
</div>

<h2>💶 Mínimo y máximo del paro en 2026</h2>
<table class="info-table"><tr><th>Situación</th><th>Mínimo al mes</th><th>Máximo al mes</th></tr>{filas_paro}</table>
<p>Cuantías brutas a jornada completa, calculadas sobre el IPREM de 600 € más una sexta parte. Del paro se descuenta tu cotización a la Seguridad Social y, si corresponde, el IRPF.</p>

<h2>🧮 Pon cifras a tu caso</h2>
<p>Calcula lo que cobrarás con la <a href="paro">calculadora del paro</a>. Si vienes de un despido, mira también la guía <a href="que-hacer-si-me-despiden">qué hacer si te despiden</a>. Todo el detalle (fijos discontinuos, baja médica durante el paro, IRPF) está en la <a href="guia-paro">guía del paro</a>.</p>

<h2>⚠️ Ten en cuenta</h2>
<ul>
<li>El plazo de 15 días hábiles cuenta desde el día siguiente a quedarte sin trabajo, o desde el final de las vacaciones no disfrutadas.</li>
<li>Esta guía es orientativa. Para tu caso, consulta con el SEPE, un graduado social o tu sindicato.</li>
</ul>
</article></div></section>
'''
faqs = [
    ('¿Qué tengo que hacer cuando me quedo en paro?',
     'Inscribirte como <strong>demandante de empleo</strong> y pedir la prestación al SEPE en los <strong>15 días hábiles</strong> siguientes, firmando el acuerdo de actividad. Después, mantener la inscripción y acudir a las citas mientras cobras.'),
    ('¿Cuánto tiempo tengo para pedir el paro?',
     '<strong>15 días hábiles</strong> desde que te quedas sin trabajo (o desde que acaban tus vacaciones no disfrutadas). Si lo pides después, lo cobras desde la fecha de la solicitud y <strong>pierdes un día por cada día de retraso</strong> (artículo 268 de la Ley General de la Seguridad Social).'),
    ('¿Cuántos días tengo que haber cotizado para cobrar el paro?',
     'Al menos <strong>360 días en los últimos 6 años</strong>. Con 360 días cobras 4 meses, y el máximo son 24 meses con 2.160 días o más.'),
    ('¿Si me voy de la empresa tengo paro?',
     'En general <strong>no</strong>: la baja voluntaria no da derecho a paro. Hay excepciones, como un traslado o una modificación sustancial de condiciones que te perjudica, o ser víctima de violencia de género.'),
]
pagina('que-hacer-si-me-quedo-en-paro', 'Qué hacer si te quedas en paro: pasos y plazos (2026)',
    'Me he quedado en paro, ¿qué hago? Apúntate y pide el paro en 15 días hábiles, cobra el 70 % y luego el 60 % de 4 a 24 meses. Paso a paso, con la ley.',
    'qué hacer si me quedo en paro, cómo pedir el paro, plazo para pedir el paro, me he quedado sin trabajo qué hago',
    [('Guías', 'guias'), ('Qué hacer si te quedas en paro', None)], cuerpo, faqs,
    'Ley General de la Seguridad Social (arts. 262 a 273, en especial el 268), versión consolidada del BOE, y cuantías del SEPE para 2026.',
    menu_activo='Guías')
registrar('que-hacer-si-me-quedo-en-paro', 'Despido y fin del contrato', '🧭', 'Qué hacer si te quedas en paro',
          'Los pasos en orden: si tienes derecho, el plazo de 15 días, cuánto y cuánto tiempo cobrarás.')
print('creada: que-hacer-si-me-quedo-en-paro')
