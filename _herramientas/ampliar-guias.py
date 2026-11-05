# Contenido propio en las calculadoras principales (05/11/2026), para que no parezcan «calculadora + texto genérico»
# (consejo de la auditoría antes de volver a pedir AdSense): casos con cifras, errores frecuentes, documentos y plazos,
# y cuándo pedir ayuda. Cada bloque va en su propio <article> entre <!-- AMPLIADO --> y <!-- /AMPLIADO -->,
# justo después del artículo principal de la página. Se puede lanzar las veces que haga falta: si ya está, lo sustituye.
# Uso: python3 _herramientas/ampliar-guias.py      (regenerar.sh lo lanza después de iconos.py)
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

ico = lambda n: f'<svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-{n}"/></svg>'   # icono de la web
eur = lambda x: f'{x:,.0f} €'.replace(',', '.')                                                # 4134.79 → «4.135 €»
dia = lambda anual: anual / 365                                                                 # salario diario (art. 56 ET)

# ---------------------------------------------------------------- DESPIDO IMPROCEDENTE
# Casos: (nombre, situación, sueldo bruto anual con pagas, meses trabajados)
CASOS_DI = [
    ('Laura', 'dependienta · 1.400 €/mes × 14 · 2 años y 4 meses', 1400 * 14, 28),
    ('Javier', 'técnico · 2.200 €/mes × 14 · 11 años', 2200 * 14, 132),
    ('Ana', 'comercial · 1.300 €/mes × 14 + 6.000 € de comisiones · 5 años', 1300 * 14 + 6000, 60),
]
filas_di = ''.join(
    f'<tr><td><strong>{n}</strong><br><small>{t}</small></td><td><strong>{eur(dia(a) * 33 * m / 12)}</strong></td>'
    f'<td>{eur(dia(a) * 20 * m / 12)}</td><td>{33 * m / 12:g}</td><td>{eur(dia(a))}</td></tr>'   # lo importante primero (en el móvil se ve sin deslizar)
    for n, t, a, m in CASOS_DI)
ana_sin = dia(1300 * 14) * 33 * 60 / 12                                                         # Ana olvidando las comisiones
ana_con = dia(1300 * 14 + 6000) * 33 * 60 / 12

