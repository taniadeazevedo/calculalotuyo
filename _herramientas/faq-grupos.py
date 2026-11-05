# Preguntas frecuentes agrupadas por temas (03/11/2026): en las páginas con muchas preguntas (hoy solo la del IRPF,
# con 13), la lista seguida se hacía eterna en el móvil. Aquí se ordenan en bloques con un pequeño título.
# Las preguntas siguen todas en la página (y en el marcado para Google); solo cambia el orden y se añaden los títulos.
# Una pregunta nueva que no esté en la lista va a «Otras preguntas». Se puede lanzar las veces que haga falta.
# Uso: python3 _herramientas/faq-grupos.py      (regenerar.sh lo lanza después de titulos.py)
import os, re, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

GRUPOS = {
    'irpf': [
        ('Hijos y familia', ['¿Cuánto IRPF paga una madre o un padre solo con un hijo?', '¿Cuánto IRPF me quitan con 2 hijos?',
                             '¿Cómo calcular el IRPF si tengo hijos?']),
        ('Cómo se calcula', ['¿Cuáles son los tramos del IRPF en 2026?', '¿Cómo se calcula el IRPF de la nómina?', '¿Cómo sé qué IRPF me corresponde?',
                             '¿Qué diferencia hay entre tipo marginal y tipo efectivo?', '¿Por qué mi retención en nómina es diferente al tipo efectivo?']),
        ('Sobre la calculadora', ['¿Esta calculadora de IRPF es la misma que la de Hacienda?', '¿Cuánto IRPF me quitan con 30.000 € brutos?',
                                  '¿Vale para el País Vasco y Navarra?']),
        ('Declaración de la renta', ['¿Qué deducciones puedo aplicar en la declaración de la renta?', '¿Estoy obligado a hacer la declaración de la renta?']),
    ],
}
# Preguntas repetidas que se quitan (decía casi lo mismo que otra que se queda)
QUITAR = {'irpf': ['¿Cómo afectan los hijos a mi IRPF?']}

ITEM = re.compile(r'<div class="faq-item">(?:(?!<div class="faq-item">).)*?</div>\s*</div>', re.S)   # pregunta + respuesta
pregunta = lambda it: re.sub(r'<[^>]+>', '', re.search(r'class="faq-q"[^>]*>(.*?)</button>', it, re.S).group(1)).strip()

for pag, grupos in GRUPOS.items():
    f = f'{pag}.html'; s = o = open(f, encoding='utf-8').read()
    def sin_repetidas(m):                                              # …y del marcado de Google (FAQPage)
        datos = json.loads(m.group(2))
        if datos.get('@type') != 'FAQPage': return m.group(0)
        vistas = set()                                                 # cada pregunta una sola vez (la primera es la más reciente)
        datos['mainEntity'] = [x for x in datos['mainEntity'] if x.get('name') not in QUITAR.get(pag, []) and not (x.get('name') in vistas or vistas.add(x.get('name')))]
        return m.group(1) + json.dumps(datos, ensure_ascii=False, indent=1) + m.group(3)
    s = re.sub(r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', sin_repetidas, s, flags=re.S)
    ini = s.index('<div class="faq-list">') + len('<div class="faq-list">')
    items = list(ITEM.finditer(s, ini))
    fin = items[-1].end()                                              # hasta el final de la última pregunta
    todas = {pregunta(m.group(0)): m.group(0).strip() for m in items}
    for q in QUITAR.get(pag, []): todas.pop(q, None)                   # fuera de la lista
    html, usadas = '', set()
    for titulo, qs in grupos:
        bloque = [todas[q] for q in qs if q in todas]
        usadas.update(qs)
        if bloque: html += f'\n<h3 class="faq-grupo">{titulo}</h3>\n' + '\n'.join(bloque)
    resto = [it for q, it in todas.items() if q not in usadas]
    if resto: html += '\n<h3 class="faq-grupo">Otras preguntas</h3>\n' + '\n'.join(resto)
    # se quitan los títulos de una pasada anterior y se rehace el bloque
    s = s[:ini] + html + '\n' + s[fin:]
    if s != o: open(f, 'w', encoding='utf-8').write(s)
    print('preguntas agrupadas:', pag, len(todas), 'en', len(grupos), 'temas' + (f' + {len(resto)} sueltas' if resto else ''))
