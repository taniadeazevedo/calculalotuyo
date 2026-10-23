# Pendientes de CalculaLoTuyo

Última actualización: 20/10/2026. Marca con [x] lo que esté hecho.
👩 = lo haces tú · 🤖 = lo hago yo (pídemelo en una sesión)

## 🔜 Ya (esta semana)
- [ ] 👩 Search Console → Sitemaps: volver a enviar `https://calculalotuyo.es/sitemap.xml` (dirección completa).
- [ ] 👩 Search Console → pedir indexación de las páginas clave (unas 10 al día): portada, calendario-laboral-2027, puentes-2027, jubilacion, sueldo-bruto-a-neto-2026, tabla-paro-2026, tabla-indemnizacion-despido, modelos.
- [ ] 👩 Bing Webmaster Tools: pulsar «Verificar» y añadir el sitemap.
- [x] 👩 Decidir la revisión de ciudades → programada los días 1 y 15 de cada mes, a las 10:00, hasta enero (tarea «calculalotuyo-ciudades-fiestas-locales»).

## ✉️ Correo profesional (21/10/2026)
- [x] 👩 Strato → Correo electrónico → crear la redirección de **contacto@calculalotuyo.es** a tu Gmail (el dominio ya usa el correo de Strato). Probar enviando un correo de prueba.
- [x] 🤖 Publicada la web con contacto@calculalotuyo.es (contacto, privacidad y aviso legal), el 21/10/2026.
- [x] 👩 Formulario de contacto activado con contacto@ (FormSubmit) y redirección de Strato a Gmail funcionando (filtro «Desviar a» + «Mantener»; submissions@formsubmit.co en remitentes seguros). Ojo: lo que te envías desde tu propio Gmail no se ve en la bandeja de entrada.
- [ ] 👩 Opcional: en Gmail → Configuración → Cuentas → «Enviar como» contacto@calculalotuyo.es, para responder desde esa dirección (necesita el servidor SMTP de Strato).

## 📣 Conseguir enlaces y visitas (gratis)
- [x] 🤖 Correo para periodistas y blogs de finanzas: borrador en `_herramientas/correo-prensa.md`.
- [ ] 👩 Enviarlo.
- [ ] 👩 Responder en Reddit (r/spain, r/askspain) y foros cuando la pregunta encaje, con el enlace exacto (pásame la pregunta y te escribo la respuesta).
- [ ] 🤖 Imágenes para Pinterest de los modelos y del calendario 2027.

## 💰 AdSense
- [ ] 👩 16/11/2026: revisar la indexación (hay recordatorio programado) y, si la mayoría de páginas están indexadas, pedir de nuevo la revisión de AdSense.
- [ ] 👩 Cuando te aprueben: AdSense → Anuncios → Por unidad de anuncio → crear 3 unidades «de display»: «después del resultado», «mitad del texto» y «antes de preguntas». Pásame los códigos.
- [ ] 🤖 Colocar esas 3 unidades en los huecos ya preparados de todas las páginas (con la altura reservada para que la página no salte).
- [x] 🤖 22/10/2026: AdSense y su aviso de cookies cargan al primer gesto (o a los 10 s) desde site.js; la verificación queda con la meta google-adsense-account y ads.txt. Si AdSense pone pegas en la revisión, volver a ponerlo en el <head> (quitar la línea de seo-final.py).
- [ ] 👩 En AdSense, anuncios automáticos: activar solo el anuncio fijo de abajo en el móvil («de anclaje») y desactivar los de pantalla completa («viñetas»).

## 📅 Calendario
- [ ] 🤖 Añadir las 44 ciudades pendientes según publiquen sus boletines (noviembre–enero): Andalucía (10), Cataluña (8), Madrid (4), Comunitat Valenciana (4), País Vasco (3), Aragón (3), Castilla-La Mancha (5), Extremadura (2), Cantabria, Burgos, Valladolid, Pamplona y Ceuta. Datos en `_herramientas/calendario/fiestas-locales-2027.json`; luego `sh _herramientas/regenerar.sh`.
- [ ] 🤖 Octubre de 2027: calendario 2028 cuando el BOE publique las fiestas.

