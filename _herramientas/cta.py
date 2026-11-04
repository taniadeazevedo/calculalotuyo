# Recuadro «Calcula tu…» al principio de cada página de contenido (03/11/2026, consejo de un consultor SEO):
# quien llega desde Google a una guía, un caso o un modelo tiene la calculadora de su tema a mano, sin bajar hasta el final.
#   · Casos, novedades y «qué hacer si…»: justo después del resumen «En 30 segundos».
#   · Guías y datos (SMI, IPREM): al principio del contenido, tras el índice.
#   · Modelos: debajo de los botones de descarga.
# Para añadir una página, se pone en PAGINAS con su calculadora. Se puede lanzar las veces que haga falta.
# Uso: python3 _herramientas/cta.py      (regenerar.sh lo lanza después de los iconos)
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

# Texto del botón de cada calculadora
TEXTO = {
    'despido-improcedente': 'Calcula tu indemnización por despido', 'sueldo-neto': 'Calcula tu sueldo neto',
    'paro': 'Calcula cuánto paro te corresponde', 'finiquito': 'Calcula tu finiquito',
    'cuota-autonomos': 'Calcula tu cuota de autónomos', 'baja-medica': 'Calcula lo que cobras de baja',
    'vacaciones': 'Calcula tus días de vacaciones', 'reduccion-jornada': 'Calcula tu sueldo con jornada reducida',
    'facturas': 'Calcula el IVA y la retención de tu factura', 'horas-extra': 'Calcula tus horas extra',
    'jubilacion': 'Calcula cuándo y cuánto cobrarás al jubilarte', 'irpf': 'Calcula tu retención de IRPF',
    'subida-ipc': 'Calcula cuánto debería subir tu sueldo', 'dias-laborables': 'Calcula tus días laborables',
    'obligado-a-declarar-renta': 'Comprueba si tienes que hacer la renta',
}
# Página → calculadora de su tema
PAGINAS = {
    # guías y datos
    'guia-despido': 'despido-improcedente', 'guia-despido-disciplinario': 'despido-improcedente', 'guia-sueldo-neto': 'sueldo-neto',
    'guia-nomina': 'sueldo-neto', 'guia-paro': 'paro', 'guia-finiquito': 'finiquito', 'guia-baja-voluntaria': 'finiquito',
    'guia-contratos': 'finiquito', 'guia-autonomos': 'cuota-autonomos', 'guia-baja-medica': 'baja-medica',
    'guia-permisos': 'vacaciones', 'guia-nacimiento': 'reduccion-jornada', 'smi-2026': 'sueldo-neto', 'iprem-2026': 'paro',
    # modelos
    'modelo-carta-baja-voluntaria': 'finiquito', 'modelo-baja-periodo-de-prueba': 'finiquito', 'modelo-reclamacion-cantidades': 'finiquito',
    'modelo-factura-autonomo': 'facturas', 'modelo-factura-rectificativa': 'facturas', 'modelo-presupuesto-autonomo': 'facturas',
    'modelo-solicitud-reduccion-jornada': 'reduccion-jornada', 'modelo-adaptacion-jornada': 'reduccion-jornada',
    'modelo-solicitud-vacaciones': 'vacaciones', 'modelo-permiso-retribuido': 'vacaciones', 'modelo-registro-jornada': 'horas-extra',
    'modelo-plantilla-nomina': 'sueldo-neto',
    # novedades
    'subida-pensiones-2027': 'jubilacion', 'elecciones-29n-pensiones-smi-2027': 'jubilacion', 'deduccion-alquiler-renta': 'obligado-a-declarar-renta',
    'ipc-actual': 'subida-ipc', 'festivos-2027': 'dias-laborables',
    # casos concretos y «qué hacer si…»
    'que-hacer-si-voy-a-tener-un-hijo': 'reduccion-jornada', 'que-hacer-si-me-quedo-en-paro': 'paro', 'baja-15-dias-cuanto-cobro': 'baja-medica',
    'que-es-el-finiquito': 'finiquito', 'paro-tras-contrato-temporal': 'paro', 'cuando-se-cobra-el-paro': 'paro',
    'despido-estando-de-baja': 'despido-improcedente', 'paro-e-indemnizacion-a-la-vez': 'despido-improcedente',
    'baja-voluntaria-tengo-paro': 'finiquito', 'tarifa-plana-autonomos-2026': 'cuota-autonomos',
}
FLECHA = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
def recuadro(calc):
    return (f'<!-- CTA --><a class="cta-calc" href="{calc}"><span class="cta-calc-texto"><strong>{TEXTO[calc]}</strong>'
            f'<span>Con tus datos, en un minuto. Gratis y sin registro.</span></span><span class="cta-calc-boton">Calcular {FLECHA}</span></a><!-- /CTA -->')

hechas, sin_sitio = 0, []
for pag, calc in PAGINAS.items():
    f = f'{pag}.html'
    if not os.path.exists(f): sin_sitio.append(pag + ' (no existe)'); continue
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- CTA -->.*?<!-- /CTA -->\n?', '', s, flags=re.S)          # fuera el de una pasada anterior
    caja = recuadro(calc) + '\n'
    m = re.search(r'<div class="respuesta-corta">.*?</ul></div>\n?', s, re.S)       # 1) tras «En 30 segundos»
    if m: s = s[:m.end()] + caja + s[m.end():]
    elif (m := re.search(r'<div class="guide-content">\s*<div class="container">\n?', s)):   # 2) guías: al principio del contenido
        s = s[:m.end()] + caja + s[m.end():]
    elif (m := re.search(r'<div class="doc-cabecera">', s)):                     # 3) modelos: bajo las descargas
        s = s[:m.start()] + caja + s[m.start():]
    else: sin_sitio.append(pag); continue
    if s != o: open(f, 'w', encoding='utf-8').write(s)
    hechas += 1
print('recuadros «Calcula tu…»:', hechas, 'páginas' + (' · sin sitio: ' + ', '.join(sin_sitio) if sin_sitio else ''))
