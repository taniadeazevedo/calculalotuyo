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
const scriptAnalytics=document.createElement('script');   // crea la etiqueta <script> de Analytics
scriptAnalytics.async=true;                          // que no frene la carga de la página
scriptAnalytics.src='https://www.googletagmanager.com/gtag/js?id='+ID_ANALYTICS;
document.head.appendChild(scriptAnalytics);          // la añade al <head>

// Cualquier enlace con data-cookies vuelve a abrir el mensaje de Google para cambiar la decisión
window.googlefc=window.googlefc||{};                 // objeto que crea el mensaje de Google
googlefc.callbackQueue=googlefc.callbackQueue||[];   // cola de tareas que se ejecutan cuando esté listo
document.querySelectorAll('[data-cookies]').forEach(el=>el.addEventListener('click',e=>{
    e.preventDefault();                              // que el enlace "#" no salte arriba
    googlefc.callbackQueue.push(()=>googlefc.showRevocationMessage());   // muestra otra vez el mensaje
}));