DESPIDO_IMPROCEDENTE = f'''<h2>{ico('users')} Tres casos con cifras</h2>
<p>Para que veas cómo cambia la indemnización con el sueldo y la antigüedad. Todos con contrato posterior a 2012 y la indemnización legal mínima (tu convenio puede mejorarla):</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Caso</th><th>Improcedente</th><th>Si fuera objetivo</th><th>Días</th><th>Salario al día</th></tr></thead><tbody>{filas_di}</tbody></table></div>
<p>El caso de Ana es el que más se equivoca: si se calcula solo con el sueldo fijo salen <strong>{eur(ana_sin)}</strong>, pero las comisiones de los últimos 12 meses también cuentan y la cifra correcta es <strong>{eur(ana_con)}</strong>. Son {eur(round(ana_con) - round(ana_sin))} de diferencia.</p>

<h2>{ico('scale')} Readmisión o indemnización: quién decide</h2>
<ul>
<li><strong>Decide la empresa</strong>, no tú. Tiene <strong>5 días</strong> desde que le notifican la sentencia; si no dice nada, se entiende que te readmite (art. 56 del Estatuto).</li>
<li><strong>Si te readmite</strong>, además te paga los <strong>salarios de tramitación</strong>: el sueldo de los días que pasaron entre el despido y la sentencia.</li>
<li><strong>Si te indemniza</strong>, no hay salarios de tramitación. Esto es lo más habitual, y casi siempre se cierra antes, en la conciliación.</li>
<li><strong>Si eres representante de los trabajadores</strong> (delegado o comité), eliges tú.</li>
<li><strong>Ojo, no es lo mismo que un despido nulo.</strong> Si te despiden estando embarazada, de baja por nacimiento, con reducción de jornada por cuidado de hijos o por reclamar tus derechos, el despido puede ser <strong>nulo</strong>: la readmisión es obligatoria y te pagan los salarios de tramitación.</li>
</ul>

<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Dejar pasar los 20 días hábiles.</strong> Es un plazo de caducidad: si se pasa, ya no se puede reclamar. Presentar la papeleta de conciliación lo detiene.</li>
<li><strong>Calcular con el sueldo neto</strong> o sin las pagas extra. Se usa el <strong>bruto anual</strong> con las pagas y los complementos fijos.</li>
<li><strong>Olvidar lo variable:</strong> comisiones, pluses o incentivos que cobras con regularidad entran en el cálculo (con la media de los últimos 12 meses).</li>
<li><strong>Contar la antigüedad desde el último contrato.</strong> Si encadenaste contratos temporales con la misma empresa casi sin interrupción, la antigüedad puede contar desde el primero.</li>
<li><strong>Cobrar sin pasar por la conciliación.</strong> Si la empresa te paga los 33 días sin acta de conciliación ni sentencia, Hacienda puede hacerte pagar IRPF por la indemnización.</li>
<li><strong>Esperar a resolver el despido para pedir el paro.</strong> Tienes 15 días hábiles para pedirlo, y es compatible con reclamar.</li>
</ul>

<h2>{ico('folder-open')} Qué documentos tener a mano</h2>
<ul>
<li>La <strong>carta de despido</strong> (con la fecha y tu firma de «no conforme»).</li>
<li>Tu <strong>contrato</strong> o contratos, y las <strong>últimas 12 nóminas</strong>.</li>
<li>Tu <strong>vida laboral</strong>: se descarga gratis en la sede de la Seguridad Social y sirve para demostrar la antigüedad.</li>
<li>El <strong>finiquito</strong> y el justificante de lo que te hayan pagado.</li>
<li>Tu <strong>convenio colectivo</strong>: puede mejorar la indemnización o fijar otros complementos.</li>
<li>Correos, mensajes o avisos de la empresa sobre el despido o sus motivos.</li>
</ul>

<h2>{ico('handshake')} Cuándo pedir ayuda</h2>
<ul>
<li><strong>Abogado laboralista:</strong> si la carta no explica bien los motivos, si sospechas que el despido es nulo o si la cantidad es alta. Para el juicio, los trabajadores tienen derecho a <strong>abogado de oficio gratis</strong> sea cual sea su sueldo (Ley 1/1996 de asistencia jurídica gratuita, art. 2).</li>
<li><strong>Sindicato:</strong> asesoran sobre despidos y suelen acompañar en la conciliación (gratis o con descuento si estás afiliado).</li>
<li><strong>Inspección de Trabajo:</strong> sirve para denunciar impagos, horas sin cotizar o contratos fraudulentos, pero <strong>no decide si un despido es improcedente</strong>: eso lo hace el Juzgado de lo Social.</li>
</ul>'''

# ---------------------------------------------------------------- DESPIDO OBJETIVO
# Casos: (nombre, situación, sueldo bruto anual, días por 20/año sin tope)
CASOS_DO = [
    ('Laura', 'dependienta · 1.400 €/mes × 14 · 2 años y 4 meses', 1400 * 14, 20 * 28 / 12),
    ('Javier', 'técnico · 2.200 €/mes × 14 · 11 años', 2200 * 14, 20 * 11),
    ('Pedro', 'administrativo · 2.000 €/mes × 14 · 20 años', 2000 * 14, 20 * 20),
]
filas_do = ''.join(
    f'<tr><td><strong>{n}</strong><br><small>{t}</small></td><td><strong>{eur(dia(a) * min(d, 360))}</strong></td>'
    f'<td>{eur(dia(a) * min(d * 33 / 20, 720))}</td><td>{min(d, 360):g}{" (tope)" if d > 360 else ""}</td></tr>'
    for n, t, a, d in CASOS_DO)

