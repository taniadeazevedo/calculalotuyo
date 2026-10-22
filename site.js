// =====================================================================
// JavaScript común a todas las páginas: formato de euros, menú,
// preguntas frecuentes, errores de formulario y consentimiento de cookies.
// =====================================================================

// ---------- Formato de euros ----------
// useGrouping:'always' pone el punto de miles también en números de 4 cifras (6.418 €)
const fmt=n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0,useGrouping:'always'}).format(n);
const fmtDec=n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',useGrouping:'always'}).format(n);

// ---------- Menú de escritorio (desplegables) ----------
const desplegables=document.querySelectorAll('[data-dropdown]');
const cerrarDesplegables=()=>desplegables.forEach(d=>{
    d.classList.remove('open');
    d.querySelector('[data-dropdown-btn]').setAttribute('aria-expanded','false');
});
desplegables.forEach(dd=>{
    const btn=dd.querySelector('[data-dropdown-btn]');
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',e=>{
        e.stopPropagation();                         // que el clic no llegue al document y lo cierre
        const estabaAbierto=dd.classList.contains('open');
        cerrarDesplegables();                        // solo uno abierto a la vez
        if(!estabaAbierto){dd.classList.add('open');btn.setAttribute('aria-expanded','true')}
    });
});
document.addEventListener('click',cerrarDesplegables);   // clic fuera: se cierran
document.addEventListener('keydown',e=>{if(e.key==='Escape')cerrarDesplegables()});

// ---------- Menú móvil ----------
const menuBtn=document.getElementById('menuBtn'),mobileNav=document.getElementById('mobileNav');
if(menuBtn&&mobileNav){
    menuBtn.setAttribute('aria-expanded','false');
    menuBtn.addEventListener('click',()=>{
        const abierto=mobileNav.classList.toggle('open');
        menuBtn.classList.toggle('active',abierto);
        menuBtn.setAttribute('aria-expanded',abierto);
        document.body.style.overflow=abierto?'hidden':'';   // sin scroll de fondo con el menú abierto
    });
}
document.querySelectorAll('[data-mobile-toggle]').forEach(btn=>{
    btn.addEventListener('click',()=>btn.parentElement.classList.toggle('open'));
});

// ---------- Preguntas frecuentes (acordeón) ----------
document.querySelectorAll('.faq-q').forEach(btn=>{
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',()=>{
        const item=btn.parentElement;
        const estabaAbierta=item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i=>{
            i.classList.remove('open');
            i.querySelector('.faq-q').setAttribute('aria-expanded','false');
        });
        if(!estabaAbierta){item.classList.add('open');btn.setAttribute('aria-expanded','true')}
    });
});

// ---------- Errores de formulario (sustituye a alert) ----------
// Muestra el mensaje encima del botón de calcular; con '' lo oculta.
function mostrarError(mensaje){
    const form=document.getElementById('calc');
    if(!form)return;
    let caja=form.querySelector('.form-error');
    if(!caja){
        caja=document.createElement('p');
        caja.className='form-error';
        caja.setAttribute('role','alert');           // los lectores de pantalla lo anuncian
        const boton=form.querySelector('[type="submit"]');
        boton.parentNode.insertBefore(caja,boton);
    }
    caja.textContent=mensaje;
    caja.hidden=!mensaje;
    if(mensaje)caja.scrollIntoView({behavior:'smooth',block:'center'});
}
// Al volver a calcular se borra el error anterior (se ejecuta antes que el cálculo de la página)
const formCalc=document.getElementById('calc');
if(formCalc)formCalc.addEventListener('submit',()=>mostrarError(''),true);
// Después de calcular, la página baja sola hasta el resultado (en el móvil quedaba escondido debajo del formulario)
if(formCalc)formCalc.addEventListener('submit',()=>{
    setTimeout(()=>{                                 // espera a que la calculadora haya pintado el resultado
        const resultado=document.getElementById('result');
        if(resultado&&resultado.classList.contains('visible'))resultado.scrollIntoView({behavior:'smooth',block:'start'});
    },60);
});

// ---------- Correo de contacto ----------
// La dirección no está escrita entera en el HTML para que no la recojan los robots de spam
document.querySelectorAll('[data-correo]').forEach(el=>{
    const correo=el.dataset.correo+'@'+el.dataset.dominio;
    el.textContent=correo;
    if(el.tagName==='A')el.href='mailto:'+correo;
});

