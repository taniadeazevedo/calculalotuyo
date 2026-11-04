# Prueba (05/11/2026): «Cuánto consume un radiador eléctrico» (consumo-radiador-electrico.html).
# Primera página de la familia «Hogar y consumo»: si en 6-8 semanas tiene impresiones en Search Console, seguir con
# lavadora, aire acondicionado y coche eléctrico; si no, dejarlo aquí.
# Consumo = potencia (kW) × horas × parte del tiempo que el aparato está calentando. Coste = consumo × precio del kWh.
# Uso: python3 _herramientas/hogar/gen-radiador.py
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
from plantilla import pagina, REVISADO, e, AD, RAIZ

PRECIO = 0.15                                              # €/kWh de ejemplo (cada uno pone el de su factura)
POTENCIAS = [1000, 1500, 2000, 2500]
HORAS = [1, 4, 6, 8]
kwh = lambda w, h, uso=1: w / 1000 * h * uso
filas = ''.join(f'<tr><td>{e(w)} W</td>' + ''.join(f'<td>{e(kwh(w, h) * PRECIO, 2)} €</td>' for h in HORAS) + f'<td><strong>{e(kwh(w, 6) * PRECIO * 30)} €</strong></td></tr>' for w in POTENCIAS)
ej = kwh(2000, 6) * PRECIO

