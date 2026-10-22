# Iconos propios en vez de emojis (21/10/2026).
# 1) Arma iconos.svg: un único archivo con todos los iconos (lo descarga el navegador una vez y lo reutiliza)
# 2) Cambia los emojis del HTML de todas las páginas por <svg><use href="/iconos.svg#…"></svg>
# 3) Escribe el mismo mapa en site.js, para los emojis que el JavaScript añade al calcular
# Iconos: Lucide (licencia ISC, libre). Se guardan en _herramientas/iconos/ y solo se descargan los que falten.
# Uso: python3 _herramientas/iconos.py      (regenerar.sh ya lo lanza, después del menú)
import glob, json, os, re, urllib.request
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(RAIZ)
CARPETA = '_herramientas/iconos'
VERSION = '0.460.0'                                                  # versión fija de Lucide

# Emoji (o secuencia de emojis) → icono de Lucide
MAPA = {
    '📅': 'calendar', '📆': 'calendar-days', '🗓️': 'calendar-range', '📊': 'chart-column', '⚖️': 'scale', '💼': 'briefcase',
    '🧾': 'receipt', '🩺': 'stethoscope', '🏛️': 'landmark', '🏖️': 'tree-palm', '💶': 'euro', '📋': 'clipboard-list',
    '🏦': 'wallet', '💵': 'banknote', '🕒': 'clock', '📑': 'file-text', '⏰': 'alarm-clock', '🎁': 'gift', '📈': 'trending-up',
    '🔁': 'repeat', '🎄': 'tree-pine', '🌅': 'sunset', '📚': 'library', '📄': 'file-text', '✍️': 'pen-line', '❓': 'circle-help',
    '❔': 'circle-help', '🧮': 'calculator', '✅': 'circle-check', '📝': 'pencil-line', '🎉': 'party-popper', '⏱️': 'timer',
    '🔄': 'rotate-ccw', '⚠️': 'triangle-alert', '📱': 'smartphone', '💡': 'lightbulb', '🔗': 'link', '🗺️': 'map',
    '📖': 'book-open', '⚡': 'zap', '🚪': 'door-open', '✉️': 'mail', '🤝': 'handshake', '⏸️': 'circle-pause', '📕': 'file-down',
    '👀': 'eye', '💰': 'piggy-bank', '⏳': 'hourglass', '📉': 'trending-down', '🏙️': 'building-2', '📜': 'scroll-text',
    '📌': 'pin', '💻': 'laptop', '🔍': 'search', '🔎': 'search', '🎨': 'palette', '👥': 'users', '📬': 'mailbox', '📍': 'map-pin',
    '📰': 'newspaper', '🥇': 'medal', '🥈': 'medal', '🥉': 'medal', '🔧': 'wrench', '😟': 'frown', '👋': 'hand', '⏩': 'fast-forward',
    '☀️': 'sun', '🛋️': 'sofa', '🏢': 'building', '🔢': 'hash', '📏': 'ruler', '🛡️': 'shield-check', '🏨': 'hotel', '🎯': 'target',
    '🔒': 'lock', '⚙️': 'settings', '✈️': 'plane', '📥': 'download', '🔑': 'key-round', '🧪': 'flask-conical', '🎟️': 'ticket',
    '⬆️': 'arrow-up', '➕': 'plus', '➖': 'minus', '👶': 'baby', '👧': 'user', '👦': 'user', '👩': 'user', '👨': 'user',
    '👨‍👩‍👧': 'users', '👩‍👧‍👦': 'users', '👨‍🔧': 'user', '👩‍🍳': 'user', '👩‍💼': 'user',
    '👨‍💼': 'user', '👩‍💻': 'user', '👨‍💻': 'user', '👩‍⚕️': 'user', '👨‍⚕️': 'user',
    '🎓': 'graduation-cap', '🏠': 'house', '🚗': 'car', '🍼': 'baby', '💳': 'credit-card', '📞': 'phone', '🌍': 'globe',
    '❌': 'circle-x', '⭐': 'star', '🔔': 'bell', '📦': 'package', '🖨️': 'printer', '✨': 'sparkles', '👉': 'arrow-right',
    '🏥': 'hospital', '💊': 'pill', '🤒': 'thermometer', '🏗️': 'hard-hat', '🛒': 'shopping-cart', '🍽️': 'utensils',
    '📧': 'mail', '🗂️': 'folder-open', '🧭': 'compass', '🧑': 'user', '👤': 'user', '👩\u200d🎨': 'user', '🖼️': 'image', '👵': 'user', '🔮': 'telescope', '🖨️': 'printer',
}
# Emoji o secuencia: base + (unión + emoji)* + selector de variación opcional
EMOJI = re.compile('(?:[\U0001F300-\U0001FAFF☀-➿⬀-⯿⌚-⏿]️?)(?:‍[\U0001F300-\U0001FAFF☀-➿]️?)*')

