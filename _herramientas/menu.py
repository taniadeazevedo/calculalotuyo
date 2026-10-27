# Menú único de toda la web. Sustituye el menú de ordenador y el del móvil en TODAS las páginas .html
# y marca en cada una su sección y su enlace. Para cambiar el menú, se cambia aquí y se lanza:
#   python3 _herramientas/menu.py      (regenerar.sh ya lo lanza al final)
import glob, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # carpeta raíz de la web

FLECHA = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
FLECHA_M = FLECHA.replace('width="10" height="10"', 'width="12" height="12"')   # la del móvil, un poco más grande

# Calculadoras agrupadas: (título del grupo, [(página, texto del enlace)])
GRUPOS = [
    ('💶 Sueldo y nómina', [('sueldo-neto', '🏦 Sueldo neto'), ('neto-a-bruto', '🔁 Neto a bruto'), ('irpf', '📑 Retención de IRPF'),
                           ('horas-extra', '⏰ Horas extra'), ('pagas-extra', '🎁 Pagas extra'), ('vacaciones', '🏖️ Vacaciones'),
                           ('subida-ipc', '📈 Subida del IPC'), ('reduccion-jornada', '🕒 Reducción de jornada'),
                           ('sueldo-funcionario-2026', '🏛️ Sueldo de funcionarios')]),
    ('⚖️ Despido y paro', [('despido-improcedente', '⚖️ Despido improcedente'), ('despido-objetivo', '📋 Despido objetivo'),
                          ('ere', '📊 ERE / colectivo'), ('finiquito', '💵 Finiquito'), ('paro', '📊 Paro')]),
    ('🩺 Bajas y jubilación', [('baja-medica', '🩺 Baja médica'), ('jubilacion', '🌅 Jubilación')]),
    ('💼 Autónomos', [('cuota-autonomos', '💼 Cuota de autónomos'), ('facturas', '🧾 Facturas')]),
]
CALENDARIO = [('calendario-laboral-2027', '📆 Calendario laboral 2027'), ('dias-laborables', '📅 Días laborables'), ('puentes-2027', '🗓️ Puentes 2027')]
HACIENDA = [('obligado-a-declarar-renta', '🧾 ¿Tengo que hacer la renta?'), ('tramos-irpf-2026', '📊 Tramos del IRPF 2026'), ('loteria-navidad-hacienda', '🎄 Lotería: cuánto se queda Hacienda')]

# Artículos de Novedades (los escribe _herramientas/novedades/gen-novedades.py)
import json as _json
try: NOVEDADES = _json.load(open('_herramientas/novedades/lista.json', encoding='utf-8'))
except FileNotFoundError: NOVEDADES = []

# Sección de cada página según su nombre: la primera regla que encaja gana
SECCION = [
    ('hacienda', r'^(obligado-a-declarar-renta|renta-.*|loteria-.*|tramos-irpf-.*)$'),
    ('novedades', r'^(novedades|' + '|'.join(re.escape(x['slug']) for x in NOVEDADES) + ')$'),   # Novedades, sección propia
    ('guias', r'^(guia.*|que-hacer-.*)$'),
    ('modelos', r'^modelo.*$'),
    ('calendario', r'^(calendario-laboral-2027.*|dias-laborables.*|puentes-2027|semana-santa-2027|trabajar-en-festivo)$'),
    ('calculadoras', r'^(' + '|'.join(p for _, ls in GRUPOS for p, _ in ls) +
     r'|\d+-euros-brutos-en-netos|paga-extra-navidad-2026|sueldo-funcionario-2026|sueldo-bruto-a-neto-2026|paro-.*|tabla-paro-2026|cuanto-paro-me-corresponde|indemnizacion-despido-.*|tabla-indemnizacion-despido)$'),
]

# Pie de todas las páginas (27/10/2026): cada columna, un tipo de cosa. Para cambiarlo, se cambia aquí.
PIE = [
    ('Calculadoras', [('sueldo-neto', 'Sueldo neto'), ('irpf', 'Retención de IRPF'), ('despido-improcedente', 'Despido improcedente'),
                      ('finiquito', 'Finiquito'), ('paro', 'Paro'), ('cuota-autonomos', 'Cuota de autónomos'), ('./#calculadoras', 'Todas las calculadoras')]),
    ('Guías', [('guias', 'Todas las guías'), ('que-hacer-si-me-despiden', 'Qué hacer si te despiden'), ('guia-despido', 'Guía del despido'),
               ('guia-paro', 'Guía del paro'), ('guia-sueldo-neto', 'Guía del sueldo neto'), ('modelos', 'Modelos gratis'), ('novedades', 'Novedades')]),
    ('Datos 2026', [('sueldo-bruto-a-neto-2026', 'Tabla bruto a neto'), ('tramos-irpf-2026', 'Tramos del IRPF'), ('tabla-paro-2026', 'Tabla del paro'),
                    ('tabla-indemnizacion-despido', 'Tabla de indemnización'), ('smi-2026', 'Salario mínimo (SMI)'), ('iprem-2026', 'IPREM'),
                    ('calendario-laboral-2027', 'Calendario laboral 2027'), ('informe-sueldo-coste-empresa-2026', 'Coste de un trabajador')]),
    ('CalculaLoTuyo', [('sobre-el-proyecto', 'Sobre el proyecto'), ('como-calculamos', 'Cómo calculamos'), ('contacto', 'Contacto'),
                       ('privacidad', 'Privacidad'), ('cookies', 'Cookies'), ('#', 'Gestionar cookies'), ('aviso-legal', 'Aviso legal'), ('terminos', 'Términos')]),
]

