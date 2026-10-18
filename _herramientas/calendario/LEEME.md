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