def icono(nombre):
    """SVG de un icono de Lucide: lo baja de unpkg la primera vez y lo guarda en _herramientas/iconos/."""
    ruta = os.path.join(CARPETA, nombre + '.svg')
    if not os.path.exists(ruta):
        os.makedirs(CARPETA, exist_ok=True)
        with urllib.request.urlopen(f'https://unpkg.com/lucide-static@{VERSION}/icons/{nombre}.svg', timeout=20) as r:
            open(ruta, 'wb').write(r.read())
    return open(ruta, encoding='utf-8').read()

# ---- 1) iconos.svg: un <symbol> por icono
simbolos = []
for nombre in sorted(set(MAPA.values())):
    dentro = re.search(r'<svg[^>]*>(.*)</svg>', icono(nombre), re.S).group(1)
    dentro = re.sub(r'\s+', ' ', dentro).strip()
    simbolos.append(f'<symbol id="i-{nombre}" viewBox="0 0 24 24">{dentro}</symbol>')
open('iconos.svg', 'w', encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(simbolos) + '</svg>\n')
svg = lambda n: f'<svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-{n}"/></svg>'

# ---- 2) Las páginas: solo el texto visible del <body> (no atributos, ni <script>, ni <title>…)
sin_mapa = {}
def cambiar_texto(txt, quitar):
    def r(m):
        e = m.group(0); n = MAPA.get(e) or MAPA.get(e.replace('️', '')) or MAPA.get(e + '️')
        if not n: sin_mapa[e] = sin_mapa.get(e, 0) + 1; return m.group(0)   # sin icono: se deja el emoji y se avisa
        return '' if quitar else svg(n)
    t = EMOJI.sub(r, txt)
    return re.sub(r'^\s+', ' ', t) if quitar and t != txt else t             # en <option>, sin el espacio de delante
TROZO = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<option\b[^>]*>.*?</option>|<textarea\b.*?</textarea>|<[^>]+>)', re.S)
cambiadas = 0
for f in sorted(glob.glob('*.html')):
    s = open(f, encoding='utf-8').read()
    i = s.index('<body')
    partes = TROZO.split(s[i:])
    for k, p in enumerate(partes):
        if k % 2 == 0:
            partes[k] = cambiar_texto(p, False)                                   # texto normal → icono
        elif p.startswith('<option'):
            a, b = p.index('>') + 1, p.rindex('<')
            partes[k] = p[:a] + cambiar_texto(p[a:b], True).lstrip() + p[b:]      # en un desplegable no cabe un SVG: se quita el emoji
    nuevo = s[:i] + ''.join(partes)
    # Ejemplos con personas («El caso de Pedro…»): en el círculo, el icono genérico de persona
    nuevo = re.sub(r'(<span class="example-icon">)(?:(?!</span>).)*(</span>)', lambda m: m.group(1) + svg('user') + m.group(2), nuevo, flags=re.S)
    if nuevo != s:
        open(f, 'w', encoding='utf-8').write(nuevo); cambiadas += 1

# ---- 3) site.js: el mismo mapa, para lo que el JavaScript pinta al calcular
js = open('site.js', encoding='utf-8').read()
mapa_js = 'const ICONOS=' + json.dumps(MAPA, ensure_ascii=False, separators=(',', ':')) + ';'
js = re.sub(r'// ICONOS-INICIO.*?// ICONOS-FIN', lambda m: f'// ICONOS-INICIO (lo escribe _herramientas/iconos.py: no tocar a mano)\n{mapa_js}\n// ICONOS-FIN', js, flags=re.S)
open('site.js', 'w', encoding='utf-8').write(js)
print('iconos:', len(simbolos), '· páginas cambiadas:', cambiadas, '· sin icono:', sin_mapa or 'ninguno')
