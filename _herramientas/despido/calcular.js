// Calcula indemnizaciones con el MISMO motor que la web (despido.js) para varias antigüedades y sueldos.
// Fecha de despido de referencia: la de hoy al generar. Escribe despido.json.
const fs=require('fs'),vm=require('vm'),path=require('path');
const raiz=path.join(__dirname,'..','..');
vm.runInThisContext(fs.readFileSync(path.join(raiz,'despido.js'),'utf8')+'\nglobalThis.indemnizacionImprocedente=indemnizacionImprocedente;globalThis.mesesProrrateados=mesesProrrateados;globalThis.diaSiguiente=diaSiguiente;');
const HOY=new Date(Date.UTC(2026,9,19));                      // 19/10/2026: fecha del despido en los ejemplos
const sueldosMes=[1300,1500,2000,2500,3000];                  // brutos al mes en 14 pagas
const anios=[];for(let a=1;a<=25;a++)anios.push(a);
const r={hoy:'2026-10-19',sueldosMes,datos:{}};
for(const a of anios){
    const inicio=new Date(Date.UTC(2026-a,9,20));             // empezó el 20/10: con el día del despido incluido son "a" años justos
    r.datos[a]={inicio:inicio.toISOString().slice(0,10),sueldos:{}};
    for(const sm of sueldosMes){
        const anual=sm*14;
        const imp=indemnizacionImprocedente(anual,inicio,HOY);  // improcedente: 33 días (y 45 antes de 2012)
        // objetivo: 20 días por año, máximo 12 mensualidades (igual que despido-objetivo.html)
        const meses=mesesProrrateados(inicio,diaSiguiente(HOY));
        let obj=anual/365*20*meses/12; const objTope=obj>anual; if(objTope)obj=anual;
        const temporal=anual/365*12*meses/12;                    // fin de contrato temporal: 12 días por año
        r.datos[a].sueldos[sm]={anual,diario:anual/365,imp:imp.importe,impDias:imp.dias,pre:imp.pre,mesesPre:imp.mesesPre,mesesPost:imp.mesesPost,tramoPre:imp.tramoPre,tramoPost:imp.tramoPost,tope:imp.tope,obj,objTope,temporal,meses};
    }
}
fs.writeFileSync(path.join(__dirname,'despido.json'),JSON.stringify(r));
for(const a of [1,5,10,15,20])console.log(a,'años, 2.000 €/mes →',JSON.stringify(r.datos[a].sueldos[2000],(k,v)=>typeof v==='number'?Math.round(v*100)/100:v));