DESPIDO_OBJETIVO = f'''<h2>{ico('users')} Tres casos con cifras</h2>
<p>La indemnización del despido objetivo es de <strong>20 días por año</strong> con un tope de <strong>12 mensualidades</strong> (360 días). El tope se alcanza a los 18 años de antigüedad, como le pasa a Pedro:</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Caso</th><th>Objetivo</th><th>Si fuera improcedente</th><th>Días</th></tr></thead><tbody>{filas_do}</tbody></table></div>
<p>La diferencia entre las dos columnas es lo que está en juego si reclamas y el juez dice que el despido no estaba justificado.</p>

<h2>{ico('clipboard-list')} Lo que la empresa tiene que cumplir</h2>
<p>El despido objetivo tiene requisitos de forma (art. 53 del Estatuto). Si la empresa se salta alguno, el despido puede declararse <strong>improcedente</strong> y pasar a 33 días por año:</p>
<ul>
<li><strong>Carta por escrito</strong> que explique la causa concreta: no basta con «causas económicas», tiene que decir cuáles.</li>
<li><strong>La indemnización, al mismo tiempo que la carta</strong> (normalmente por transferencia ese día). Solo puede retrasarla si la causa es económica y lo explica en la carta.</li>
<li><strong>15 días de preaviso.</strong> Si no lo da, te tiene que pagar esos días, pero el despido sigue siendo válido.</li>
<li><strong>Durante el preaviso</strong> tienes <strong>6 horas a la semana</strong> de permiso pagado para buscar trabajo.</li>
<li>Si hay representantes de los trabajadores, la empresa les tiene que dar una copia de la carta.</li>
</ul>

<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Pensar que cobrar la indemnización es aceptar el despido.</strong> Puedes cobrar los 20 días y reclamar a la vez: si ganas, te pagan la diferencia hasta los 33.</li>
<li><strong>Dejar pasar los 20 días hábiles</strong> para presentar la papeleta de conciliación. Es el mismo plazo que en cualquier despido.</li>
<li><strong>No comprobar el salario que usan.</strong> Tiene que ser el bruto anual con pagas extra y pluses fijos; si falta algo, la indemnización es menor de lo debido.</li>
<li><strong>Firmar «conforme».</strong> Firma con «no conforme» y la fecha: solo acreditas que la has recibido.</li>
</ul>

<h2>{ico('handshake')} Cuándo merece la pena reclamar</h2>
<ul>
<li>Si la carta es genérica y no explica <strong>qué pérdidas o qué cambios</strong> justifican el despido.</li>
<li>Si la empresa <strong>contrata a otra persona</strong> para tu puesto poco después.</li>
<li>Si no te dieron la indemnización con la carta o el cálculo es menor del que da esta calculadora.</li>
<li>Si te despiden estando embarazada, de baja por nacimiento o con reducción de jornada por cuidado de hijos: el despido podría ser <strong>nulo</strong>.</li>
</ul>
<p>Para el juicio, los trabajadores tienen derecho a <strong>abogado de oficio gratis</strong> sea cual sea su sueldo (Ley 1/1996, art. 2). Los sindicatos también asesoran y acompañan en la conciliación.</p>'''

