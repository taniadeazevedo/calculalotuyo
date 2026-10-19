# Generadores del calendario

Esta carpeta empieza por `_`, así que GitHub Pages no la publica.

- `boe/f2027.json`: festivos 2027 sacados de la tabla del BOE (BOE-A-2026-21254).
- `build-puentes.py`: monta `puentes-2027.html` con `p-head.html`, `p-main.html` y `p-script.html`.
- `gen-seo.py`: crea `calendario-laboral-2027.html`, las 19 páginas por comunidad,
  `semana-santa-2027.html`, `dias-laborables-2027.html` y `trabajar-en-festivo.html`.

Uso (desde cualquier carpeta):

    python3 _herramientas/calendario/build-puentes.py
    python3 _herramientas/calendario/gen-seo.py

Para 2028: cuando el BOE publique las fiestas (octubre de 2027), sacar la tabla a `boe/f2028.json`,
crear `festivos-2028.js` y cambiar 2027 por 2028 en los scripts y en los textos.

## Regenerar todo (calendario, sueldos, paro y despido)

    sh _herramientas/regenerar.sh

Lanza todos los generadores y, al final, `seo-final.py` (imagen para compartir de cada sección
y marcado de calculadora). Las imágenes se diseñan en `_herramientas/og/*.html` y se hacen con Chrome:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
      --window-size=1200,630 --screenshot=og-paro.png file:///ruta/_herramientas/og/og-paro.html

## Avisar a Bing (IndexNow) después de publicar

    python3 _herramientas/indexnow.py                          # todas las páginas del sitemap
    python3 _herramientas/indexnow.py paro tabla-paro-2026     # solo las que hayas cambiado

La clave está en el archivo `<clave>.txt` de la raíz (no lo borres). También están en la raíz
`BingSiteAuth.xml` (verificación de Bing Webmaster Tools) y `llms.txt` (resumen de la web para las IA:
si cambian las cifras en enero, actualízalo también).

## Buscador

El buscador (lupa del menú, caja de la portada y tecla «/») está en `site.js` y usa `buscar.json`,
que crea `python3 _herramientas/buscador.py` con todas las páginas. `regenerar.sh` lo rehace al final.
Si añades una página a mano, vuelve a lanzar `buscador.py` para que salga en las búsquedas.
Sinónimos y palabras de relleno: constantes `SINONIMOS` y `VACIAS` de `site.js`.
