// Calcula el paro de una lista de sueldos con las MISMAS cifras y fórmula que paro.html (datos-2026.js)
// y el neto que cobrabas trabajando con el motor de irpf-2026.js. Escribe paro.json.
const fs=require('fs'),vm=require('vm'),path=require('path');
const raiz=path.join(__dirname,'..','..');
vm.runInThisContext(fs.readFileSync(path.join(raiz,'datos-2026.js'),'utf8')+'\n'+fs.readFileSync(path.join(raiz,'irpf-2026.js'),'utf8')+'\nglobalThis.calcularRetencion=calcularRetencion;globalThis.DATOS=DATOS;');
const P=DATOS.paro, C=DATOS.cotizacion;
const iprem=DATOS.iprem*7/6;                               // IPREM incrementado en 1/6: referencia de los topes
const topes=[0,1,2].map(i=>({max:iprem*P.topeMaximo[i],min:iprem*P.topeMinimo[i]}));   // sin hijos, 1 hijo, 2 o más
// Paro de una base mensual (la base de cotización, que ya incluye la parte de las pagas extra)
function paro(baseMes,hijos){
    const b=Math.min(baseMes,C.baseMaximaMes);              // la base no puede pasar de la máxima
    const t=topes[Math.min(hijos,2)];
    const ajusta=x=>Math.max(t.min,Math.min(x,t.max));     // se aplican el tope mínimo y el máximo
    return {m70:ajusta(b*P.porcentajeInicial),m60:ajusta(b*P.porcentajeDespues),ss:b*C.comunes};
}
const r={smiAnual:DATOS.smi.anual,iprem,topes,duracion:P.duracion,baseMax:C.baseMaximaMes,smiMes:DATOS.smi.mes,sueldos:{}};
const lista=[DATOS.smi.mes];                               // el salario mínimo (1.221 € en 14 pagas)
for(let s=1300;s<=3000;s+=100)lista.push(s);               // de cien en cien hasta 3.000
lista.push(3500,4000,5000);
for(const s of lista){
    r.sueldos[s]={
        doce:[0,1,2].map(h=>paro(s,h)),                     // cobras en 12 pagas o con las extra prorrateadas: base = sueldo
        catorce:[0,1,2].map(h=>paro(s*14/12,h)),            // 14 pagas: la base suma la parte de las dos extra
        netoMes14:calcularRetencion({bruto:s*14,contrato:'indefinido',situacion:3,hijos:0,hijosPorEntero:false,edad:'normal'}).neto/14,   // neto al mes si cobras 14 pagas
        netoMes:calcularRetencion({bruto:s*12,contrato:'indefinido',situacion:3,hijos:0,hijosPorEntero:false,edad:'normal'}).neto/12
    };
}
fs.writeFileSync(path.join(__dirname,'paro.json'),JSON.stringify(r));
console.log('topes',JSON.stringify(topes),'\n1500 →',JSON.stringify(r.sueldos[1500]));
