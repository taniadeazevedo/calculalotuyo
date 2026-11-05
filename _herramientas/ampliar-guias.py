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

# Página → contenido nuevo
PAGINAS = {
    'despido-improcedente': DESPIDO_IMPROCEDENTE,
}

for pag, html in PAGINAS.items():
    f = f'{pag}.html'
    s = o = re.sub(r'\s*<!-- AMPLIADO -->.*?<!-- /AMPLIADO -->', '', open(f, encoding='utf-8').read(), flags=re.S)   # quita la versión anterior
    i = s.index('<article class="seo-section"')                     # el artículo principal de la página…
    fin = s.index('</article>', s.index('data-ampliado="1"', i) if 'data-ampliado="1"' in s else i) + len('</article>')   # …y su ampliación, si la tiene
    s = s[:fin] + f'\n        <!-- AMPLIADO -->\n        <article class="seo-section">{html}</article>\n        <!-- /AMPLIADO -->' + s[fin:]
    if s != open(f, encoding='utf-8').read(): open(f, 'w', encoding='utf-8').write(s)
print('páginas ampliadas:', len(PAGINAS))