## 🧾 Renta (la de 2026, que se presenta en abril–junio de 2027)
- [x] 🤖 Página «¿Tengo que hacer la renta?» con comprobador (`obligado-a-declarar-renta`, generador `_herramientas/renta/gen-renta.py`, límites en `datos-2026.js` → `renta`). Hecha el 20/10/2026.
- [x] 🤖 Menú ordenado: «Calculadoras» (panel con grupos) · Renta · Guías · Modelos · Calendario 2027. Se cambia en `_herramientas/menu.py`.
- [ ] 🤖 Vigilar si el Congreso convalida el Real Decreto-ley 29/2026 de vivienda (BOE 7/10/2026; plazo de unos 30 días hábiles, hacia mediados de noviembre). Para la renta de 2026 añade una deducción del 10 % por alquiler de vivienda habitual y cambia el 1,1 % de las viviendas vacías; desde 2027, una escala nueva (1,1 / 1,5 / 2 / 3 %). Ojo: el anterior (RDL 26/2026) lo derogó el Congreso.
- [ ] 🤖 Noviembre–febrero: calculadora «¿Me sale a pagar o a devolver?» (escala estatal + las 17 autonómicas, comprobadas en sus boletines) y convertir «Renta» del menú en desplegable.
- [ ] 🤖 Marzo de 2027: fechas exactas de la campaña (las publica la Agencia Tributaria) y repaso de la página.

## 🎄 Navidad (hecho el 20/10/2026)
- [x] 🤖 `loteria-navidad-hacienda` (calculadora) y `paga-extra-navidad-2026`. Generador `_herramientas/navidad/gen-navidad.py`.
- [ ] 🤖 Noviembre: comprobar los importes de los premios en el programa oficial de Loterías y Apuestas del Estado (ahora salen de prensa; el impuesto sí está comprobado en el BOE).
- [ ] 🤖 Enero de 2027: adaptar la página de la lotería a El Niño (6 de enero) y cambiar la paga extra a 2027.

## 🧭 Mejoras de uso (hecho el 20/10/2026)
- [x] «Respuesta rápida» arriba de 18 calculadoras (`_herramientas/respuestas.py`: revisar las cifras en enero).
- [x] «¿Y ahora qué?», botón «Guardar en PDF» y recordar el sueldo entre calculadoras (en `site.js`).
- [x] Más fácil de usar: el paro pide el sueldo (no la base reguladora), «Más opciones» en 10 formularios y palabras normales (`_herramientas/formularios.py`), formulario más arriba en el móvil y portada un 32 % más corta.
- [x] Iconos propios en vez de emojis (`_herramientas/iconos.py` + `iconos.svg`), página `como-calculamos`, informe con marcado Dataset (licencia CC BY 4.0) y botón «Compartir imagen» en los resultados (21/10/2026).
- [x] Pruebas automáticas: `node _herramientas/pruebas/pruebas.js` (las lanza regenerar.sh). 10 casos calculados a mano + 17 «fotos». En enero, tras cambiar las cifras, las fotos avisarán: revisar cada cambio y, si está bien, `node _herramientas/pruebas/pruebas.js --foto`.
- [ ] 👩 Prueba con 3–5 personas que no sean del sector, en el móvil y sin ayudarlas: «te despiden tras 5 años cobrando 1.800 €, ¿cuánto te toca?» y «¿cuánto paro cobrarías?». Apunta dónde se atascan.

## ⚡ Velocidad (21/10/2026)
- Lighthouse en el móvil: 70–78 con el aviso de cookies de Google, 99–100 sin él. La web va bien; lo que pesa es el aviso de Google (solo sale la primera visita). Volver a medir cuando AdSense apruebe la web.

## 📰 Novedades (sección creada el 22/10/2026, generador `_herramientas/novedades/gen-novedades.py`)
- [ ] 🤖 30/10: IPC adelantado de octubre → actualizar «subida-pensiones-2027» e «ipc-septiembre-2026-sueldo» (cambiar `actualizado` y la tabla `IPC`).
- [ ] 🤖 Mediados de noviembre: ¿convalida el Congreso el RDL 29/2026? → actualizar «deduccion-alquiler-renta».
- [ ] 🤖 Mediados de diciembre: IPC de noviembre → porcentaje definitivo de las pensiones de 2027.
- [ ] 🤖 1–2 artículos nuevos por semana: SMI 2027, cuotas de autónomos 2027, calendarios de ciudades, novedades de enero… siempre con fuente oficial y sin opinar.

