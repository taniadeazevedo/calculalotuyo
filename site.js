// =====================================================================
// JavaScript común a todas las páginas: formato de euros, menú,
// preguntas frecuentes, errores de formulario y aviso de cookies.
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

// ---------- Cookies: Analytics y AdSense solo con consentimiento ----------
const ID_ANALYTICS='G-Z1JPGHYYP6';
const ID_ADSENSE='ca-pub-4853214655991551';
const CLAVE_COOKIES='clt-cookies';                   // guarda 'si' o 'no' en el navegador

function leerConsentimiento(){
    try{return localStorage.getItem(CLAVE_COOKIES)}catch(e){return null}   // modo privado: sin almacenamiento
}
function guardarConsentimiento(valor){
    try{localStorage.setItem(CLAVE_COOKIES,valor)}catch(e){}
}
function cargarScript(src,atributos){
    const s=document.createElement('script');
    s.async=true;s.src=src;
    Object.assign(s,atributos||{});
    document.head.appendChild(s);
}
let tercerosCargados=false;
function cargarTerceros(){
    if(tercerosCargados)return;                      // no cargarlos dos veces
    tercerosCargados=true;
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){dataLayer.push(arguments)};
    gtag('js',new Date());
    gtag('config',ID_ANALYTICS);
    cargarScript('https://www.googletagmanager.com/gtag/js?id='+ID_ANALYTICS);
    cargarScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+ID_ADSENSE,{crossOrigin:'anonymous'});
}
function mostrarAvisoCookies(){
    if(document.getElementById('cookieBanner'))return;
    const aviso=document.createElement('div');
    aviso.id='cookieBanner';
    aviso.className='cookie-banner';
    aviso.setAttribute('role','dialog');
    aviso.setAttribute('aria-label','Aviso de cookies');
    aviso.innerHTML=
        '<p>Usamos cookies de Google Analytics y Google AdSense para medir las visitas y mostrar publicidad. '+
        'Solo se activan si las aceptas. <a href="cookies">Ver la política de cookies</a></p>'+
        '<div class="cookie-banner-actions">'+
        '<button type="button" class="cookie-btn" data-respuesta="no">Rechazar</button>'+
        '<button type="button" class="cookie-btn cookie-btn-primary" data-respuesta="si">Aceptar</button>'+
        '</div>';
    aviso.addEventListener('click',e=>{
        const respuesta=e.target.dataset.respuesta;
        if(!respuesta)return;                        // clic en el texto, no en un botón
        const anterior=leerConsentimiento();
        guardarConsentimiento(respuesta);
        aviso.remove();
        if(respuesta==='si')cargarTerceros();
        else if(anterior==='si')location.reload();   // al retirar el permiso se recarga sin los scripts
    });
    document.body.appendChild(aviso);
}
// Al entrar: si ya aceptó, se cargan; si no ha contestado, se pregunta
const consentimiento=leerConsentimiento();
if(consentimiento==='si')cargarTerceros();
else if(consentimiento===null)mostrarAvisoCookies();
// Cualquier elemento con data-cookies vuelve a abrir el aviso para cambiar la decisión
document.querySelectorAll('[data-cookies]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();mostrarAvisoCookies()}));