# ---------------------------------------------------------------- FINIQUITO
FINIQUITO = f'''<h2>{ico('clipboard-list')} Qué tiene que llevar tu finiquito</h2>
<p>El finiquito es la liquidación de lo que la empresa te debe el día que terminas. Revisa que estén estas partidas:</p>
<ul>
<li><strong>Los días trabajados del último mes</strong> que todavía no has cobrado.</li>
<li><strong>Las vacaciones generadas y no disfrutadas</strong>: unos 2,5 días por mes trabajado en el año (con 30 días naturales al año).</li>
<li><strong>La parte proporcional de las pagas extra</strong>, si no las cobras prorrateadas cada mes.</li>
<li><strong>Horas extra, comisiones o pluses</strong> pendientes.</li>
<li><strong>Descuentos</strong>: el preaviso que no hayas dado (en una baja voluntaria), anticipos o lo que hayas cobrado de más.</li>
</ul>
<p>La <strong>indemnización por despido</strong> no forma parte del finiquito: si te corresponde, va aparte y no paga IRPF (dentro del límite legal). El finiquito sí tributa, como cualquier nómina.</p>

<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Firmar sin revisar.</strong> Si no estás de acuerdo, firma con «<strong>no conforme</strong>» y la fecha: así cobras lo que te dan y puedes reclamar el resto.</li>
<li><strong>Olvidar las vacaciones del año en curso.</strong> Es la partida que más se «pierde».</li>
<li><strong>Contar dos veces las pagas extra</strong> cuando ya las cobras prorrateadas en la nómina.</li>
<li><strong>No dar el preaviso en una baja voluntaria.</strong> Si tu convenio lo exige (lo normal es 15 días), la empresa puede descontarte los días que falten.</li>
<li><strong>Pensar que firmar el finiquito te impide reclamar.</strong> Si hay un error en las cifras, se puede reclamar igualmente.</li>
</ul>

<h2>{ico('alarm-clock')} Plazos y derechos</h2>
<ul>
<li><strong>Un año</strong> para reclamar cantidades que te deban (art. 59 del Estatuto), contado desde el día en que terminó el contrato.</li>
<li>Puedes pedir que un <strong>representante de los trabajadores</strong> esté presente cuando firmes (art. 49 del Estatuto).</li>
<li>La empresa tiene que darte el <strong>certificado de empresa</strong> (lo envía al SEPE) para que puedas pedir el paro, si te corresponde.</li>
</ul>

<h2>{ico('folder-open')} Qué documentos tener a mano</h2>
<ul>
<li>Tu <strong>contrato</strong> y las <strong>últimas nóminas</strong>, para comprobar el sueldo y si las pagas van prorrateadas.</li>
<li>Un registro de las <strong>vacaciones</strong> que ya has disfrutado este año (correos, solicitudes, el portal del empleado).</li>
<li>Tu <strong>convenio colectivo</strong>: fija los días de preaviso, las pagas extra y cuándo se generan.</li>
<li>La carta de despido o tu carta de baja voluntaria, con la fecha.</li>
</ul>'''

# ---------------------------------------------------------------- BAJA MÉDICA
BR = 1800 / 30                                                      # base reguladora diaria del ejemplo
BAJA_COMUN = 17 * BR * 0.60 + 10 * BR * 0.75                        # 30 días por enfermedad común
BAJA_ACC = 30 * BR * 0.75                                           # 30 días por accidente de trabajo
BAJA_MEDICA = f'''<h2>{ico('users')} El mismo mes de baja, dos casos</h2>
<p>Marta tiene una base de cotización de 1.800 € al mes ({eur(BR)} al día) y su convenio no complementa la baja. Está de baja 30 días:</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Motivo</th><th>Total</th></tr></thead><tbody>
<tr><td><strong>Enfermedad común</strong><br><small>días 1-3: nada · 4-20: 17 × {eur(BR * 0.6)} · 21-30: 10 × {eur(BR * 0.75)}</small></td><td><strong>{eur(BAJA_COMUN)}</strong></td></tr>
<tr><td><strong>Accidente de trabajo</strong><br><small>30 × {eur(BR * 0.75)} (75 % desde el primer día)</small></td><td><strong>{eur(BAJA_ACC)}</strong></td></tr>
</tbody></table></div>
<p>Son cantidades brutas: luego se restan el IRPF y la Seguridad Social, como en una nómina normal.</p>

<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Llevar el parte a la empresa.</strong> Desde abril de 2023 no hace falta: el médico lo envía directamente a la Seguridad Social y esta avisa a la empresa.</li>
<li><strong>Dar por perdidas las vacaciones.</strong> Si la baja coincide con tus vacaciones, las conservas y puedes cogerlas después, hasta 18 meses desde el final del año en que se generaron (art. 38 del Estatuto).</li>
<li><strong>No mirar el convenio.</strong> Muchos complementan la baja hasta el 100 % del sueldo, a veces desde el primer día.</li>
<li><strong>Faltar a una revisión de la mutua o del INSS</strong> sin justificarlo: te pueden suspender la prestación.</li>
</ul>

<h2>{ico('scale')} Si no estás de acuerdo con el alta</h2>
<ul>
<li>Si el <strong>INSS</strong> te da el alta y crees que no puedes trabajar, puedes presentar una <strong>disconformidad en 4 días naturales</strong> ante la inspección médica de tu comunidad. Mientras se resuelve, tienes que reincorporarte.</li>
<li>Si la <strong>mutua</strong> propone el alta, la decisión final es de tu médico de cabecera o de la inspección médica.</li>
<li>Una baja dura como máximo <strong>365 días</strong>, prorrogables otros 180 si se prevé que te vas a curar.</li>
</ul>

<h2>{ico('handshake')} Si te despiden estando de baja</h2>
<p>Estar de baja no impide que te despidan, pero si el motivo real es la enfermedad, el despido puede ser <strong>nulo</strong> por discriminación (Ley 15/2022): la empresa tendría que readmitirte y pagarte los salarios que no cobraste. Tienes 20 días hábiles para reclamar, y aquí merece la pena consultar con un abogado laboralista o un sindicato. Lo explicamos en <a href="despido-estando-de-baja">despido estando de baja</a>.</p>'''