def pie(raiz=''):
    """Columnas del pie (sin la marca, que se queda como está). raiz='/' en la 404."""
    cols = ''
    for titulo, enlaces in PIE:
        cols += f'\n            <div class="footer-col">\n                <h4>{titulo}</h4>'
        for href, texto in enlaces:
            if href == '#': cols += '\n                <a href="#" data-cookies>Gestionar cookies</a>'
            else: cols += f'\n                <a href="{raiz + href if not href.startswith("./") else (raiz or "./") + href[2:]}">{texto}</a>'
        cols += '\n            </div>'
    return cols

def menus(pag, raiz=''):
    """Devuelve (menú de ordenador, menú del móvil) para la página «pag». raiz='/' en la 404 (rutas absolutas)."""
    sec = next((s for s, r in SECCION if re.match(r, pag)), '')
    h = lambda p: f'{raiz}{p}'                                              # enlace (relativo o absoluto)
    cur = lambda p: ' aria-current="page"' if p == pag else ''              # marca el enlace de la página actual
    act = lambda s: ' active' if s == sec else ''                           # marca la sección actual
    # ---- Ordenador: «Calculadoras» abre un panel con los grupos en 3 columnas
    col = lambda g: ''.join(f'<p class="mega-titulo">{t}</p>' + ''.join(f'<a href="{h(p)}"{cur(p)}>{x}</a>' for p, x in ls) for t, ls in g)
    columnas = [GRUPOS[:1], GRUPOS[1:2], GRUPOS[2:]]                        # sueldo · despido y paro · bajas, jubilación y autónomos
    nav = f'''<nav class="nav">
            <div class="nav-dropdown nav-mega" data-dropdown>
                <button class="nav-link{act('calculadoras')}" data-dropdown-btn>Calculadoras {FLECHA}</button>
                <div class="nav-dropdown-menu">
                    {''.join(f'<div class="mega-col">{col(c)}</div>' for c in columnas)}
                    <a href="{h('./#calculadoras') if not raiz else '/#calculadoras'}" class="mega-todas">Ver todas las calculadoras →</a>
                </div>
            </div>
            <div class="nav-dropdown" data-dropdown>
                <button class="nav-link{act('hacienda')}" data-dropdown-btn>Hacienda {FLECHA}</button>
                <div class="nav-dropdown-menu">
                    {''.join(f'<a href="{h(p)}"{cur(p)}>{x}</a>' for p, x in HACIENDA)}
                </div>
            </div>
            <a href="{h('guias')}" class="nav-link{act('guias')}"{cur('guias')}>Guías</a>
            <a href="{h('novedades')}" class="nav-link{act('novedades')}"{cur('novedades')}>Novedades</a>
            <a href="{h('modelos')}" class="nav-link{act('modelos')}"{cur('modelos')}>Modelos</a>
            <div class="nav-dropdown nav-cal" data-dropdown>
                <button class="nav-link{act('calendario')}" data-dropdown-btn>📅 Calendario 2027 {FLECHA}</button>
                <div class="nav-dropdown-menu">
                    {''.join(f'<a href="{h(p)}"{cur(p)}>{x}</a>' for p, x in CALENDARIO)}
                </div>
            </div>
        </nav>'''
    # ---- Móvil: los mismos grupos en acordeón; se abre el grupo de la página actual
    abierto = lambda ls: ' open' if any(p == pag for p, _ in ls) else ''
    grupos_m = ''.join(f'''
    <div class="mobile-nav-section{abierto(ls)}">
        <button class="mobile-nav-title" data-mobile-toggle>{t} {FLECHA_M}</button>
        <div class="mobile-nav-links">{''.join(f'<a href="{h(p)}" class="mobile-nav-link"{cur(p)}>{x}</a>' for p, x in ls)}</div>
    </div>''' for t, ls in GRUPOS)
    movil = f'''<nav class="mobile-nav" id="mobileNav">
    <p class="mobile-nav-grupo">Calculadoras</p>{grupos_m}
    <div class="mobile-nav-section{abierto(HACIENDA)}">
        <button class="mobile-nav-title" data-mobile-toggle>🏛️ Hacienda {FLECHA_M}</button>
        <div class="mobile-nav-links">{''.join(f'<a href="{h(p)}" class="mobile-nav-link"{cur(p)}>{x}</a>' for p, x in HACIENDA)}</div>
    </div>
    <div class="mobile-nav-section mobile-nav-sueltos">
        <a href="{h('guias')}" class="mobile-nav-link"{cur('guias')}>📚 Guías</a>
        <a href="{h('novedades')}" class="mobile-nav-link"{cur('novedades')}>📰 Novedades</a>
        <a href="{h('modelos')}" class="mobile-nav-link"{cur('modelos')}>📄 Modelos gratis</a>
    </div>
    <div class="mobile-nav-section mobile-nav-cal open">
        <button class="mobile-nav-title" data-mobile-toggle>📅 Calendario 2027 {FLECHA_M}</button>
        <div class="mobile-nav-links">{''.join(f'<a href="{h(p)}" class="mobile-nav-link"{cur(p)}>{x}</a>' for p, x in CALENDARIO)}</div>
    </div>
</nav>'''
    return nav, movil

