// =====================================================================
// PRUEBAS AUTOMÁTICAS DE LAS CALCULADORAS
// Ejecuta el código REAL de cada página (el mismo que usa el navegador) con datos de ejemplo
// y comprueba que el resultado es el esperado.
//   node _herramientas/pruebas/pruebas.js            → pasa todas las pruebas
//   node _herramientas/pruebas/pruebas.js --foto     → guarda los resultados actuales como «foto» (tras revisarlos)
// Hay dos tipos de prueba:
//   · «a mano»: cifras calculadas a mano con la ley (si fallan, hay un error de cálculo)
//   · «foto»: el resultado de hoy de cada caso (si cambia, avisa: tras actualizar cifras en enero es normal; revisa y vuelve a hacer la foto)
// =====================================================================
const fs=require('fs'),vm=require('vm'),path=require('path');
const RAIZ=path.join(__dirname,'..','..');
const FOTO=path.join(__dirname,'foto.json');
const leer=f=>fs.readFileSync(path.join(RAIZ,f),'utf8');

// ---------- Un «navegador» mínimo: solo lo que usan las calculadoras ----------
function elemento(id,valor){
    return {id,value:valor??'',textContent:'',innerHTML:'',innerText:'',hidden:false,href:'',checked:false,open:false,
        style:{},dataset:{},className:'',
        classList:{_c:new Set(),add(c){this._c.add(c)},remove(c){this._c.delete(c)},contains(c){return this._c.has(c)},toggle(c,f){(f??!this._c.has(c))?this._c.add(c):this._c.delete(c)}},
        _ev:{},addEventListener(t,f){(this._ev[t]=this._ev[t]||[]).push(f)},dispatchEvent(e){(this._ev[e.type]||[]).forEach(f=>f(e))},
        setAttribute(){},getAttribute(){return null},appendChild(){},insertBefore(){},remove(){},scrollIntoView(){},focus(){},
        querySelector(){return elemento('x')},querySelectorAll(){return[]},closest(){return null},reset(){},
        getBoundingClientRect(){return{top:0,left:0,width:0,height:0}},options:[],selectedIndex:0};
}
// Valores por defecto de los campos, leídos del HTML (value="…" y la opción «selected» o la primera)
function valoresIniciales(html){
    const v={};
    for(const m of html.matchAll(/<input\b[^>]*>/g)){
        const id=(m[0].match(/\bid="([^"]+)"/)||[])[1]; if(!id)continue;
        v[id]=(m[0].match(/\bvalue="([^"]*)"/)||[])[1]??'';
    }
    for(const m of html.matchAll(/<select\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)){
        const ops=[...m[2].matchAll(/<option\b([^>]*)>/g)].map(o=>({v:(o[1].match(/value="([^"]*)"/)||[])[1],sel:/\bselected\b/.test(o[1])}));
        v[m[1]]=(ops.find(o=>o.sel)||ops[0]||{}).v??'';
    }
    return v;
}
// Carga una calculadora y devuelve una función que calcula con los datos que le pases
function pagina(slug){
    const html=leer(slug+'.html');
    const iniciales=valoresIniciales(html);
    return datos=>{
        const els={}, error={m:''}, dcl=[];
        const g=id=>els[id]||(els[id]=elemento(id,iniciales[id]));
        for(const [k,val] of Object.entries(datos))g(k).value=String(val);
        const documento={getElementById:g,querySelector:()=>elemento('x'),querySelectorAll:()=>[],createElement:()=>elemento('nuevo'),
            addEventListener:(t,f)=>{if(t==='DOMContentLoaded')dcl.push(f)},body:elemento('body'),documentElement:elemento('html')};
        const ctx={document:documento,window:{},console,Math,Date,Intl,JSON,Number,String,Array,Object,isNaN,parseFloat,parseInt,encodeURIComponent,setTimeout:()=>0,
            location:{href:''},navigator:{},localStorage:{getItem:()=>null,setItem(){}},
            mostrarError:m=>{error.m=m},
            Option:function(texto,valor,porDefecto,elegida){return {text:texto,value:String(valor),selected:!!elegida}},   // new Option(…) de los desplegables
            fmt:n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0,useGrouping:'always'}).format(n),
            fmtDec:n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',useGrouping:'always'}).format(n)};
        ctx.window=ctx; vm.createContext(ctx);
        // los scripts de la web que usa la página (sin site.js ni los de Google) y después su código propio
        for(const m of html.matchAll(/<script src="([^"?]+)(?:\?[^"]*)?"><\/script>/g))
            if(!/^http|site\.js/.test(m[1]))vm.runInContext(leer(m[1])+'\n;globalThis.DATOS=typeof DATOS!=="undefined"?DATOS:undefined;',ctx);
        for(const m of html.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],ctx);
        dcl.forEach(f=>f());                                              // lo que espera a que cargue la página
        for(const [k,val] of Object.entries(datos))g(k).value=String(val); // por si el código cambió algún campo al arrancar
        const form=g('calc'), ev={type:'submit',preventDefault(){}};
        if(form.onsubmit)form.onsubmit(ev); else form.dispatchEvent(ev);   // pulsa «Calcular»
        return {total:g('total').textContent, sub:g('resultSub').textContent, error:error.m, el:g, todos:els};
    };
}
const euros=t=>+String(t).replace(/[^\d,-]/g,'').replace(',','.');      // «1.225 €/mes» → 1225

// ---------- Casos ----------
// a mano: [descripción, página, datos, función que comprueba el resultado]
const A_MANO=[
    ['Paro: 1.800 €/mes en 14 pagas, 2 años, sin hijos → tope máximo 1.225 € y 8 meses','paro',{sueldoMes:1800,pagas:14,anios:2,meses:0,hijos:0},
        r=>euros(r.total)===1225&&/8 meses/.test(r.el('details').innerHTML)],
    ['Paro: 1.200 €/mes en 12 pagas, 1 año y 6 meses, 1 hijo → 840 € (70 %) y luego el mínimo de 749 €','paro',{sueldoMes:1200,pagas:12,anios:1,meses:6,hijos:1},
        r=>euros(r.total)===840&&/749/.test(r.sub)],
    ['Paro: menos de 1 año trabajado → avisa de que no hay derecho','paro',{sueldoMes:1500,pagas:14,anios:0,meses:9,hijos:0},r=>/al menos 1 año/.test(r.error)],
    ['Despido improcedente: 28.000 €/año, 5 años justos → 33 días × 5 = 12.658 €','despido-improcedente',{salario:28000,inicio:'2021-10-20',despido:'2026-10-19'},
        r=>Math.abs(euros(r.total)-28000/365*33*5)<2],
    ['Lotería: el Gordo (400.000 €) → te llegan 328.000 €','loteria-navidad-hacienda',{premio:'400000',como:'decimo',decimos:1},r=>euros(r.total)===328000],
    ['Lotería: participación de 5 € del Gordo → 82.000 €','loteria-navidad-hacienda',{premio:'400000',como:'participacion',jugado:5},r=>euros(r.total)===82000],
    ['Lotería: cuarto premio (20.000 €) → no paga nada','loteria-navidad-hacienda',{premio:'20000',como:'decimo',decimos:1},r=>euros(r.total)===20000],
    ['Renta: 17.000 € de dos pagadores (3.000 € del segundo) → tiene que declarar','obligado-a-declarar-renta',{trabajo:17000,pagadores:'2',segundo:3000},r=>/Sí/.test(r.total)],
    ['Renta: 21.000 € de un pagador → no está obligado','obligado-a-declarar-renta',{trabajo:21000},r=>/No/.test(r.total)],
    ['Renta: autónomo con 8.000 € → tiene que declarar','obligado-a-declarar-renta',{trabajo:8000,autonomo:'si'},r=>/Sí/.test(r.total)],
];
// foto: [nombre, página, datos] → se compara el resultado con el guardado en foto.json
const FOTOS=[
    ['sueldo-neto 30.000 € 12 pagas','sueldo-neto',{bruto:30000,pagas:12}],
    ['sueldo-neto 20.000 € 14 pagas','sueldo-neto',{bruto:20000,pagas:14}],
    ['irpf 30.000 €','irpf',{ingresos:30000}],
    ['neto-a-bruto 1.500 € 12 pagas','neto-a-bruto',{neto:1500,pagas:12}],
    ['despido-objetivo 2.000 €×14, 10 años','despido-objetivo',{salario:28000,inicio:'2016-10-20',despido:'2026-10-19'}],
    ['ere 32.000 €, 8 años','ere',{salario:32000,inicio:'2018-10-20',ere:'2026-10-19'}],
    ['despido improcedente desde 2005','despido-improcedente',{salario:30000,inicio:'2005-03-01',despido:'2026-10-19',tipo:'pre'}],
    ['finiquito 1.800 €, alta 2023','finiquito',{salario:1800,fechaAlta:'2023-01-10',fechaBaja:'2026-10-20'}],
    ['horas-extra 10 h','horas-extra',{salario:1800,horasExtra:10}],
    ['pagas-extra 1.800 €','pagas-extra',{salario:1800,fechaInicio:'2025-01-01',fechaCalculo:'2026-10-20'}],
    ['vacaciones 1.800 €','vacaciones',{salario:1800,fechaInicio:'2026-01-01',fechaCalculo:'2026-10-20',diasDisfrutados:10}],
    ['subida-ipc 28.000 €','subida-ipc',{salario:28000}],
    ['baja-medica 1.800 €, 30 días','baja-medica',{base:1800,dias:30}],
    ['reduccion-jornada 30.000 €, 25 %','reduccion-jornada',{bruto:30000,reduccion:25,horas:40}],
    ['cuota-autonomos 1.500 €','cuota-autonomos',{ingresos:1500}],
    ['facturas 1.000 €','facturas',{base:1000}],
    ['jubilacion 1970, 30.000 €, 25 años','jubilacion',{nacimiento:'1970-05-10',sueldo:30000,anios:25,meses:0}],
];

// ---------- Ejecutar ----------
const hacerFoto=process.argv.includes('--foto');
const foto=fs.existsSync(FOTO)?JSON.parse(fs.readFileSync(FOTO,'utf8')):{};
let mal=0;
const cache={}; const calc=s=>cache[s]||(cache[s]=pagina(s));
// Números mal redondeados en lo que pinta cada calculadora (p. ej. «7.000000000000001 %»)
const LARGOS=/\d[.,]\d{6,}/;
for(const [nombre,slug,datos] of FOTOS){
    try{const r=calc(slug)(datos);
        for(const [id,el] of Object.entries(r.todos)){const t=String(el.innerHTML||'')+' '+String(el.textContent||'');const m=t.match(LARGOS);
            if(m&&!/^(wa|.*href)/.test(id)){mal++;console.log('❌ '+slug+' · #'+id+' muestra un número sin redondear: '+m[0])}}
    }catch(e){mal++;console.log('❌ '+slug+' · la calculadora da error: '+e.message)}   // antes se callaba
}
// Enlaces rotos: cada href/src interno de todas las páginas tiene que llevar a un archivo que exista
const existe=u=>{u=decodeURIComponent(u.split('#')[0].split('?')[0]).replace(/^\//,'');
    if(u===''||u==='.')return true;                                                   // la portada
    const f=path.join(RAIZ,u);
    return fs.existsSync(f)&&fs.statSync(f).isFile()||fs.existsSync(f+'.html')||fs.existsSync(path.join(f,'index.html'));};
let rotos=0;
for(const pag of fs.readdirSync(RAIZ).filter(f=>f.endsWith('.html'))){
    const html=fs.readFileSync(path.join(RAIZ,pag),'utf8').replace(/<script[\s\S]*?<\/script>/g,'');   // lo de dentro de los scripts no son enlaces
    for(const [,u] of html.matchAll(/(?:href|src)="([^"]*)"/g)){
        if(/^(https?:|mailto:|tel:|#|javascript:|data:|\{)/.test(u)||u==='')continue;   // externos, anclas y plantillas
        if(!existe(u)){rotos++;if(rotos<=20)console.log('❌ enlace roto en '+pag+': '+u)}
    }
}
if(rotos){mal++;console.log((rotos>20?'   … y '+(rotos-20)+' más. ':'')+'❌ '+rotos+' enlace(s) roto(s)')}
else console.log('✅ ningún enlace interno roto');
// Emojis: en la web van iconos propios (iconos.py); si alguno se queda sin icono, avisa (el ♥ del pie es texto)
const EMOJI=/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}]/u;
let emojis=0;
for(const pag of fs.readdirSync(RAIZ).filter(f=>f.endsWith('.html'))){
    const t=fs.readFileSync(path.join(RAIZ,pag),'utf8').replace(/<head>[\s\S]*?<\/head>|<script[\s\S]*?<\/script>/g,'').replace(/<[^>]+>/g,' ').replace(/♥/g,'');
    const m=t.match(EMOJI); if(m){emojis++;if(emojis<=10)console.log('❌ emoji sin icono en '+pag+': '+m[0]+' (añádelo en iconos.py)')}
}
if(emojis)mal++; else console.log('✅ ningún emoji sin icono');
for(const [txt,slug,datos,ok] of A_MANO){
    let r,bien=false; try{r=calc(slug)(datos);bien=ok(r)}catch(e){r={error:e.message}}
    if(!bien)mal++;
    console.log((bien?'✅':'❌')+' '+txt+(bien?'':'  → salió: '+JSON.stringify({total:r.total,sub:r.sub,error:r.error})));
}
const nueva={};
for(const [nombre,slug,datos] of FOTOS){
    let r; try{r=calc(slug)(datos)}catch(e){r={total:'ERROR '+e.message,sub:''}}
    nueva[nombre]=(r.total||'')+' | '+(r.sub||'')+(r.error?' | ERROR: '+r.error:'');
    if(hacerFoto)continue;
    const igual=foto[nombre]===nueva[nombre];
    if(!igual)mal++;
    console.log((igual?'✅':'⚠️ ')+' '+nombre+(igual?'':'\n     antes: '+foto[nombre]+'\n     ahora: '+nueva[nombre]));
}
if(hacerFoto){fs.writeFileSync(FOTO,JSON.stringify(nueva,null,1));console.log('📸 Foto guardada ('+FOTOS.length+' casos). Revísala antes de darla por buena:');for(const [k,v] of Object.entries(nueva))console.log('   '+k+': '+v)}
else console.log(mal?`\n${mal} prueba(s) con problemas: revísalas antes de publicar.`:'\nTodo bien ✅');
process.exit(mal&&!hacerFoto?1:0);