# ---------------------------------------------------------------- JUBILACIÓN
JUBILACION = f'''<h2>{ico('clipboard-list')} Antes de pedirla: revisa tu vida laboral</h2>
<p>La pensión sale de lo que la Seguridad Social tiene registrado. Un error ahí cuesta dinero todos los meses, así que conviene revisarlo con tiempo:</p>
<ul>
<li>Descarga tu <strong>informe de vida laboral</strong> y tu <strong>informe de bases de cotización</strong> en la sede de la Seguridad Social (con Cl@ve o certificado digital). Son gratis.</li>
<li>Comprueba que estén <strong>todos tus trabajos</strong> y que las fechas cuadren con tus contratos. Los años en el extranjero, la mili o el servicio social y los cuidados de hijos pueden sumar en algunos casos.</li>
<li>Si falta algo, reclámalo con contratos o nóminas antes de jubilarte: después cuesta más.</li>
<li>Usa el <strong>simulador de jubilación</strong> de «Tu Seguridad Social»: con tus bases reales da una cifra más exacta que cualquier calculadora.</li>
</ul>

<h2>{ico('alarm-clock')} Cuándo y cómo pedirla</h2>
<ul>
<li>Puedes presentar la solicitud <strong>hasta 3 meses antes</strong> de la fecha en que quieres jubilarte, por internet o en un centro de la Seguridad Social.</li>
<li>Si la pides <strong>dentro de los 3 meses siguientes</strong> a dejar de trabajar, la cobras desde el día siguiente al cese. Si tardas más, solo te pagan con efectos de los 3 meses anteriores a la solicitud: el resto se pierde.</li>
<li>La pensión se cobra en <strong>14 pagas</strong> (las extra en junio y noviembre) y sube cada enero con el IPC medio.</li>
</ul>

<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Jubilarse un mes antes de tiempo.</strong> En la anticipada, la reducción se aplica por cada mes que adelantas: a veces esperar uno o dos meses cambia mucho la pensión.</li>
<li><strong>No contar las lagunas.</strong> Los meses sin cotizar dentro del periodo de cálculo se rellenan con la base mínima (o la mitad), y bajan la base reguladora.</li>
<li><strong>Olvidar que la pensión tributa.</strong> Paga IRPF como un sueldo, y con otro ingreso puede obligarte a hacer la renta.</li>
<li><strong>Pensar que jubilarse es dejar de trabajar del todo.</strong> Con la jubilación activa o la <a href="jubilacion-flexible">jubilación flexible</a> puedes compaginar pensión y trabajo.</li>
</ul>

<h2>{ico('handshake')} Dónde pedir ayuda</h2>
<p>Los <strong>centros de atención de la Seguridad Social</strong> (CAISS) revisan tu caso gratis con cita previa. Si te deniegan la pensión o no estás de acuerdo con la cantidad, tienes <strong>30 días</strong> para presentar una reclamación previa antes de ir al juzgado; ahí ya conviene un abogado o un sindicato.</p>'''