// ---------- Cookies: el aviso lo muestra Google (CMP certificada de AdSense) ----------
// El script de AdSense va fijo en el <head> de cada página y trae el mensaje de
// consentimiento que configuramos en AdSense > Privacidad y mensajes.
const ID_ANALYTICS='G-QLG0Q6JB5J';                  // propiedad «Calculalotuyo.es» de la cuenta «Calcula lo tuyo» (desde el 22/10/2026)

// Google Analytics con el modo de consentimiento: por defecto todo denegado,
// y el mensaje de Google lo actualiza cuando el visitante acepta
window.dataLayer=window.dataLayer||[];               // cola de órdenes que lee gtag.js
window.gtag=function(){dataLayer.push(arguments)};   // función estándar de Google para enviar órdenes
gtag('consent','default',{                           // estado inicial: sin permiso
    ad_storage:'denied',                             // cookies de publicidad
    ad_user_data:'denied',                           // enviar datos de usuario a Google para anuncios
    ad_personalization:'denied',                     // anuncios personalizados
    analytics_storage:'denied',                      // cookies de analítica
    wait_for_update:500                              // espera medio segundo a que responda el aviso
});
gtag('js',new Date());                               // marca el momento de carga
gtag('config',ID_ANALYTICS);                         // activa Analytics con nuestro identificador
// El script de Analytics se descarga cuando la página ya se ve (evento «load»):
// así no compite con el contenido en móviles con conexión lenta.
// Las órdenes de arriba esperan en dataLayer y se envían en cuanto llega.
function cargarAnalytics(){
    const scriptAnalytics=document.createElement('script');   // crea la etiqueta <script> de Analytics
    scriptAnalytics.async=true;                      // que no frene nada mientras se descarga
    scriptAnalytics.src='https://www.googletagmanager.com/gtag/js?id='+ID_ANALYTICS;
    document.head.appendChild(scriptAnalytics);      // la añade al <head>
}
if(document.readyState==='complete')cargarAnalytics();         // la página ya había terminado de cargar
else window.addEventListener('load',cargarAnalytics,{once:true});   // si no, espera a que termine (una sola vez)

// Cualquier enlace con data-cookies vuelve a abrir el mensaje de Google para cambiar la decisión
window.googlefc=window.googlefc||{};                 // objeto que crea el mensaje de Google
googlefc.callbackQueue=googlefc.callbackQueue||[];   // cola de tareas que se ejecutan cuando esté listo
document.querySelectorAll('[data-cookies]').forEach(el=>el.addEventListener('click',e=>{
    e.preventDefault();                              // que el enlace "#" no salte arriba
    if(typeof googlefc.showRevocationMessage==='function'){   // el mensaje de Google está cargado: lo abre otra vez
        googlefc.showRevocationMessage();
    }else{                                           // aún no lo está (p. ej., mientras AdSense revisa la web o con un bloqueador):
        location.href='cookies#gestionar';           // lleva a la explicación de cómo gestionar las cookies
    }
}));

// =====================================================================
// BUSCADOR
// El índice (buscar.json) lo crea _herramientas/buscador.py con todas las páginas.
// Solo se descarga la primera vez que alguien empieza a buscar (unos 10 KB).
// Todo pasa en el navegador: no se envía nada a ningún servidor.
// =====================================================================
let indiceBusqueda=null;                             // aquí se guarda el índice cuando ya se ha descargado

// Quita tildes, pasa a minúsculas y junta los números con puntos («30.000» → «30000»)
function normalizar(texto){
    return (texto||'').toLowerCase()
        .normalize('NFD').replace(/[̀-ͯ]/g,'')    // quita las tildes (á → a)
        .replace(/(\d)\.(?=\d{3})/g,'$1')                  // 30.000 → 30000
        .replace(/[^a-z0-9ñ]+/g,' ').trim();               // todo lo que no sea letra o número, a espacio
}

// Palabras que la gente usa para lo mismo: si buscas una, también vale la otra
const SINONIMOS={
    paro:['desempleo','prestacion'], desempleo:['paro'], sueldo:['salario','nomina','neto'], salario:['sueldo','nomina'],
    nomina:['sueldo','salario'], despido:['indemnizacion','despedido'], despedido:['despido','indemnizacion'],
    indemnizacion:['despido'], festivos:['calendario','puentes','festivo'], festivo:['festivos','calendario'],
    autonomo:['autonomos','cuota'], autonoma:['autonomos','cuota'], factura:['facturas'], dimision:['baja','voluntaria'],
    renuncia:['baja','voluntaria'], carta:['modelo','plantilla'], plantilla:['modelo','plantillas'], modelo:['plantilla','modelos'],
    vacaciones:['vacacion'], voy:['baja','finiquito'], irme:['baja','finiquito'], marcho:['baja','finiquito'], echado:['despido'], echan:['despido'], liquidacion:['finiquito'], bruto:['brutos'], neto:['netos','liquido'], horario:['jornada','registro'], fichar:['registro','jornada']
};

