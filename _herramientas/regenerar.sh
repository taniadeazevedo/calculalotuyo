#!/bin/sh
# Regenera todas las páginas generadas y aplica el paso final de SEO. Uso: sh _herramientas/regenerar.sh
cd "$(dirname "$0")/.." || exit 1
set -e   # si un paso falla, el script se para ahí (y no termina como si todo hubiera ido bien)
trap 'printf "\n❌ regenerar.sh se ha parado: el último paso ha fallado. No publiques hasta arreglarlo.\n" >&2' EXIT
python3 _herramientas/minificar-css.py      # styles.css (con comentarios) → styles.min.css (lo que carga la web)
node _herramientas/sueldos/calcular.js >/dev/null
python3 _herramientas/sueldos/gen-sueldos.py
python3 _herramientas/sueldos/tablas-irpf-ipc.py   # tablas y preguntas de las páginas de IRPF y subida del IPC
node _herramientas/paro/calcular.js >/dev/null
python3 _herramientas/paro/gen-paro.py
node _herramientas/despido/calcular.js >/dev/null
python3 _herramientas/despido/gen-despido.py
python3 _herramientas/calendario/gen-ciudades.py >/dev/null   # ciudades con fiestas locales publicadas (antes de gen-seo, que las enlaza)
python3 _herramientas/calendario/gen-seo.py >/dev/null
python3 _herramientas/calendario/build-puentes.py
python3 _herramientas/modelos/gen-modelos.py   # sin python-docx/openpyxl solo rehace las páginas, no los archivos
python3 _herramientas/jubilacion/gen-jubilacion.py
python3 _herramientas/informe/gen-informe.py
python3 _herramientas/renta/gen-renta.py
python3 _herramientas/navidad/gen-navidad.py
python3 _herramientas/funcionarios/gen-funcionarios.py
python3 _herramientas/metodologia/gen-metodologia.py
python3 _herramientas/irpf/gen-tramos.py   # página «Tramos del IRPF 2026»
python3 _herramientas/que-hacer/gen-que-hacer.py   # guía «Qué hacer si te despiden»
python3 _herramientas/novedades/gen-novedades.py   # sección Novedades (artículos, portada, RSS)
python3 _herramientas/consolidar.py      # páginas de plantilla unidas en sus tablas (24/10/2026)
python3 _herramientas/seo-final.py
python3 _herramientas/titulos.py           # títulos, descripciones y preguntas según cómo busca la gente
python3 _herramientas/respuestas.py         # «Respuesta rápida» arriba de cada calculadora
python3 _herramientas/menu.py              # el mismo menú en todas las páginas (después de generarlas)
python3 _herramientas/iconos.py            # iconos propios en vez de emojis (después del menú)
python3 _herramientas/buscador.py           # índice del buscador (buscar.json), siempre al final
# pruebas de las calculadoras y de los enlaces: se guarda la salida para enseñar solo el resumen,
# pero el script se para si fallan (con «| tail -1» se perdía el aviso)
if ! salida=$(node _herramientas/pruebas/pruebas.js); then echo "$salida"; exit 1; fi
echo "$salida" | tail -1
python3 _herramientas/sitemap.py           # fechas del sitemap (último cambio de cada página)
trap - EXIT   # todo ha ido bien: sin aviso de error
echo "✅ Web regenerada sin errores"
