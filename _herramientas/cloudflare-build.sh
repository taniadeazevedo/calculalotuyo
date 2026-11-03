#!/bin/bash
# Script que ejecuta Cloudflare Pages cada vez que subes cambios a GitHub.
# Copia la web a la carpeta "dist" SIN las herramientas internas,
# para que no se publiquen (en GitHub Pages las ocultaba Jekyll por empezar por "_").
set -e                                   # si algo falla, se para y Cloudflare avisa del error
rm -rf dist                              # borra una "dist" vieja si la hubiera
mkdir dist                               # crea la carpeta vacía que se publicará
tar --exclude=./dist \
    --exclude=./.git \
    --exclude=./_herramientas \
    --exclude='.DS_Store' --exclude=./.gitignore \
    --exclude=./CNAME --exclude=./netlify.toml \
    -cf - . | tar -xf - -C dist          # empaqueta todo lo demás y lo desempaqueta dentro de dist
echo "Archivos publicados: $(find dist -type f | wc -l)"   # muestra cuántos archivos se suben