// Descarga el índice (una sola vez) y prepara las palabras de cada página para buscar rápido
async function cargarIndice(){
    if(indiceBusqueda)return indiceBusqueda;                         // ya estaba cargado
    const respuesta=await fetch('/buscar.json');                     // el archivo está en la raíz de la web
    const datos=await respuesta.json();
    indiceBusqueda=datos.map(p=>({...p,                               // copia cada página y le añade sus palabras ya normalizadas
        pt:normalizar(p.t).split(' '),                                // palabras del título
        pk:normalizar(p.k).split(' '),                                // palabras clave
        pd:normalizar(p.d).split(' ')                                 // palabras de la descripción
    }));
    return indiceBusqueda;
}

// Palabras de relleno que no ayudan a buscar («me han despedido» → «despedido»)
const VACIAS=new Set(['me','te','se','le','lo','la','las','los','el','un','una','de','del','al','a','en','con','por','para','y','o','que','mi','mis','tu','su','es','han','ha','he','hay','como','cuanto','cuanta','cuantos','cuantas','cual','tengo','si','sin','mas','muy','ya','hago','hacer','cobro','cobrar','cobra','queda','quedan','puedo','debo','necesito','quiero','saber','calcular','calculo','dar','darme','pasa','pasaria','esta','estoy','soy','empresa','trabajo','trabajar']);

// Busca y devuelve las mejores páginas (como mucho «cuantas»)
function buscar(consulta,cuantas){
    const frase=normalizar(consulta);                                       // la búsqueda entera, para premiar la frase exacta
    const palabras=frase.split(' ').filter(w=>!VACIAS.has(w)&&(w.length>1||/^\d$/.test(w)));   // sin relleno; los números de una cifra sí valen
    if(!palabras.length||!indiceBusqueda)return [];
    const empieza=(lista,w)=>/^\d+$/.test(w)?lista.includes(w):lista.some(x=>x.startsWith(w));   // números exactos («5» no es «50000»); palabras por el principio («desp» → «despido»)
    const resultados=[];
    for(const p of indiceBusqueda){
        let puntos=0,encontradas=0;
        for(const w of palabras){
            const variantes=[w,...(SINONIMOS[w]||[])];                        // la palabra y sus sinónimos
            const en=lista=>variantes.some(v=>empieza(lista,v));
            if(empieza(p.pt,w)){puntos+=8;encontradas++}                      // la palabra tal cual en el título: lo que más vale
            else if(en(p.pt)){puntos+=5;encontradas++}                        // un sinónimo en el título, algo menos
            else if(en(p.pk)){puntos+=3;encontradas++}                        // en las palabras clave, algo menos
            else if(en(p.pd)){puntos+=1;encontradas++}                        // en la descripción, lo mínimo
        }
        if(encontradas<Math.ceil(palabras.length/2))continue;               // tienen que aparecer al menos la mitad de las palabras
        if(palabras.length>1&&p.pt.join(' ').includes(palabras.join(' ')))puntos+=12;   // la frase entera está en el título («semana santa»)
        resultados.push({p,puntos:encontradas*100+puntos*p.p});              // primero las que encajan más palabras; luego el peso (calculadoras y tablas antes)
    }
    return resultados.sort((a,b)=>b.puntos-a.puntos).slice(0,cuantas).map(r=>r.p);
}

// Pinta los resultados en una lista; «activo» es el que está marcado con el teclado
function pintarResultados(lista,resultados,consulta,activo){
    if(!consulta.trim()){lista.hidden=true;lista.innerHTML='';return}         // caja vacía: no se enseña nada
    lista.hidden=false;
    if(!resultados.length){                                                    // nada encontrado: sugerencias
        lista.innerHTML='<p class="busca-nada">No hemos encontrado nada. Prueba con «paro», «despido», «vacaciones» o «factura».</p>';
        return;
    }
    const esc=t=>t.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));   // evita que un texto rompa el HTML
    lista.innerHTML=resultados.map((p,i)=>
        `<a href="/${p.u}" class="busca-res${i===activo?' activo':''}" role="option"><span class="busca-ico" aria-hidden="true">${p.i}</span>`+
        `<span class="busca-txt"><strong>${esc(p.t)}</strong><small>${esc(p.c)} · ${esc(p.d)}</small></span></a>`).join('');
}