cambiadas = 0
for f in sorted(glob.glob('*.html')):
    pag = f[:-5]
    s = o = open(f, encoding='utf-8').read()
    nav, movil = menus(pag, '/' if pag == '404' else '')
    s = re.sub(r'<nav class="nav">.*?</nav>', lambda m: nav, s, count=1, flags=re.S)                               # menú de ordenador
    s = re.sub(r'<nav class="mobile-nav" id="mobileNav">.*?\n</nav>', lambda m: movil, s, count=1, flags=re.S)     # menú del móvil
    # «Cómo calculamos»: en el pie (tras «Sobre el Proyecto») y en la línea «Revisado el… · CalculaLoTuyo»
    if 'como-calculamos">Cómo calculamos' not in s:
        s = re.sub(r'(<a href="/?sobre-el-proyecto">Sobre el Proyecto</a>)', lambda m: m.group(1) + m.group(1).replace('sobre-el-proyecto', 'como-calculamos').replace('Sobre el Proyecto', 'Cómo calculamos'), s, count=1)
    s = re.sub(r'\n\s*<a href="/?novedades">Novedades</a>(</p>)', r'\1', s)   # quita el que se coló en «Revisado el…» (22/10/2026)
    if not re.search(r'Cómo calculamos</a>\s*<a href="/?novedades">Novedades</a>', s):   # «Novedades» en el pie, justo tras «Cómo calculamos»
        s = re.sub(r'(Sobre el Proyecto</a>\s*<a href="(/?)como-calculamos">Cómo calculamos</a>)', lambda m: m.group(1) + f'\n                <a href="{m.group(2)}novedades">Novedades</a>', s, count=1)
    if pag != 'como-calculamos':
        s = re.sub(r'(<p class="hero-meta">.*?<a href="sobre-el-proyecto">CalculaLoTuyo</a>)(</p>)', r'\1 · <a href="como-calculamos">Cómo calculamos</a>\2', s, count=1) if 'href="como-calculamos">Cómo calculamos</a></p>' not in s else s
    # Pie: se conserva la marca (logo y texto) y se rehacen las columnas
    s = re.sub(r'(<div class="footer-grid-4">\s*<div class="footer-brand">.*?</div>\s*</div>)(.*?)(\n\s*</div>\n\s*<div class="footer-bottom">)',
               lambda m: m.group(1) + pie('/' if pag == '404' else '') + m.group(3), s, count=1, flags=re.S)
    # Instagram: un iconito discreto al final de la línea «© 2026 CalculaLoTuyo…» (27/10/2026)
    s = re.sub(r'\n\s*<a href="https://www\.instagram\.com/calculalotuyo/" target="_blank" rel="noopener">Instagram</a>', '', s)   # quita el enlace de texto que iba en la columna de guías
    if 'class="footer-ig"' not in s:
        s = s.replace('Hecho con ♥ en España</p>', 'Hecho con ♥ en España <a class="footer-ig" href="https://www.instagram.com/calculalotuyo/" target="_blank" rel="noopener" aria-label="CalculaLoTuyo en Instagram" title="Instagram"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/></svg></a></p>', 1)
    # Accesibilidad: «Saltar al contenido» para quien navega con teclado (lo primero de la página) y destino en <main>
    s = re.sub(r'<main(?![^>]*id=)', '<main id="contenido" tabindex="-1"', s, count=1)
    s = s.replace('<main id="contenido">', '<main id="contenido" tabindex="-1">', 1)   # tabindex: el teclado sigue desde ahí
    if 'class="saltar"' not in s and 'noindex' not in s:   # (las páginas de traslado no lo necesitan)
        s = re.sub(r'(<body[^>]*>)', r'\1\n<a class="saltar" href="#contenido">Saltar al contenido</a>', s, count=1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); cambiadas += 1
print('menú actualizado en', cambiadas, 'páginas')