cuerpo = f'''    <section class="hero-mini"><div class="container">{{{{MIGAS}}}}<div class="hero-badge">🏠 Hogar</div><h1>¿Cuánto consume un radiador eléctrico?<br><span class="highlight">calcula lo que te cuesta por hora, al día y al mes</span></h1>
            <p class="respuesta-corta"><span>⚡ Respuesta rápida</span>Un radiador consume su <strong>potencia por cada hora encendido</strong>: uno de 2.000 W gasta 2 kWh por hora. Con la luz a {e(PRECIO, 2)} €/kWh, son <strong>{e(2 * PRECIO, 2)} € por hora</strong> y unos <strong>{e(ej * 30)} € al mes</strong> usándolo 6 horas al día a tope. Con termostato, menos.</p>
            {REVISADO.format(fecha='5 de noviembre de 2026')}</div></section>

    <section class="calc-section"><div class="container"><div class="card">
        <div class="card-title"><div class="card-icon">🏠</div>Tu radiador y tu tarifa</div>
        <form id="calc">
            <div class="form-grid">
                <div class="form-group"><label class="form-label" for="potencia">Potencia del radiador (W)</label><input type="number" class="form-input" id="potencia" value="2000" min="100" step="50" required><span class="form-hint">Viene en la etiqueta o en las instrucciones</span></div>
                <div class="form-group"><label class="form-label" for="horas">Horas al día</label><input type="number" class="form-input" id="horas" value="6" min="0.5" max="24" step="0.5" required></div>
                <div class="form-group"><label class="form-label" for="dias">Días al mes</label><input type="number" class="form-input" id="dias" value="30" min="1" max="31" required></div>
                <div class="form-group"><label class="form-label" for="precio">Precio de la luz (€/kWh)</label><input type="number" class="form-input" id="precio" value="{PRECIO}" min="0.01" step="0.001" required><span class="form-hint">El «término de energía» de tu factura</span></div>
                <div class="form-group"><label class="form-label" for="uso">¿Cómo funciona?</label><select class="form-select" id="uso"><option value="1">Calentando todo el rato</option><option value="0.6">Con termostato (calienta a ratos, aprox. 60 %)</option></select><span class="form-hint">El termostato lo apaga al llegar a la temperatura</span></div>
            </div>
            <button type="submit" class="btn">Calcular el consumo</button>
            <p class="btn-text">100% privado · Tus datos no salen de tu dispositivo</p>
        </form>
        <div class="result" id="result"><div class="result-hero"><p class="result-label">Te cuesta al mes</p><p class="result-value" id="total">0 €</p><p class="result-sub" id="resultSub"></p></div>
            <div class="result-breakdown"><div class="result-row"><span class="result-row-label">⏰ Por hora</span><span class="result-row-value" id="rHora">0 €</span></div><div class="result-row bruto"><span class="result-row-label">📅 Al día</span><span class="result-row-value" id="rDia">0 €</span></div><div class="result-row exento"><span class="result-row-label">⚡ Consumo al mes</span><span class="result-row-value" id="rKwh">0 kWh</span></div></div>
            <div class="result-actions"><button type="button" class="btn-secondary" id="reset">🔄 Nueva consulta</button></div></div>
    </div></div></section>
''' + AD + f'''
    <section class="section"><div class="container"><article class="seo-section">
<h2>📋 Coste según la potencia y las horas</h2>
<p>Con la luz a {e(PRECIO, 2)} €/kWh (ejemplo: pon el precio de tu factura en la calculadora) y el radiador calentando todo el rato:</p>
<div class="tabla-wrap"><table class="tabla-festivos"><thead><tr><th>Potencia</th>{''.join(f'<th>{h} hora{"s" if h > 1 else ""}</th>' for h in HORAS)}<th>Al mes (6 h al día)</th></tr></thead><tbody>{filas}</tbody></table></div>
<h2>🧮 Cómo se calcula</h2>
<div class="calc-steps">
    <div class="calc-step"><span class="step-num">1</span><div><strong>Consumo por hora:</strong><p>Potencia en vatios ÷ 1.000. Un radiador de 2.000 W gasta <strong>2 kWh</strong> cada hora que está calentando.</p></div></div>
    <div class="calc-step"><span class="step-num">2</span><div><strong>Coste por hora:</strong><p>kWh × precio de la luz: 2 × {e(PRECIO, 2)} = <strong>{e(2 * PRECIO, 2)} €</strong>.</p></div></div>
    <div class="calc-step"><span class="step-num">3</span><div><strong>Coste al mes:</strong><p>Coste por hora × horas al día × días: {e(2 * PRECIO, 2)} × 6 × 30 = <strong>{e(ej * 30, 2)} €</strong>.</p></div></div>
</div>
<h2>💡 Cómo gastar menos</h2>
<ul>
<li>Usa el <strong>termostato</strong> a 19-20 °C: el radiador deja de calentar al llegar a esa temperatura.</li>
<li>Caliéntalo en las <strong>horas más baratas</strong> si tu tarifa tiene discriminación horaria.</li>
<li>Calienta solo la habitación en la que estás y cierra la puerta.</li>
<li>Un radiador de <strong>aceite</strong> no gasta menos que uno de convección de la misma potencia, pero conserva el calor un rato después de apagarse.</li>
</ul>
</article></div></section>

<script>
// Consumo = potencia (kW) × horas × parte del tiempo calentando; coste = consumo × precio del kWh
const f2=n=>new Intl.NumberFormat('es-ES',{{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}}).format(n);
document.getElementById('calc').onsubmit=function(ev){{
    ev.preventDefault();
    const w=+document.getElementById('potencia').value, h=+document.getElementById('horas').value, d=+document.getElementById('dias').value, p=+document.getElementById('precio').value, u=+document.getElementById('uso').value;
    if(!w||!h||!d||!p){{document.getElementById('potencia').focus();return}}
    const kwhHora=w/1000*u, mesKwh=kwhHora*h*d;
    document.getElementById('total').textContent=f2(mesKwh*p);
    document.getElementById('resultSub').textContent=h.toLocaleString('es-ES')+' h al día, '+d+' días, a '+p.toLocaleString('es-ES')+' €/kWh';
    document.getElementById('rHora').textContent=f2(kwhHora*p);
    document.getElementById('rDia').textContent=f2(kwhHora*h*p);
    document.getElementById('rKwh').textContent=mesKwh.toLocaleString('es-ES',{{maximumFractionDigits:1}})+' kWh';
    document.getElementById('result').classList.add('visible');document.getElementById('result').scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('reset').onclick=function(){{document.getElementById('calc').reset();document.getElementById('result').classList.remove('visible');window.scrollTo({{top:0,behavior:'smooth'}})}};
</script>
'''
faqs = [
    ('¿Cuánto consume un radiador eléctrico de 2.000 W?', f'<strong>2 kWh por cada hora</strong> que está calentando. Con la luz a {e(PRECIO, 2)} €/kWh, {e(2 * PRECIO, 2)} € por hora y {e(ej * 30)} € al mes usándolo 6 horas al día.'),
    ('¿Cuánto cuesta tener un radiador encendido toda la noche?', f'Uno de 1.500 W durante 8 horas gasta 12 kWh: unos <strong>{e(kwh(1500, 8) * PRECIO, 2)} €</strong> con la luz a {e(PRECIO, 2)} €/kWh, menos si tiene termostato.'),
    ('¿Gasta menos un radiador de aceite?', '<strong>No</strong>: con la misma potencia consume lo mismo. La diferencia es que el aceite guarda el calor y sigue calentando un rato después de apagarse.'),
    ('¿Qué precio de la luz pongo?', 'El del <strong>término de energía</strong> de tu factura, en €/kWh. Si tienes la tarifa regulada (PVPC), el precio cambia cada hora: usa una media de tus últimas facturas.'),
]
fuente = 'Cálculo propio: consumo (kWh) = potencia (kW) × horas de funcionamiento. El precio de la luz depende de tu contrato.'
pagina('consumo-radiador-electrico', 'Cuánto consume un radiador eléctrico: calculadora de coste',
       f'Un radiador de 2.000 W gasta 2 kWh por hora: unos {e(2 * PRECIO, 2)} € a {e(PRECIO, 2)} €/kWh. Calcula cuánto te cuesta por hora, al día y al mes con tu tarifa.',
       'cuanto consume un radiador electrico, consumo radiador electrico, cuanto gasta un radiador, radiador 2000w consumo, coste radiador electrico',
       [('Hogar', None), ('Consumo de un radiador', None)], cuerpo, faqs, fuente)
sm = os.path.join(RAIZ, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
if '/consumo-radiador-electrico<' not in s:
    open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', '    <url><loc>https://calculalotuyo.es/consumo-radiador-electrico</loc><lastmod>2026-11-05</lastmod><priority>0.7</priority></url>\n</urlset>'))
print(f'consumo-radiador-electrico · 2.000 W, 6 h, 30 días → {e(ej * 30, 2)} €')