## 🗓️ Enero de 2027 (hay tarea programada el 11/01)
- [ ] 🤖 Límites de la renta en `datos-2026.js` → `renta` (si cambian) y escala de rentas imputadas de 2027 si se convalida el RDL 29/2026.
- [ ] 🤖 Cifras de 2027 en `datos-2026.js` (SMI, IPREM, cotizaciones, bases, pensión máxima) y `irpf-2026.js`.
- [ ] 🤖 Regenerar sueldos, paro, despido, jubilación, informe y modelos (`sh _herramientas/regenerar.sh`) y cambiar «2026» por «2027» en los textos.
- [ ] 🤖 Actualizar las cifras de `llms.txt` y la plantilla de nómina (tipos de cotización).
- [ ] 🤖 Hacerlo en los primeros días de enero: quien publica antes las cifras nuevas se lleva el tráfico.

## 🧱 Contenido nuevo (por orden de prioridad)
- [x] 🤖 `sueldo-funcionario-2026`: tablas oficiales de Hacienda por grupo (20/10/2026). Generador `_herramientas/funcionarios/`. En enero, con la tabla de 2027.
- [ ] 🤖 «¿Cuánto cobra un/a…?» por profesión: en octubre de 2026 no hay tabla oficial del complemento específico (policía, etc.). Revisar si Interior o las comunidades la publican.
- [ ] 🤖 Novedades 2027 (SMI 2027, pensiones 2027, cambios laborales), en diciembre y enero.
- [ ] 🤖 Guías «Qué hacer si…» (me despiden, me quedo en paro, me pongo de baja, nace mi hijo).
- [ ] 🤖 Tablas salariales por convenio (hostelería, comercio, limpieza, metal…): mucho tráfico, pero mucho mantenimiento.

## 💼 Más ingresos (más adelante)
- [ ] 👩 Buscar un despacho de abogados laboralistas colaborador → 🤖 formulario de contacto en las páginas de despido y finiquito.
- [ ] 👩 Darte de alta en programas de afiliados (gestorías para autónomos, renta, cuentas nómina) → 🤖 colocar los enlaces marcados como «patrocinado».
- [ ] 🤖 Calendario 2027 imprimible con el logo de la empresa (producto de pago).
- [ ] 👩 Cuenta de Google Ads solo para usar el Planificador de palabras clave (sin campañas).
- [ ] Con más de unas 20.000 visitas al mes: pasar a Ezoic y, más adelante, a Mediavine o Raptive.
- [ ] Más adelante: chat con IA que solo responda con las páginas de la web y cite la fuente.

## Informe técnico externo (22/10/2026)
- [x] `regenerar.sh` se para si un paso falla (set -e, pruebas sin `| tail -1`) y avisa con ❌.
- [x] Las pruebas ya no se callan los errores de una calculadora y comprueban los enlaces internos rotos de todas las páginas.
- [x] Accesibilidad: «Saltar al contenido», marco visible con el tabulador (:focus-visible) y sin animaciones si se pide (prefers-reduced-motion).
- [x] Portada: «21 calculadoras» (antes 16).
- [ ] Más adelante: CI con GitHub Actions, cabecera/pie sin sacarlos de vacaciones.html, renombrar datos-2026.js en enero.

## Diseño de apartados (anotado el 22/10/2026, revisar)
- [x] (23/10) Ejemplos con pasos en filas y resultado destacado; tablas `info-table` con marco, cabecera y filas alternas; listas numeradas como pasos con número en círculo. Antes: algunas páginas (p. ej. `paro`, bloque de ejemplo «Pedro» y tabla de «Duración») tienen apartados con poco diseño: texto muy apilado (líneas de cálculo pegadas, sin aire) y tablas de dos columnas anchas y sosas.
- [ ] Ideas: ejemplo con pasos en filas separadas y el resultado destacado; tablas con columnas más compactas, cifras alineadas y alguna marca visual (barra o fila resaltada). Revisar el resto de calculadoras y guías con el mismo criterio.

## Enlaces que se vuelven botón (anotado el 23/10/2026, no urgente)
- [x] (23/10) Unificados como texto con flecha. Antes: al pasar el ratón, algunos enlaces de «ver todo» no cambian y otros se convierten en botón con borde (p. ej. «Ver todas las novedades →» es texto, «Ver los 14 modelos →» es botón). Unificar: que ninguno forme botón (mismo estilo de enlace con flecha en toda la web). Revisar `.calc-group-guide`, `.chip-mas` y similares.
