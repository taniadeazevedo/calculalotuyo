# Avisa a Bing (y a los buscadores que usan IndexNow) de las páginas nuevas o cambiadas.
# Uso, DESPUÉS de publicar en GitHub:
#   python3 _herramientas/indexnow.py                → manda todas las páginas del sitemap
#   python3 _herramientas/indexnow.py paro tabla-paro-2026   → manda solo esas
import json, os, re, sys, urllib.request
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CLAVE = '77f3c860fa9a4f91d8c6175259f8af72'                                    # la misma que el archivo 77f3c860fa9a4f91d8c6175259f8af72.txt de la raíz
if len(sys.argv) > 1:
    urls = ['https://calculalotuyo.es/' + p.strip('/') for p in sys.argv[1:]]     # páginas que se pasan por la terminal
else:
    urls = re.findall(r'<loc>(.*?)</loc>', open('sitemap.xml', encoding='utf-8').read())   # todas las del sitemap
datos = json.dumps({'host': 'calculalotuyo.es', 'key': CLAVE,
                    'keyLocation': f'https://calculalotuyo.es/{CLAVE}.txt', 'urlList': urls}).encode()
peticion = urllib.request.Request('https://api.indexnow.org/indexnow', data=datos,
                                  headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(peticion, timeout=30) as r:
        print(f'IndexNow: {len(urls)} páginas enviadas · respuesta {r.status}')   # 200 o 202 = recibido
except urllib.error.HTTPError as e:
    print(f'IndexNow: error {e.code} · {e.read().decode()[:200]}')
