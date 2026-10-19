// Calcula el neto de una lista de sueldos con el MISMO motor que la web (datos-2026.js + irpf-2026.js)
// Uso: node _herramientas/sueldos/calcular.js  → escribe _herramientas/sueldos/sueldos.json
const fs=require('fs'),vm=require('vm'),path=require('path');
const raiz=path.join(__dirname,'..','..');
// Carga los dos archivos de la web como si fueran <script> del navegador
vm.runInThisContext(fs.readFileSync(path.join(raiz,'datos-2026.js'),'utf8')+'\n'+fs.readFileSync(path.join(raiz,'irpf-2026.js'),'utf8')+'\nglobalThis.calcularRetencion=calcularRetencion;globalThis.DATOS=DATOS;');
// Casos que se enseñan en cada página
const casos={
    base:{contrato:'indefinido',situacion:3,hijos:0,hijosPorEntero:false,edad:'normal'},        // sin hijos, indefinido
    hijo1:{contrato:'indefinido',situacion:3,hijos:1,hijosPorEntero:false,edad:'normal'},       // 1 hijo, mínimo a medias con el otro progenitor
    hijos2:{contrato:'indefinido',situacion:3,hijos:2,hijosPorEntero:false,edad:'normal'},      // 2 hijos, a medias
    temporal:{contrato:'temporal',situacion:3,hijos:0,hijosPorEntero:false,edad:'normal'}       // contrato temporal, sin hijos
};
const sueldos=[];
for(let b=17000;b<=60000;b+=1000)sueldos.push(b);          // de mil en mil hasta 60.000
for(let b=65000;b<=100000;b+=5000)sueldos.push(b);         // y de cinco en cinco mil hasta 100.000
sueldos.push(DATOS.smi.anual);                             // el salario mínimo
const r={smi:DATOS.smi.anual,datos:{}};
for(const bruto of sueldos.sort((a,b)=>a-b)){
    r.datos[bruto]={};
    for(const [k,c] of Object.entries(casos)){
        const x=calcularRetencion({bruto,...c});
        r.datos[bruto][k]={neto:x.neto,ss:x.ss,irpf:x.irpf,tipo:x.tipo,coste:x.costeEmpresa};
    }
}
fs.writeFileSync(path.join(__dirname,'sueldos.json'),JSON.stringify(r));
console.log('sueldos:',sueldos.length,'· 30.000 →',JSON.stringify(r.datos[30000].base));
