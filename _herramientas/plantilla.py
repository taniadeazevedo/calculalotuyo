# Plantilla común para las páginas generadas: cabecera, menú, migas, preguntas frecuentes y pie.
# El menú y el pie se copian de vacaciones.html, así siempre están al día.
import json, os, re, html as H
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def leer(nombre):
    return open(os.path.join(RAIZ, nombre), encoding='utf-8').read()

def e(n, dec=0):                                   # 1927.5 → "1.928" (formato español)
    t = f'{n:,.{dec}f}'
    return t.replace(',', 'X').replace('.', ',').replace('X', '.')

def pct(n, dec=2):
    return f'{n:.{dec}f}'.replace('.', ',') + ' %'

_v = leer('vacaciones.html')
_NAV = _v[_v.index('<body>') + len('<body>\n'):_v.index('<main')].replace(' aria-current="page"', '').replace('class="nav-link active" data-dropdown-btn>Nómina', 'class="nav-link" data-dropdown-btn>Nómina')
_FOOT = _v[_v.index('<footer'):_v.index('<script src="site.js')]
_CSS = re.search(r'styles(?:\.min)?\.css\?v=[0-9a-z]+', leer('index.html')).group(0)
_limpio = lambda t: re.sub(r'<[^>]+>', '', t)
REVISADO = '<p class="hero-meta">📅 Revisado el {fecha} · ✍️ <a href="sobre-el-proyecto">CalculaLoTuyo</a></p>'
AD = '\n    <div class="container"><div class="ad"></div></div>\n'

def faq_html(faqs):
    return ''.join(f'<div class="faq-item"><button class="faq-q"><span>{q}</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faqs)

def pagina(nombre, titulo, desc, keywords, migas, cuerpo, faqs, fuente, menu_activo='', tema=''):
    """migas: lista de (texto, enlace o None). El último es la página actual."""
    ld_faq = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': _limpio(q), 'acceptedAnswer': {'@type': 'Answer', 'text': _limpio(a)}} for q, a in faqs]}, ensure_ascii=False, indent=1)
    todas = [('Inicio', './')] + migas
    ld_miga = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': t, **({'item': 'https://calculalotuyo.es/' + ('' if u == './' else u)} if u else {})} for i, (t, u) in enumerate(todas)]}, ensure_ascii=False, indent=1)
    migas_html = ' <span class="breadcrumb-sep">›</span> '.join(f'<a href="{u}">{t}</a>' if u else f'<span aria-current="page">{t}</span>' for t, u in todas)
    cuerpo = cuerpo.replace('{{MIGAS}}', f'<nav class="breadcrumb" aria-label="Estás en">{migas_html}</nav>')
    nav = _NAV.replace(f'class="nav-link" data-dropdown-btn>{menu_activo}', f'class="nav-link active" data-dropdown-btn>{menu_activo}') if menu_activo else _NAV
    t, d = H.escape(titulo), H.escape(desc)
    texto = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-4853214655991551">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4853214655991551" crossorigin="anonymous"></script>
    <meta name="description" content="{d}">
    <meta name="keywords" content="{H.escape(keywords)}">
    <title>{t}</title>
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://calculalotuyo.es/{nombre}">
    <meta property="og:title" content="{t}">
    <meta property="og:description" content="{d}">
    <meta property="og:site_name" content="CalculaLoTuyo">
    <meta property="og:locale" content="es_ES">
    <meta name="twitter:card" content="summary_large_image">
    <meta property="og:image" content="https://calculalotuyo.es/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:image" content="https://calculalotuyo.es/og-image.png">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <meta name="theme-color" content="#4F46E5">
    <link rel="canonical" href="https://calculalotuyo.es/{nombre}">
    <link rel="stylesheet" href="{_CSS}">
    <script type="application/ld+json">
{ld_faq}
    </script>
    <script type="application/ld+json">
{ld_miga}
    </script>
</head>
<body{f' class="{tema}"' if tema else ''}>
{nav}<main>
{cuerpo}
    <section class="section section-alt"><div class="container"><h2 class="section-title">❓ Preguntas frecuentes</h2>
        <div class="faq-list">{faq_html(faqs)}</div>
    </div></section>
    <section class="section"><div class="container"><div class="source-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg><div><strong>Fuente:</strong><p>{fuente}</p></div></div></div></section>
</main>

{_FOOT}<script src="site.js?v=20261022b"></script>
</body>
</html>
'''
    open(os.path.join(RAIZ, f'{nombre}.html'), 'w', encoding='utf-8').write(texto)
    return nombre