# ---------------------------------------------------------------- PARO
PARO = f'''<h2>{ico('triangle-alert')} Errores que cuestan días de paro</h2>
<ul>
<li><strong>Pedirlo tarde.</strong> Tienes <strong>15 días hábiles</strong> desde el día siguiente al despido o al fin del contrato. Si lo pides después, no lo pierdes, pero pierdes los días de retraso.</li>
<li><strong>Esperar a la conciliación o al juicio.</strong> Puedes pedir el paro y reclamar el despido a la vez.</li>
<li><strong>Irte de vacaciones sin avisar.</strong> Si sales de España tienes que comunicarlo. Hasta 15 días al año no afecta a tu prestación; más tiempo, la suspende.</li>
<li><strong>No renovar la demanda de empleo</strong> en la fecha que te dan o no ir a una cita: pueden quitarte un mes de paro.</li>
<li><strong>Rechazar una oferta de empleo adecuada</strong> o un curso: también tiene sanción.</li>
<li><strong>Trabajar unas horas sin avisar.</strong> Un trabajo a tiempo parcial es compatible con el paro, pero hay que comunicarlo y se cobra la parte proporcional.</li>
</ul>

<h2>{ico('folder-open')} Qué documentos necesitas</h2>
<ul>
<li><strong>DNI o NIE</strong> y tu número de cuenta.</li>
<li>El <strong>certificado de empresa</strong>: lo envía la empresa directamente al SEPE. Si no lo ha hecho, pídeselo.</li>
<li>Si tienes hijos a cargo, el <strong>libro de familia</strong> o el certificado de nacimiento: sube el tope de lo que cobras.</li>
<li>Estar inscrita o inscrito como <strong>demandante de empleo</strong> en tu servicio autonómico de empleo.</li>
</ul>

<h2>{ico('scale')} Si te lo deniegan o te pagan menos</h2>
<ul>
<li>Revisa la resolución: muchas veces es un dato que falta (un contrato que no aparece, días cotizados sin contar).</li>
<li>Tienes <strong>30 días hábiles</strong> para presentar una <strong>reclamación previa</strong> ante el SEPE. Si la rechazan, puedes ir al Juzgado de lo Social.</li>
<li>Los sindicatos y las oficinas de empleo te ayudan a prepararla. Para el juicio tienes derecho a abogado de oficio gratis.</li>
</ul>

<h2>{ico('lightbulb')} Lo que poca gente sabe</h2>
<ul>
<li>El paro <strong>tributa en el IRPF</strong>. Si en el año has tenido dos pagadores (tu empresa y el SEPE), puede que tengas que hacer la renta: míralo en <a href="obligado-a-declarar-renta">¿tengo que hacer la renta?</a></li>
<li>Mientras cobras el paro, el SEPE <strong>cotiza por ti para la jubilación</strong>.</li>
<li>Si encuentras trabajo y lo vuelves a perder antes de agotar el paro, puedes <strong>reanudar</strong> el que te quedaba.</li>
</ul>'''