// Conecta una caja de texto con su lista de resultados (se usa en la portada y en la ventana de la lupa)
function montarBuscador(caja,lista){
    let resultados=[],activo=-1;                                               // resultados actuales y cuál está marcado
    const actualizar=async()=>{
        await cargarIndice();                                                  // la primera vez descarga el índice
        resultados=buscar(caja.value,8);activo=-1;                             // como mucho 8 resultados
        pintarResultados(lista,resultados,caja.value,activo);
    };
    caja.addEventListener('input',actualizar);                                 // busca mientras escribes
    caja.addEventListener('focus',()=>{cargarIndice()});                       // empieza a descargar el índice al entrar en la caja
    caja.addEventListener('keydown',e=>{
        if(e.key==='ArrowDown'||e.key==='ArrowUp'){                            // flechas: moverse por los resultados
            e.preventDefault();
            if(!resultados.length)return;
            activo=(activo+(e.key==='ArrowDown'?1:-1)+resultados.length)%resultados.length;   // da la vuelta al llegar al final
            pintarResultados(lista,resultados,caja.value,activo);
        }else if(e.key==='Enter'&&resultados.length){                          // Intro: abre el marcado (o el primero)
            e.preventDefault();
            location.href='/'+resultados[Math.max(0,activo)].u;
        }
    });
}

// Buscador de la portada (solo existe en index.html)
const cajaPortada=document.getElementById('buscaHome');
if(cajaPortada)montarBuscador(cajaPortada,document.getElementById('buscaHomeLista'));

// Ventana del buscador que abre la lupa del menú (se crea solo la primera vez que hace falta)
function abrirBuscador(){
    let modal=document.getElementById('buscaModal');
    if(!modal){
        modal=document.createElement('div');
        modal.id='buscaModal';modal.className='busca-modal';
        modal.innerHTML='<div class="busca-ventana" role="dialog" aria-modal="true" aria-label="Buscar en la web">'+
            '<div class="busca-fila"><input type="search" class="busca-input" id="buscaModalCaja" placeholder="¿Qué necesitas? Paro, despido, 30.000 brutos…" autocomplete="off" aria-label="Buscar">'+
            '<button type="button" class="busca-cerrar" aria-label="Cerrar">✕</button></div>'+
            '<div class="busca-lista" id="buscaModalLista" role="listbox" hidden></div></div>';
        document.body.appendChild(modal);
        montarBuscador(document.getElementById('buscaModalCaja'),document.getElementById('buscaModalLista'));
        modal.addEventListener('click',e=>{if(e.target===modal)cerrarBuscador()});            // clic fuera de la ventana: se cierra
        modal.querySelector('.busca-cerrar').addEventListener('click',cerrarBuscador);       // botón ✕
    }
    modal.classList.add('abierto');
    document.body.style.overflow='hidden';                                     // la página de fondo no se mueve
    setTimeout(()=>document.getElementById('buscaModalCaja').focus(),30);      // el cursor directamente en la caja
}
function cerrarBuscador(){
    const modal=document.getElementById('buscaModal');
    if(modal)modal.classList.remove('abierto');
    document.body.style.overflow='';
}
document.querySelectorAll('[data-buscar]').forEach(b=>b.addEventListener('click',abrirBuscador));   // la lupa del menú
document.addEventListener('keydown',e=>{
    const escribiendo=/input|textarea|select/i.test(document.activeElement.tagName);
    if(e.key==='/'&&!escribiendo){e.preventDefault();abrirBuscador()}          // tecla «/»: abre el buscador desde cualquier sitio
    if(e.key==='Escape')cerrarBuscador();                                      // Esc: lo cierra
});

// =====================================================================
// DESPUÉS DEL RESULTADO: «¿Y ahora qué?», guardar en PDF y recordar datos
// =====================================================================
const PAGINA=location.pathname.split('/').pop().replace('.html','')||'index';   // nombre de la página («paro», «finiquito»…)

