# Formularios más sencillos (20/10/2026). Se lanza UNA vez sobre las calculadoras hechas a mano:
#  1) pasa los campos poco usados a «Más opciones» (un desplegable cerrado; siguen teniendo su valor por defecto)
#  2) cambia las palabras técnicas por otras normales
# Si una página ya tiene «Más opciones», no la vuelve a tocar. Uso: python3 _herramientas/formularios.py
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

# Página → campos que van a «Más opciones»
MOVER = {
    'finiquito': ['tipoPagas', 'diasVacAnuales', 'irpf'],
    'horas-extra': ['horasContrato', 'recargo', 'horasAcumuladas', 'compensacion'],
    'ere': ['topeMeses', 'edad', 'convenioSS'],
    'despido-objetivo': ['causa'],
    'pagas-extra': ['devengo'],
    'sueldo-neto': ['contrato', 'edad'],
    'irpf': ['hijosMenores3', 'discapacidad', 'ascendientes', 'edad'],
    'reduccion-jornada': ['horas', 'contrato'],
    'neto-a-bruto': ['contrato'],
    'facturas': ['gastos'],
}
CASADO = [('Casado/a (1 perceptor)', 'Casado/a (solo cobra uno de los dos)'), ('Casado/a (2 perceptores)', 'Casado/a (cobráis los dos)'),
          ('Casado/a - un perceptor de rentas', 'Casado/a (solo cobra uno de los dos)'), ('Casado/a - dos perceptores', 'Casado/a (cobráis los dos)'),
          ('Temporal (&lt;1 año)', 'Temporal (menos de 1 año)')]
EMPEZASTE = ('¿Cuándo empezaste en la empresa?')
# Página → [(texto técnico, texto normal)]
TEXTOS = {
    'despido-improcedente': [('>Salario bruto anual (con pagas)<', '>Sueldo bruto al año (con las pagas extra)<'), ('Incluye pagas extra prorrateadas', 'Lo que cobras al año antes de descuentos'),
                             ('>Fecha inicio contrato<', f'>{EMPEZASTE}<'), ('>Fecha despido<', '>¿Qué día te despidieron?<'),
                             ('>Tipo de contrato<', '>¿Empezaste antes del 12 de febrero de 2012?<'), ('Desde 12/02/2012 (33 días/año)', 'No (33 días por año)'),
                             ('Anterior 12/02/2012 (45+33 días)', 'Sí (45 días por año hasta 2012 y 33 después)')],
    'despido-objetivo': [('>Salario bruto anual (con pagas extra)<', '>Sueldo bruto al año (con las pagas extra)<'), ('>Fecha de inicio del contrato<', f'>{EMPEZASTE}<'),
                         ('>Fecha efectiva del despido<', '>¿Qué día es el despido?<'), ('>Causa del despido objetivo<', '>Motivo que da la empresa<')],
    'ere': [('>Salario bruto anual (con pagas)<', '>Sueldo bruto al año (con las pagas extra)<'), ('>Fecha inicio contrato<', f'>{EMPEZASTE}<'),
            ('>Fecha efectiva del ERE<', '>¿Qué día sales de la empresa?<'), ('>Días/año pactados en el ERE<', '>¿Cuántos días por año trabajado os pagan?<'),
            ('>¿Hay tope de mensualidades?<', '>¿Hay un máximo pactado?<'), ('>Edad del trabajador<', '>Tu edad<'),
            ('>¿Incluye convenio especial SS?<', '>¿La empresa te paga la Seguridad Social hasta jubilarte?<')],
    'finiquito': [('>Salario bruto mensual<', '>Sueldo bruto al mes<'), ('>Fecha de alta en la empresa<', f'>{EMPEZASTE}<'),
                  ('>Fecha de baja (último día)<', '>¿Cuál es tu último día?<'), ('>Motivo de la baja<', '>¿Por qué te vas?<'),
                  ('>Tipo de pagas extra<', '>¿Cuántas pagas cobras al año?<'), ('>12 pagas (prorrateadas)<', '>12 pagas (las extra van incluidas cada mes)<'),
                  ('>Días de vacaciones anuales<', '>Días de vacaciones al año<'), ('>Retención IRPF de tu nómina (%)<', '>% de IRPF que te quitan en la nómina<')],
    'horas-extra': [('Con las pagas extra prorrateadas (bruto anual ÷ 12)', 'Tu sueldo bruto al año dividido entre 12'), ('>Horas extra realizadas<', '>¿Cuántas horas extra has hecho?<'),
                    ('>Tipo de hora extra<', '>¿Cuándo las hiciste?<'), ('>Recargo según convenio<', '>¿Cuánto más te pagan por hora extra?<'),
                    ('>Horas semanales de contrato<', '>Horas a la semana de tu contrato<'), ('>¿Compensación en tiempo libre?<', '>¿Te las pagan o te dan horas libres?<'),
                    ('>Compensación en tiempo (4 meses)<', '>Horas libres (en los 4 meses siguientes)<')],
    'pagas-extra': [('>Salario base mensual<', '>Sueldo base al mes<'), ('Sin complementos variables ni pagas', 'El «salario base» de tu nómina, sin pluses'),
                    ('>Fecha de inicio en la empresa<', f'>{EMPEZASTE}<'), ('>Fecha de cálculo<', '>¿Hasta qué día calculamos?<'),
                    ('>Número de pagas anuales<', '>¿Cuántas pagas cobras al año?<'), ('>12 pagas (prorrateadas)<', '>12 pagas (las extra van incluidas cada mes)<'),
                    ('>Periodo de devengo<', '>¿Qué meses cuentan para cada paga?<'), ('>Semestral (lo habitual)<', '>Cada paga, 6 meses (lo habitual)<'),
                    ('>Anual (todo el año)<', '>Cada paga, 12 meses<'),
                    ('Semestral: ene-jun y jul-dic · Anual: verano jul-jun, navidad ene-dic', 'Lo habitual: la de verano por enero–junio y la de Navidad por julio–diciembre. Lo dice tu convenio')],
    'vacaciones': [('>Salario bruto mensual<', '>Sueldo bruto al mes<'), ('Para calcular valor económico', 'Para saber cuánto valen en dinero'),
                   ('>Días vacaciones según convenio (al año)<', '>¿Cuántos días de vacaciones tienes al año?<'), ('>Fecha inicio en empresa<', f'>{EMPEZASTE}<'),
                   ('>Fecha de cálculo<', '>¿Hasta qué día calculamos?<'), ('>¿Tipo de días?<', '>¿Tus días son naturales o laborables?<'),
                   ('>Días naturales<', '>Naturales (cuentan sábados y domingos)<'), ('>Días laborables<', '>Laborables (solo de lunes a viernes)<')],
    'subida-ipc': [('>Salario bruto anual actual<', '>Sueldo bruto al año<'), ('>IPC a aplicar (%)<', '>¿Qué año de IPC?<'),
                   ('>¿Subida que te han ofrecido?<', '>¿Cuánto te han ofrecido subir? (%)<')],
    'sueldo-neto': [('>Salario bruto anual<', '>Sueldo bruto al año<'), ('>Número de pagas<', '>¿Cuántas pagas al año?<'), ('>Situación personal<', '>Tu situación<')] + CASADO,
    'irpf': [('>Ingresos brutos anuales<', '>Sueldo bruto al año<'), ('>Situación familiar<', '>Tu situación<'), ('>Número de hijos menores de 25 años<', '>Hijos menores de 25 años<'),
             ('>Ascendientes a cargo (+65 años)<', '>Padres o abuelos mayores de 65 que viven contigo<'), ('>Discapacidad del contribuyente<', '>¿Tienes alguna discapacidad?<'),
             ('>Edad del contribuyente<', '>Tu edad<')] + CASADO,
    'reduccion-jornada': [('>Salario bruto anual a jornada completa<', '>Sueldo bruto al año a jornada completa<'), ('>Reducción de jornada (%)<', '>¿Cuánto quieres reducir? (%)<'),
                          ('>Número de pagas<', '>¿Cuántas pagas al año?<'), ('>Situación personal<', '>Tu situación<')] + CASADO,
    'neto-a-bruto': [('>Número de pagas<', '>¿Cuántas pagas al año?<'), ('>Situación personal<', '>Tu situación<')] + CASADO,
    'baja-medica': [('>Base de cotización del mes anterior<', '>Sueldo bruto del mes anterior a la baja<')],
    'cuota-autonomos': [('>Rendimiento neto mensual (€)<', '>¿Cuánto ganas al mes? (ingresos menos gastos)<'),
                        ('Ingresos - gastos deducibles', 'Lo que facturas menos los gastos del negocio, sin IVA'), ('>Tipo de autónomo<', '>¿Cómo trabajas?<')],
    'facturas': [('>Base imponible (tus honorarios)<', '>Importe de tu trabajo (sin IVA)<'), ('>Suplidos (pagos hechos en nombre del cliente)<', '>Gastos que pagaste por el cliente (suplidos)<')],
}