# ---------------------------------------------------------------- IRPF
IRPF = f'''<h2>{ico('triangle-alert')} Errores frecuentes con la retención</h2>
<ul>
<li><strong>Confundir tu retención con tu tramo.</strong> Que ganes 30.000 € no significa que te quiten un 30 %: los tramos se aplican por partes y, con el mínimo personal, la retención se queda en torno al 16 %.</li>
<li><strong>No avisar a la empresa cuando cambia tu situación.</strong> Si tienes un hijo, te separas o te reconocen una discapacidad, rellena de nuevo el <strong>modelo 145</strong>. Si no, te retienen de más (o de menos) todo el año.</li>
<li><strong>Tener dos pagadores y no hacer cuentas.</strong> Si has cambiado de trabajo o has cobrado el paro, cada pagador retiene como si fuera el único. Lo normal es que en la renta te salga a pagar.</li>
<li><strong>Pensar que una subida de sueldo te deja con menos dinero.</strong> No pasa: solo tributa más la parte que supera cada tramo. Lo explicamos en la <a href="sueldo-neto">calculadora de sueldo neto</a>.</li>
<li><strong>Olvidar los contratos cortos.</strong> Con un contrato temporal de menos de un año, la retención mínima es del <strong>2 %</strong> aunque ganes poco.</li>
</ul>

<h2>{ico('pen-line')} Cómo cambiar tu retención</h2>
<ul>
<li><strong>Para que te retengan más</strong> (y no te toque pagar en la renta): pídelo por escrito a tu empresa indicando el porcentaje. La ley lo permite siempre.</li>
<li><strong>Para que te retengan menos</strong>: no se puede pedir un porcentaje a la carta. Lo que sí puedes es actualizar el modelo 145 con tus datos reales (hijos, ascendientes, discapacidad, hipoteca anterior a 2013) para que la empresa lo recalcule.</li>
<li>Los cambios se aplican a partir de la siguiente nómina, y la empresa <strong>regulariza</strong> el resto del año: por eso a veces el porcentaje cambia a mitad de año.</li>
</ul>

<h2>{ico('folder-open')} Dónde mirar tus datos</h2>
<ul>
<li><strong>En la nómina:</strong> el porcentaje aparece en la línea «Retención IRPF» y la base sobre la que se aplica.</li>
<li><strong>En el certificado de retenciones</strong> que te da la empresa a principios de año: lo que cobraste y lo que te retuvieron en total.</li>
<li><strong>En los datos fiscales</strong> de la Agencia Tributaria (con Cl@ve) desde marzo: ahí ves todos tus pagadores antes de hacer la renta.</li>
</ul>'''

# ---------------------------------------------------------------- SUELDO NETO
SUELDO_NETO = f'''<h2>{ico('triangle-alert')} Errores frecuentes al comparar sueldos</h2>
<ul>
<li><strong>Comparar ofertas por el sueldo al mes.</strong> 2.000 € en 14 pagas y 2.333 € en 12 pagas son el mismo sueldo: <strong>28.000 € al año</strong>. Compara siempre el bruto anual.</li>
<li><strong>Olvidar lo que no es dinero.</strong> El seguro médico, los tickets restaurante o el coche de empresa son retribución en especie: pueden subir tu IRPF aunque no cobres más en la cuenta.</li>
<li><strong>Esperar el mismo neto todos los meses.</strong> Si te suben el sueldo a mitad de año o cobras un bonus, la empresa recalcula la retención y el neto de los meses siguientes puede bajar un poco.</li>
<li><strong>Pensar que las pagas extra tributan más.</strong> Llevan el mismo porcentaje de IRPF que el resto; parecen menores porque en muchas nóminas no llevan pluses.</li>
</ul>

<h2>{ico('search')} Si tu nómina no cuadra con la calculadora</h2>
<ol>
<li><strong>Compara el bruto.</strong> En la nómina pueden sumar horas extra, pluses o especie que aquí no has puesto.</li>
<li><strong>Mira el porcentaje de IRPF.</strong> Si es muy distinto, puede que la empresa no tenga tus datos actualizados (modelo 145).</li>
<li><strong>Revisa la Seguridad Social.</strong> Debe ser el 6,50 % (6,55 % con contrato temporal) de tu base de cotización, que incluye la parte proporcional de las pagas extra.</li>
<li><strong>Consulta tu convenio</strong> para ver si cobras lo que te corresponde por tu categoría.</li>
<li><strong>Pregunta a tu empresa</strong> por escrito. Si te deben dinero, tienes <strong>un año</strong> para reclamarlo (art. 59 del Estatuto).</li>
</ol>'''