// ---------- «¿Y ahora qué?»: el siguiente paso lógico después de cada calculadora ----------
// [enlace, texto] · Se muestra debajo del resultado (dentro de #result, así solo se ve al calcular)
const SIGUIENTE={
    'despido-improcedente':[['paro','📊 ¿Cuánto paro vas a cobrar?'],['finiquito','💵 Calcula también tu finiquito'],['modelo-reclamacion-cantidades','📄 Modelo para reclamar lo que te deben']],
    'despido-objetivo':[['paro','📊 ¿Cuánto paro vas a cobrar?'],['despido-improcedente','⚖️ ¿Y si el despido fuera improcedente?'],['finiquito','💵 Calcula también tu finiquito']],
    'ere':[['paro','📊 ¿Cuánto paro vas a cobrar?'],['finiquito','💵 Calcula también tu finiquito'],['jubilacion','🌅 Si te queda poco, mira tu jubilación']],
    'finiquito':[['paro','📊 ¿Te quedas en paro? Mira cuánto cobras'],['despido-improcedente','⚖️ Si te han despedido: tu indemnización'],['modelo-carta-baja-voluntaria','📄 Modelo de carta de baja voluntaria']],
    'paro':[['tabla-paro-2026','📋 Tabla del paro según tu sueldo'],['cuanto-paro-me-corresponde','⏳ Cuánto tiempo de paro te corresponde'],['obligado-a-declarar-renta','🧾 Con paro y trabajo, ¿tienes que hacer la renta?']],
    'sueldo-neto':[['pagas-extra','🎁 Calcula tus pagas extra'],['irpf','📑 Revisa tu retención de IRPF'],['obligado-a-declarar-renta','🧾 ¿Tienes que hacer la renta?']],
    'irpf':[['sueldo-neto','🏦 Mira tu sueldo neto al mes'],['obligado-a-declarar-renta','🧾 ¿Tienes que hacer la renta?'],['neto-a-bruto','🔁 Qué bruto pedir para un neto']],
    'neto-a-bruto':[['sueldo-neto','🏦 Comprueba el neto de ese bruto'],['sueldo-bruto-a-neto-2026','📋 Tabla de bruto a neto 2026'],['subida-ipc','📈 Cuánto debería subirte el sueldo']],
    'horas-extra':[['sueldo-neto','🏦 Mira tu sueldo neto al mes'],['modelo-registro-jornada','📄 Plantilla de registro de jornada'],['guia-jornada','📚 Guía de jornada y horas extra']],
    'pagas-extra':[['paga-extra-navidad-2026','🎄 Paga extra de Navidad 2026'],['sueldo-neto','🏦 Mira tu sueldo neto al mes'],['finiquito','💵 Si te vas: tu finiquito']],
    'vacaciones':[['modelo-solicitud-vacaciones','📄 Modelo para pedir vacaciones'],['puentes-2027','🗓️ Puentes 2027: dónde te cunden más'],['finiquito','💵 Si te vas: vacaciones en el finiquito']],
    'subida-ipc':[['sueldo-neto','🏦 Mira cuánto es en neto'],['neto-a-bruto','🔁 Qué bruto pedir para un neto'],['guia-nomina','📚 Guía para entender tu nómina']],
    'baja-medica':[['guia-baja-medica','📚 Guía de la baja médica'],['sueldo-neto','🏦 Tu sueldo neto normal'],['finiquito','💵 Si te despiden estando de baja: finiquito']],
    'reduccion-jornada':[['modelo-solicitud-reduccion-jornada','📄 Modelo para pedir la reducción'],['modelo-adaptacion-jornada','📄 Modelo para adaptar tu horario'],['guia-nacimiento','📚 Guía de nacimiento y cuidado']],
    'jubilacion':[['sueldo-neto','🏦 Tu sueldo neto actual'],['paro','📊 Si te quedas sin trabajo antes: el paro'],['obligado-a-declarar-renta','🧾 Con pensión, ¿tienes que hacer la renta?']],
    'cuota-autonomos':[['facturas','🧾 Calcula tus facturas con IVA e IRPF'],['modelo-factura-autonomo','📄 Plantilla de factura gratis'],['guia-autonomos','📚 Guía para autónomos']],
    'facturas':[['modelo-factura-autonomo','📄 Plantilla de factura gratis'],['cuota-autonomos','💼 Tu cuota de autónomos'],['modelo-presupuesto-autonomo','📄 Plantilla de presupuesto']],
    'obligado-a-declarar-renta':[['irpf','📑 Revisa tu retención de IRPF'],['loteria-navidad-hacienda','🎄 Lotería: cuánto se queda Hacienda'],['sueldo-neto','🏦 Tu sueldo neto']],
    'loteria-navidad-hacienda':[['obligado-a-declarar-renta','🧾 ¿Tienes que hacer la renta?'],['paga-extra-navidad-2026','🎁 Paga extra de Navidad 2026'],['puentes-2027','🗓️ Puentes 2027 para gastarlo']]
};
const resultado=document.getElementById('result');
if(resultado&&SIGUIENTE[PAGINA]){
    const caja=document.createElement('div');
    caja.className='siguiente';
    caja.innerHTML='<p class="siguiente-titulo">👉 ¿Y ahora qué?</p>'+SIGUIENTE[PAGINA].map(([h,t])=>'<a href="'+h+'">'+t+'</a>').join('');
    resultado.appendChild(caja);                       // queda dentro del resultado: solo se ve después de calcular
}

