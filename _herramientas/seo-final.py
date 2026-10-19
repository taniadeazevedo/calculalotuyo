# Último paso después de generar páginas (lo lanza regenerar.sh):
#  1) cada página usa la imagen para compartir de su sección (og-calendario, og-sueldo, og-paro, og-despido)
#  2) las calculadoras llevan el marcado WebApplication (Google sabe que son herramientas gratis)
import glob, html as H, json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ---- 1) Imagen de cada sección: la primera regla que encaja gana
SECCIONES = [
    ('og-calendario.png', r'^(dias-laborables|puentes-2027|calendario-laboral-2027.*|semana-santa-2027|dias-laborables-2027|trabajar-en-festivo)$'),
    ('og-sueldo.png', r'^(sueldo-neto|irpf|neto-a-bruto|sueldo-bruto-a-neto-2026|\d+-euros-brutos-en-netos|guia-sueldo-neto|guia-nomina)$'),
    ('og-paro.png', r'^(paro|guia-paro|tabla-paro-2026|paro-maximo-minimo-2026|cuanto-paro-me-corresponde|paro-con-\d+-euros)$'),
    ('og-despido.png', r'^(despido-improcedente|despido-objetivo|ere|guia-despido|guia-despido-disciplinario|tabla-indemnizacion-despido|indemnizacion-despido-\d+-anos)$'),
]
# ---- 2) Calculadoras (las 16 laborales y las 2 del calendario)
CALCULADORAS = ['despido-improcedente', 'despido-objetivo', 'ere', 'finiquito', 'paro', 'sueldo-neto', 'irpf', 'horas-extra',
                'pagas-extra', 'vacaciones', 'subida-ipc', 'cuota-autonomos', 'facturas', 'baja-medica', 'reduccion-jornada',
                'neto-a-bruto', 'dias-laborables', 'puentes-2027', 'jubilacion']

cambiadas = 0
for f in glob.glob('*.html'):
    nombre = f[:-5]
    s = o = open(f, encoding='utf-8').read()
    img = next((i for i, patron in SECCIONES if re.match(patron, nombre)), 'og-image.png')
    s = re.sub(r'(https://calculalotuyo\.es/)og-[a-z]+\.png', rf'\g<1>{img}', s)      # og:image y twitter:image
    if nombre in CALCULADORAS and '"WebApplication"' not in s:
        titulo = H.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
        desc = H.unescape(re.search(r'name="description" content="(.*?)"', s).group(1))
        ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebApplication', 'name': titulo, 'url': f'https://calculalotuyo.es/{nombre}',
                         'description': desc, 'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Cualquiera (navegador web)',
                         'inLanguage': 'es-ES', 'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'},
                         'author': {'@type': 'Organization', 'name': 'CalculaLoTuyo', 'url': 'https://calculalotuyo.es/'}}, ensure_ascii=False, indent=1)
        s = s.replace('</head>', f'    <script type="application/ld+json">\n{ld}\n    </script>\n</head>', 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); cambiadas += 1
print('páginas actualizadas:', cambiadas)
