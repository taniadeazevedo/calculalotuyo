# Títulos, descripciones y preguntas pensados para cómo busca la gente (según Search Console, 22/10/2026):
# «calcular…», «calculadora…», con la cifra que responde en la descripción, para que se haga clic.
# Se lanza después de generar las páginas (regenerar.sh) y se puede repetir sin duplicar nada.
# Las cifras son de 2026: revisar en enero junto con las demás. Uso: python3 _herramientas/titulos.py
import json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web
FLECHA = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
limpio = lambda t: re.sub(r'<[^>]+>', '', t)

# Página → (título, descripción). Títulos de 60 caracteres como mucho; descripciones de 160.
TITULOS = {
    'guia-paro': ('Paro 2026: cuánto cobras, cuánto dura y requisitos',
                  'Cobras el 70 % de tu base los 6 primeros meses y el 60 % después (máximo 1.225 € sin hijos). Cuánto dura según lo cotizado y cómo pedirlo.'),
    'despido-objetivo': ('Despido objetivo 2026: calcula tu indemnización (20 días)',
                         '20 días por año trabajado, máximo 12 mensualidades. Con 2.000 € al mes y 10 años, unos 15.342 €. Calcula la tuya gratis en 1 minuto.'),
    'puentes-2027': ('Puentes 2027: los mejores de tu comunidad autónoma',
                     'Qué días pedir en 2027 para encadenar más días libres en tu comunidad, con los festivos oficiales del BOE. Elige tu comunidad y míralo en el calendario.'),
    'guias': ('Guías laborales 2026 en lenguaje claro: despido, paro…',
              '15 guías laborales de 2026 explicadas fácil: despido, finiquito, paro, nómina, baja médica, permisos, contratos, jornada y autónomos.'),
    'facturas': ('Calcular factura de autónomo 2026: IVA y retención IRPF',
                 'Calcula tu factura de autónomo: base, 21 % de IVA y 15 % de IRPF (7 % los primeros años). Con 1.000 € de base cobras 1.060 €. Gratis.'),
    'cuota-autonomos': ('Calcular cuota de autónomos 2026 según tus ingresos',
                        'Tu cuota de autónomos 2026 según lo que ganas: de 205,88 € a 607,35 € al mes, o 88,64 € con tarifa plana. Con 1.500 € netos al mes, 302,65 €.'),
    'pagas-extra': ('Calcular paga extra 2026: verano y Navidad',
                    'Calcula tu paga extra de verano o de Navidad 2026 y la parte que llevas generada si no has trabajado todo el periodo. En 14, 15 o 16 pagas.'),
    'vacaciones': ('Calculadora de vacaciones 2026: días que te corresponden',
                   'Calcula cuántos días de vacaciones te corresponden: 30 naturales al año, 2,5 por mes trabajado. Cuántos te quedan y cuánto valen en dinero.'),
}
# Página → preguntas nuevas (con las palabras de las búsquedas): van las primeras del acordeón y del marcado para Google
FAQS = {
    'facturas': [('¿Cómo se calcula una factura de autónomo?', 'Sobre el importe de tu trabajo (la base) se suma el <strong>21 % de IVA</strong> y, si el cliente es una empresa o un autónomo, se resta la <strong>retención de IRPF</strong> (15 %, o 7 % los tres primeros años). Con 1.000 € de base: 1.000 + 210 − 150 = <strong>1.060 €</strong> a cobrar.')],
    'cuota-autonomos': [('¿Cómo se calcula la cuota de autónomos en 2026?', 'Según tus <strong>rendimientos netos al mes</strong> (ingresos menos gastos, con un 7 % más de gastos si eres persona física), que te colocan en un tramo con una base mínima. La cuota es el <strong>31,5 %</strong> de esa base. Con 1.500 € netos al mes, la base es de 960,78 € y la cuota, <strong>302,65 €</strong>.')],
    'pagas-extra': [('¿Cómo se calcula la paga extra de verano?', 'Normalmente equivale a <strong>un mes de salario base</strong> (lo fija tu convenio) y se genera de enero a junio. Si no has trabajado esos 6 meses, cobras la parte proporcional: con 3 meses trabajados, <strong>la mitad</strong>.')],
    'vacaciones': [('¿Cuántos días de vacaciones me corresponden si llevo 6 meses trabajando?', '<strong>15 días naturales</strong>. Las vacaciones se generan a razón de <strong>2,5 días por mes trabajado</strong> (30 al año), salvo que tu convenio dé más.')],
    'despido-objetivo': [('¿Cuánto me corresponde por despido objetivo con 10 años?', '<strong>20 días de sueldo por año</strong>: 200 días en total. Con 2.000 € brutos al mes en 14 pagas, unos <strong>15.342 €</strong>.')],
}

def cabecera(s, titulo, desc):
    """Cambia el título y la descripción en todos los sitios donde salen (pestaña, Google, WhatsApp y marcado)."""
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', s, count=1)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', rf'\g<1>{titulo}', s, count=1)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', rf'\g<1>{desc}', s, count=1)
    return re.sub(r'("@type": "WebApplication",\s*"name": ")[^"]*(",\s*"url": "[^"]*",\s*"description": ")[^"]*', rf'\g<1>{titulo}\g<2>{desc}', s, count=1)

def poner_faqs(s, faqs):
    for q, a in faqs:
        if q in s or '<div class="faq-item">' not in s: continue                 # página sin preguntas: no se inventa la sección
        item = f'<div class="faq-item"><button class="faq-q"><span>{q}</span>{FLECHA}</button><div class="faq-a"><p>{a}</p></div></div>\n'
        i = s.index('<div class="faq-item">')                                      # delante de la primera pregunta que ya hay
        s = s[:i] + item + s[i:]
        if '"mainEntity": [' in s:
            ld = json.dumps({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': limpio(a)}}, ensure_ascii=False)
            s = s.replace('"mainEntity": [', '"mainEntity": [\n  ' + ld + ',', 1)
    return s

cambiadas = 0
for pag in sorted(set(TITULOS) | set(FAQS)):
    f = f'{pag}.html'
    s = o = open(f, encoding='utf-8').read()
    if pag in TITULOS:
        t, d = TITULOS[pag]
        assert len(t) <= 60 and len(d) <= 160, (pag, len(t), len(d))
        s = cabecera(s, t, d)
    s = poner_faqs(s, FAQS.get(pag, []))
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); cambiadas += 1
print('títulos y preguntas actualizados en', cambiadas, 'páginas')
