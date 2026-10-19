#!/bin/sh
# Regenera todas las páginas generadas y aplica el paso final de SEO. Uso: sh _herramientas/regenerar.sh
cd "$(dirname "$0")/.." || exit 1
python3 _herramientas/minificar-css.py      # styles.css (con comentarios) → styles.min.css (lo que carga la web)
node _herramientas/sueldos/calcular.js >/dev/null && python3 _herramientas/sueldos/gen-sueldos.py
node _herramientas/paro/calcular.js >/dev/null && python3 _herramientas/paro/gen-paro.py
node _herramientas/despido/calcular.js >/dev/null && python3 _herramientas/despido/gen-despido.py
python3 _herramientas/calendario/gen-seo.py >/dev/null && python3 _herramientas/calendario/build-puentes.py
python3 _herramientas/modelos/gen-modelos.py   # sin python-docx/openpyxl solo rehace las páginas, no los archivos
python3 _herramientas/seo-final.py