def grupo(s, campo):
    """Devuelve (inicio, fin) del <div class="form-group"> que contiene el campo con ese id."""
    i = s.index(f'id="{campo}"')
    ini = s.rindex('<div class="form-group"', 0, i)
    n, j = 0, ini
    for m in re.finditer(r'<div\b|</div>', s[ini:]):                 # cuenta los <div> abiertos hasta cerrar el grupo
        n += 1 if m.group(0) == '<div' else -1
        if n == 0:
            return ini, ini + m.end()
    raise ValueError(campo)

for pag in sorted(set(MOVER) | set(TEXTOS)):
    f = f'{pag}.html'
    s = o = open(f, encoding='utf-8').read()
    ini_form, fin_form = s.index('<form id="calc">'), s.index('</form>')
    form = s[ini_form:fin_form]
    for a, b in TEXTOS.get(pag, []):                                   # 2) palabras normales (solo dentro del formulario)
        if a in form: form = form.replace(a, b)
        else: print(f'  aviso: «{a}» no está en {pag}')
    if pag in MOVER and 'mas-opciones' not in form:                   # 1) «Más opciones»
        sacados = []
        for campo in MOVER[pag]:
            i, j = grupo(form, campo)
            sacados.append(form[i:j]); form = form[:i] + form[j:]
        caja = '<details class="mas-opciones"><summary>Más opciones (si no las tocas, usamos lo habitual)</summary><div class="form-grid">' + ''.join(sacados) + '</div></details>\n'
        # va justo después de la cuadrícula principal: delante del aviso o del botón, lo que aparezca antes
        pos = min(p for p in (form.find('<div class="disclaimer-box">'), form.find('<button type="submit"')) if p != -1)
        form = form[:pos] + caja + form[pos:]
    s = s[:ini_form] + form + s[fin_form:]
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); print('cambiada:', pag)
