# Crea styles.min.css (lo que carga la web) a partir de styles.css (el original, con comentarios).
# Siempre se edita styles.css; este script lo comprime. Lo lanza regenerar.sh.
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
css = open('styles.css', encoding='utf-8').read()
t = re.sub(r'/\*.*?\*/', '', css, flags=re.S)       # 1) quita los comentarios /* … */
t = re.sub(r'\s+', ' ', t)                          # 2) saltos de línea y espacios seguidos → un espacio
t = re.sub(r'\s*([{};,])\s*', r'\1', t)             # 3) sin espacios alrededor de { } ; ,
t = re.sub(r':\s+', ':', t)                         # 4) sin espacio después de «:» (antes sí se deja: «a :hover» no es «a:hover»)
t = t.replace(';}', '}').strip()                    # 5) el último «;» de cada bloque sobra
open('styles.min.css', 'w', encoding='utf-8').write(t + '\n')
print(f'styles.css {len(css):,} → styles.min.css {len(t):,} caracteres')