// ---------- Guardar el resultado en PDF (usa «Imprimir» del navegador → «Guardar como PDF») ----------
const acciones=resultado&&resultado.querySelector('.result-actions');
if(acciones){
    const b=document.createElement('button');
    b.type='button'; b.className='btn-secondary btn-pdf'; b.textContent='🖨️ Guardar en PDF';
    b.addEventListener('click',()=>window.print());    // la hoja de estilos de impresión deja solo el resultado
    acciones.insertBefore(b,acciones.querySelector('.btn-wa'));   // entre «Nueva consulta» y «WhatsApp»
}

// ---------- Recordar tus datos entre calculadoras (solo en este navegador, nunca se envían) ----------
// Página → {campo: dato guardado}. «brutoAnual» y «brutoMes» se comparten entre calculadoras distintas.
const RECORDAR={
    'despido-improcedente':{salario:'brutoAnual',inicio:'alta'}, 'despido-objetivo':{salario:'brutoAnual',inicio:'alta'},
    'ere':{salario:'brutoAnual',inicio:'alta'}, 'subida-ipc':{salario:'brutoAnual'}, 'sueldo-neto':{bruto:'brutoAnual'},
    'reduccion-jornada':{bruto:'brutoAnual'}, 'jubilacion':{sueldo:'brutoAnual'}, 'irpf':{ingresos:'brutoAnual'},
    'finiquito':{salario:'brutoMes',fechaAlta:'alta'}, 'paro':{sueldoMes:'brutoMes'}, 'horas-extra':{salario:'brutoMes'}, 'vacaciones':{salario:'brutoMes'}
};
const leerDatos=()=>{try{return JSON.parse(localStorage.getItem('clt-datos'))||{}}catch(e){return {}}};   // puede fallar en modo privado
const campos=RECORDAR[PAGINA], form=document.getElementById('calc');
if(campos&&form){
    const guardado=leerDatos(); let rellenados=0;
    Object.entries(campos).forEach(([id,clave])=>{
        const el=document.getElementById(id);
        if(el&&!el.value&&guardado[clave]){el.value=guardado[clave];rellenados++}   // solo rellena campos vacíos
    });
    if(rellenados){                                    // avisa y deja borrarlo
        const aviso=document.createElement('p');
        aviso.className='aviso-recordado';
        aviso.innerHTML='✨ Hemos rellenado algunos datos con lo que pusiste en otra calculadora (solo se guarda en este dispositivo). <button type="button">Borrar mis datos</button>';
        aviso.querySelector('button').addEventListener('click',()=>{
            try{localStorage.removeItem('clt-datos')}catch(e){}
            Object.keys(campos).forEach(id=>{const el=document.getElementById(id);if(el)el.value=''});
            aviso.remove();
        });
        form.insertBefore(aviso,form.firstChild);
    }
    form.addEventListener('submit',()=>{                // al calcular, guarda lo que has puesto
        const datos=leerDatos();
        Object.entries(campos).forEach(([id,clave])=>{const el=document.getElementById(id);if(el&&el.value)datos[clave]=el.value});
        try{localStorage.setItem('clt-datos',JSON.stringify(datos))}catch(e){}
    });
}

