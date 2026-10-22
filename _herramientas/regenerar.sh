#!/bin/sh
# Regenera todas las páginas generadas y aplica el paso final de SEO. Uso: sh _herramientas/regenerar.sh
cd "$(dirname "$0")/.." || exit 1
python3 _herramientas/minificar-css.py      # styles.css (con comentarios) → styles.min.css (lo que carga la web)
node _herramientas/sueldos/calcular.js >/dev/null && python3 _herramientas/sueldos/gen-sueldos.py
node _herramientas/paro/calcular.js >/dev/null && python3 _herramientas/paro/gen-paro.py
node _herramientas/despido/calcular.js >/dev/null && python3 _herramientas/despido/gen-despido.py
python3 _herramientas/calendario/gen-ciudades.py >/dev/null   # ciudades con fiestas locales publicadas (antes de gen-seo, que las enlaza)
python3 _herramientas/calendario/gen-seo.py >/dev/null && python3 _herramientas/calendario/build-puentes.py
python3 _herramientas/modelos/gen-modelos.py   # sin python-docx/openpyxl solo rehace las páginas, no los archivos
python3 _herramientas/jubilacion/gen-jubilacion.py
python3 _herramientas/informe/gen-informe.py
python3 _herramientas/renta/gen-renta.py
python3 _herramientas/navidad/gen-navidad.py
python3 _herramientas/funcionarios/gen-funcionarios.py
python3 _herramientas/metodologia/gen-metodologia.py
python3 _herramientas/seo-final.py
python3 _herramientas/respuestas.py         # «Respuesta rápida» arriba de cada calculadora
python3 _herramientas/menu.py              # el mismo menú en todas las páginas (después de generarlas)
python3 _herramientas/iconos.py            # iconos propios en vez de emojis (después del menú)
python3 _herramientas/buscador.py           # índice del buscador (buscar.json), siempre al final
node _herramientas/pruebas/pruebas.js | tail -1   # pruebas de las calculadoras: si algo cambia, lo avisa
python3 _herramientas/sitemap.py           # fechas del sitemap (último cambio de cada página)