# ---------------------------------------------------------------- CUOTA DE AUTÓNOMOS
CUOTA_AUTONOMOS = f'''<h2>{ico('triangle-alert')} Errores frecuentes</h2>
<ul>
<li><strong>Elegir el tramo más bajo «por si acaso».</strong> Si al final ganas más, la Seguridad Social te reclama la diferencia de golpe al año siguiente, en la regularización.</li>
<li><strong>No cambiar el tramo cuando cambian tus ingresos.</strong> Puedes cambiarlo <strong>hasta 6 veces al año</strong> desde Import@ss. Hacerlo a tiempo evita sustos en la regularización.</li>
<li><strong>Confundir la cuota con los impuestos.</strong> La cuota es la Seguridad Social. El IRPF (modelo 130) y el IVA (modelo 303) se pagan aparte, cada trimestre, a Hacienda.</li>
<li><strong>No contar la cuota como gasto.</strong> Lo que pagas de autónomos se resta de tus ingresos en el IRPF.</li>
<li><strong>Dejar un recibo sin pagar.</strong> Tiene un recargo del 10 % si lo pagas el mes siguiente y del 20 % después. Además, con deudas puedes perder la tarifa plana y las ayudas.</li>
</ul>

<h2>{ico('alarm-clock')} Plazos que conviene tener claros</h2>
<ul>
<li><strong>Alta:</strong> en Hacienda (modelo 036 o 037) y en la Seguridad Social <strong>antes de empezar</strong> a trabajar. La tarifa plana hay que pedirla en el momento del alta.</li>
<li><strong>La cuota</strong> se cobra por domiciliación el último día hábil de cada mes.</li>
<li><strong>Los impuestos trimestrales</strong> se presentan del 1 al 20 de abril, julio y octubre, y del 1 al 30 de enero.</li>
<li><strong>La regularización</strong> llega cuando Hacienda pasa tus ingresos reales a la Seguridad Social, normalmente en la segunda mitad del año siguiente.</li>
</ul>

<h2>{ico('handshake')} Dónde pedir ayuda</h2>
<p>Las <strong>cámaras de comercio</strong> y los puntos PAE (Punto de Atención al Emprendedor) te ayudan a darte de alta gratis. Muchos ayuntamientos y comunidades tienen servicios de asesoramiento para nuevos autónomos. Para la contabilidad y los impuestos de cada trimestre, una gestoría suele costar entre 40 y 80 € al mes.</p>'''

# Página → contenido nuevo
PAGINAS = {
    'despido-improcedente': DESPIDO_IMPROCEDENTE,
    'despido-objetivo': DESPIDO_OBJETIVO,
    'finiquito': FINIQUITO,
    'baja-medica': BAJA_MEDICA,
    'jubilacion': JUBILACION,
    'paro': PARO,
    'irpf': IRPF,
    'sueldo-neto': SUELDO_NETO,
    'cuota-autonomos': CUOTA_AUTONOMOS,
}

for pag, html in PAGINAS.items():
    f = f'{pag}.html'
    s = o = re.sub(r'\s*<!-- AMPLIADO -->.*?<!-- /AMPLIADO -->', '', open(f, encoding='utf-8').read(), flags=re.S)   # quita la versión anterior
    i = s.index('<article class="seo-section"')                     # el artículo principal de la página…
    fin = s.index('</article>', s.index('data-ampliado="1"', i) if 'data-ampliado="1"' in s else i) + len('</article>')   # …y su ampliación, si la tiene
    s = s[:fin] + f'\n        <!-- AMPLIADO -->\n        <article class="seo-section">{html}</article>\n        <!-- /AMPLIADO -->' + s[fin:]
    if s != open(f, encoding='utf-8').read(): open(f, 'w', encoding='utf-8').write(s)
print('páginas ampliadas:', len(PAGINAS))