// ---------- Iconos propios en vez de emojis ----------
// El HTML ya llega con iconos (lo hace _herramientas/iconos.py). Esto cambia los emojis que el JavaScript
// pinta después (resultados, buscador, «¿Y ahora qué?»), con el mismo mapa emoji → icono.
// ICONOS-INICIO (lo escribe _herramientas/iconos.py: no tocar a mano)
const ICONOS={"📅":"calendar","📆":"calendar-days","🗓️":"calendar-range","📊":"chart-column","⚖️":"scale","💼":"briefcase","🧾":"receipt","🩺":"stethoscope","🏛️":"landmark","🏖️":"tree-palm","💶":"euro","📋":"clipboard-list","🏦":"wallet","💵":"banknote","🕒":"clock","📑":"file-text","⏰":"alarm-clock","🎁":"gift","📈":"trending-up","🔁":"repeat","🎄":"tree-pine","🌅":"sunset","📚":"library","📄":"file-text","✍️":"pen-line","❓":"circle-help","❔":"circle-help","🧮":"calculator","✅":"circle-check","📝":"pencil-line","🎉":"party-popper","⏱️":"timer","🔄":"rotate-ccw","⚠️":"triangle-alert","📱":"smartphone","💡":"lightbulb","🔗":"link","🗺️":"map","📖":"book-open","⚡":"zap","🚪":"door-open","✉️":"mail","🤝":"handshake","⏸️":"circle-pause","📕":"file-down","👀":"eye","💰":"piggy-bank","⏳":"hourglass","📉":"trending-down","🏙️":"building-2","📜":"scroll-text","📌":"pin","💻":"laptop","🔍":"search","🔎":"search","🎨":"palette","👥":"users","📬":"mailbox","📍":"map-pin","📰":"newspaper","🥇":"medal","🥈":"medal","🥉":"medal","🔧":"wrench","😟":"frown","👋":"hand","⏩":"fast-forward","☀️":"sun","🛋️":"sofa","🏢":"building","🔢":"hash","📏":"ruler","🛡️":"shield-check","🏨":"hotel","🎯":"target","🔒":"lock","⚙️":"settings","✈️":"plane","📥":"download","🔑":"key-round","🧪":"flask-conical","🎟️":"ticket","⬆️":"arrow-up","➕":"plus","➖":"minus","👶":"baby","👧":"user","👦":"user","👩":"user","👨":"user","👨‍👩‍👧":"users","👩‍👧‍👦":"users","👨‍🔧":"user","👩‍🍳":"user","👩‍💼":"user","👨‍💼":"user","👩‍💻":"user","👨‍💻":"user","👩‍⚕️":"user","👨‍⚕️":"user","🎓":"graduation-cap","🏠":"house","🚗":"car","🍼":"baby","💳":"credit-card","📞":"phone","🌍":"globe","❌":"circle-x","⭐":"star","🔔":"bell","📦":"package","🖨️":"printer","✨":"sparkles","👉":"arrow-right","🏥":"hospital","💊":"pill","🤒":"thermometer","🏗️":"hard-hat","🛒":"shopping-cart","🍽️":"utensils","📧":"mail","🗂️":"folder-open","🧭":"compass","🧑":"user","👤":"user","👩‍🎨":"user","🖼️":"image"};
// ICONOS-FIN
const EMOJI_RE=/(?:[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{231A}-\u{23FF}]\u{FE0F}?)(?:\u{200D}[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]\u{FE0F}?)*/gu;
function iconizar(raiz){
    const nodos=[], recorrido=document.createTreeWalker(raiz,NodeFilter.SHOW_TEXT,{
        acceptNode:n=>n.parentElement&&n.parentElement.closest('script,style,option,textarea,select')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
    const hay=new RegExp(EMOJI_RE.source,'u');            // copia sin «g»: con «g», test() recuerda la posición y falla a saltos
    while(recorrido.nextNode())if(hay.test(recorrido.currentNode.nodeValue))nodos.push(recorrido.currentNode);
    nodos.forEach(n=>{                                    // cada texto con emojis se parte en texto + iconos
        EMOJI_RE.lastIndex=0;
        const html=n.nodeValue.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])).replace(EMOJI_RE,e=>{
            const nombre=ICONOS[e]||ICONOS[e.replace(/️/g,'')]||ICONOS[e+'️'];
            return nombre?'<svg class="ico" aria-hidden="true"><use href="/iconos.svg#i-'+nombre+'"/></svg>':e;
        });
        if(!html.includes('<svg'))return;                // ningún emoji con icono (p. ej. «♥»): no se toca, o se repetiría sin fin
        const t=document.createElement('template'); t.innerHTML=html; n.replaceWith(t.content);
    });
}
if(typeof ICONOS!=='undefined'&&'MutationObserver' in window){
    new MutationObserver(cambios=>cambios.forEach(c=>{
        c.addedNodes.forEach(n=>{if(n.nodeType===1)iconizar(n);else if(n.nodeType===3&&n.parentElement)iconizar(n.parentElement)});
        if(c.type==='characterData'&&c.target.parentElement)iconizar(c.target.parentElement);
    })).observe(document.body,{childList:true,subtree:true,characterData:true});
    iconizar(document.body);                              // por si quedó alguno en la página
}

