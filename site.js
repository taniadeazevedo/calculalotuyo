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
const ID_ANALYTICS='G-Z1JPGHYYP6';

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
    googlefc.callbackQueue.push(()=>googlefc.showRevocationMessage());   // muestra otra vez el mensaje
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
            if(en(p.pt)){puntos+=6;encontradas++}                             // en el título vale más
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
