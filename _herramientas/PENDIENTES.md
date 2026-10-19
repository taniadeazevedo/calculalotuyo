# Pendientes de CalculaLoTuyo

Última actualización: 20/10/2026. Marca con [x] lo que esté hecho.
👩 = lo haces tú · 🤖 = lo hago yo (pídemelo en una sesión)

## 🔜 Ya (esta semana)
- [ ] 👩 Search Console → Sitemaps: volver a enviar `https://calculalotuyo.es/sitemap.xml` (dirección completa).
- [ ] 👩 Search Console → pedir indexación de las páginas clave (unas 10 al día): portada, calendario-laboral-2027, puentes-2027, jubilacion, sueldo-bruto-a-neto-2026, tabla-paro-2026, tabla-indemnizacion-despido, modelos.
- [ ] 👩 Bing Webmaster Tools: pulsar «Verificar» y añadir el sitemap.
- [x] 👩 Decidir la revisión de ciudades → programada los días 1 y 15 de cada mes, a las 10:00, hasta enero (tarea «calculalotuyo-ciudades-fiestas-locales»).

## 📣 Conseguir enlaces y visitas (gratis)
- [ ] 🤖 Preparar el correo para periodistas y blogs de finanzas con el informe (informe-sueldo-coste-empresa-2026).
- [ ] 👩 Enviarlo.
- [ ] 👩 Responder en Reddit (r/spain, r/askspain) y foros cuando la pregunta encaje, con el enlace exacto (pásame la pregunta y te escribo la respuesta).
- [ ] 🤖 Imágenes para Pinterest de los modelos y del calendario 2027.

## 💰 AdSense
- [ ] 👩 16/11/2026: revisar la indexación (hay recordatorio programado) y, si la mayoría de páginas están indexadas, pedir de nuevo la revisión de AdSense.
- [ ] 👩 Cuando te aprueben: AdSense → Anuncios → Por unidad de anuncio → crear 3 unidades «de display»: «después del resultado», «mitad del texto» y «antes de preguntas». Pásame los códigos.
- [ ] 🤖 Colocar esas 3 unidades en los huecos ya preparados de todas las páginas (con la altura reservada para que la página no salte).
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

## 🗓️ Enero de 2027 (hay tarea programada el 11/01)
- [ ] 🤖 Límites de la renta en `datos-2026.js` → `renta` (si cambian) y escala de rentas imputadas de 2027 si se convalida el RDL 29/2026.
- [ ] 🤖 Cifras de 2027 en `datos-2026.js` (SMI, IPREM, cotizaciones, bases, pensión máxima) y `irpf-2026.js`.
- [ ] 🤖 Regenerar sueldos, paro, despido, jubilación, informe y modelos (`sh _herramientas/regenerar.sh`) y cambiar «2026» por «2027» en los textos.
- [ ] 🤖 Actualizar las cifras de `llms.txt` y la plantilla de nómina (tipos de cotización).
- [ ] 🤖 Hacerlo en los primeros días de enero: quien publica antes las cifras nuevas se lleva el tráfico.

## 🧱 Contenido nuevo (por orden de prioridad)
- [ ] 🤖 «¿Cuánto cobra un/a…?» (enfermera, policía, profesor, bombero, médico…), con sueldos públicos oficiales.
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