// ---------- Compartir el resultado como imagen (tarjeta con el logo para WhatsApp o Instagram) ----------
// Se dibuja en el móvil de cada uno (canvas): no se envía nada a ningún servidor.
if(acciones&&document.getElementById('total')){
    const b=document.createElement('button');
    b.type='button'; b.className='btn-secondary btn-imagen'; b.textContent='🖼️ Compartir imagen';
    b.addEventListener('click',compartirImagen);
    acciones.insertBefore(b,acciones.querySelector('.btn-wa'));
}
// Parte un texto en líneas que quepan en «ancho» píxeles
function lineas(ctx,texto,ancho){
    const palabras=texto.split(' '),res=[];let l='';
    palabras.forEach(p=>{const prueba=l?l+' '+p:p;if(ctx.measureText(prueba).width>ancho&&l){res.push(l);l=p}else l=prueba});
    if(l)res.push(l);return res;
}
async function compartirImagen(){
    const T=1080, c=document.createElement('canvas'); c.width=c.height=T;
    const ctx=c.getContext('2d'), fuente='-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif';
    const limpio=t=>(t||'').replace(EMOJI_RE,'').replace(/\s+/g,' ').trim();   // sin emojis (en la imagen no se ven bien)
    // Fondo: el mismo degradado morado que el recuadro del resultado
    const g=ctx.createLinearGradient(0,0,T,T); g.addColorStop(0,'#312E81'); g.addColorStop(1,'#6D28D9');
    ctx.fillStyle=g; ctx.fillRect(0,0,T,T);
    ctx.fillStyle='rgba(255,255,255,0.08)'; ctx.beginPath(); ctx.arc(T*0.9,T*0.1,260,0,7); ctx.fill();   // círculo decorativo
    // Marca arriba
    ctx.textBaseline='top';
    try{const logo=new Image(); logo.src='/favicon.svg?v=2'; await logo.decode(); ctx.drawImage(logo,80,70,72,72)}catch(e){}   // el logo, si carga
    ctx.fillStyle='#fff'; ctx.font='700 46px '+fuente; ctx.fillText('CalculaLoTuyo',172,82);
    // Qué se ha calculado: el título de la página sin «Calculadora…» ni lo que va tras los dos puntos
    const tema=limpio(document.title.split(/[:|]/)[0].replace(/^Calculadora (del |de |de la )?/i,''));
    const etiqueta=limpio((document.querySelector('#result .result-label')||{}).textContent);
    const total=limpio(document.getElementById('total').textContent);
    const sub=limpio((document.getElementById('resultSub')||{}).textContent);
    // Medidas de cada bloque, para centrarlos en el hueco entre la marca y el pie
    ctx.font='700 58px '+fuente; const lTema=lineas(ctx,tema.charAt(0).toUpperCase()+tema.slice(1),T-160).slice(0,2);
    let tam=170; ctx.font='800 '+tam+'px '+fuente;
    while(ctx.measureText(total).width>T-160&&tam>60){tam-=8;ctx.font='800 '+tam+'px '+fuente}   // que la cifra quepa en una línea
    ctx.font='500 40px '+fuente; const lSub=lineas(ctx,sub,T-160).slice(0,3);
    const alto=lTema.length*72+40+(etiqueta?60:0)+tam+30+lSub.length*54;
    let y=180+(T-170-180-alto)/2;
    ctx.fillStyle='#fff'; ctx.font='700 58px '+fuente; lTema.forEach(l=>{ctx.fillText(l,80,y);y+=72}); y+=40;
    if(etiqueta){ctx.fillStyle='rgba(255,255,255,0.7)';ctx.font='600 34px '+fuente;ctx.fillText(etiqueta.toUpperCase(),80,y);y+=60}
    ctx.fillStyle='#fff'; ctx.font='800 '+tam+'px '+fuente; ctx.fillText(total,80,y); y+=tam+30;
    ctx.fillStyle='rgba(255,255,255,0.85)'; ctx.font='500 40px '+fuente; lSub.forEach(l=>{ctx.fillText(l,80,y);y+=54});
    // Pie: dónde calcularlo
    ctx.fillStyle='rgba(255,255,255,0.15)'; ctx.fillRect(0,T-170,T,170);
    ctx.fillStyle='#fff'; ctx.font='600 40px '+fuente;
    ctx.fillText('Calcula el tuyo gratis en',80,T-140);
    ctx.font='800 44px '+fuente; ctx.fillText('calculalotuyo.es/'+PAGINA,80,T-88);
    // Compartir (móvil) o descargar (ordenador)
    const blob=await new Promise(r=>c.toBlob(r,'image/png'));
    const archivo=new File([blob],'calculalotuyo-'+PAGINA+'.png',{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[archivo]})){
        try{await navigator.share({files:[archivo],text:'Calculado en https://calculalotuyo.es/'+PAGINA})}catch(e){}   // si cancela, no pasa nada
    }else{
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=archivo.name; a.click();
        setTimeout(()=>URL.revokeObjectURL(a.href),2000);
    }
}
