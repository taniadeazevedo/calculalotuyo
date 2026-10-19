#!/bin/sh
# Regenera todas las páginas generadas y aplica el paso final de SEO. Uso: sh _herramientas/regenerar.sh
cd "$(dirname "$0")/.." || exit 1
node _herramientas/sueldos/calcular.js >/dev/null && python3 _herramientas/sueldos/gen-sueldos.py
node _herramientas/paro/calcular.js >/dev/null && python3 _herramientas/paro/gen-paro.py
node _herramientas/despido/calcular.js >/dev/null && python3 _herramientas/despido/gen-despido.py
python3 _herramientas/calendario/gen-seo.py >/dev/null && python3 _herramientas/calendario/build-puentes.py
python3 _herramientas/seo-final.py
