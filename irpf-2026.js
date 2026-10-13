// =====================================================================
// Motor de cálculo compartido: Seguridad Social + retención de IRPF.
// Lo usan sueldo-neto.html e irpf.html para que las dos den el mismo dato.
// Las cifras salen de datos-2026.js (hay que cargarlo antes que este archivo).
// =====================================================================

// Tipo de cotización del trabajador según el contrato (6,50 % o 6,55 %)
function tipoCotizacion(contrato){
    const c=DATOS.cotizacion;
    const desempleo=contrato==='temporal'?c.desempleoTemporal:c.desempleoIndefinido;
    return c.comunes+desempleo+c.formacion+c.mei;
}

// Cotización anual del trabajador, con base máxima y cuota de solidaridad
function cotizacionTrabajador(bruto,contrato){
    const c=DATOS.cotizacion;
    const mes=bruto/12;                                   // la base mensual prorratea las pagas extra
    let cuota=Math.min(mes,c.baseMaximaMes)*tipoCotizacion(contrato);
    let desde=c.baseMaximaMes;                            // inicio del tramo de solidaridad
    for(const [hasta,tipo] of c.solidaridad){
        if(mes<=desde)break;                              // no llega a este tramo
        cuota+=(Math.min(mes,hasta)-desde)*tipo;          // solo la parte dentro del tramo
        desde=hasta;
    }
    return cuota*12;
}

// Aplica la escala progresiva a una base y devuelve cuota, marginal y desglose
function aplicarEscala(base){
    let cuota=0,desde=0,marginal=0;
    const tramos=[];
    for(const [hasta,tipo] of DATOS.irpf.escala){
        if(base<=desde)break;
        const parte=Math.min(base,hasta)-desde;           // euros que caen en este tramo
        cuota+=parte*tipo;
        marginal=tipo;
        tramos.push({desde,hasta:Math.min(base,hasta),tipo,cuota:parte*tipo});
        desde=hasta;
    }
    return {cuota,marginal,tramos};
}

// Reducción por obtención de rendimientos del trabajo (art. 20 LIRPF)
function reduccionTrabajo(rendimientoNeto){
    if(rendimientoNeto<=14852)return 7302;
    if(rendimientoNeto<=17673.52)return 7302-1.75*(rendimientoNeto-14852);
    if(rendimientoNeto<=19747.5)return 2364.34-1.14*(rendimientoNeto-17673.52);
    return 0;
}

// Cálculo completo de la retención anual.
// d = { bruto, contrato:'indefinido'|'temporal', situacion:1|2|3, hijos, hijosMenores3,
//       hijosPorEntero:boolean, edad:'normal'|'65'|'75', discapacidad:0|33|65, ascendientes }
function calcularRetencion(d){
    const bruto=d.bruto;
    const hijos=d.hijos||0;
    const ss=cotizacionTrabajador(bruto,d.contrato);

    // 1. Gastos deducibles: Seguridad Social + 2.000 € generales (+ trabajador activo con discapacidad)
    const f=DATOS.irpf;
    let gastos=f.gastos;
    if(d.discapacidad===33)gastos+=3500;
    if(d.discapacidad===65)gastos+=7750;
    const rendimientoNeto=Math.max(0,bruto-ss-gastos);

    // 2. Reducciones: rendimientos del trabajo y 600 € si hay más de dos hijos.
    // La reducción del art. 20 se mira sobre bruto - cotizaciones, SIN restar los 2.000 € de gastos
    // (así lo hace el algoritmo de retenciones de la Agencia Tributaria: RNT = RETRIB - COTIZACIONES)
    const reduccion=reduccionTrabajo(Math.max(0,bruto-ss))+(hijos>2?600:0);
    const base=Math.max(0,rendimientoNeto-reduccion);

    // 3. Mínimo personal y familiar
    let minimoPersonal=f.minimoPersonal;
    if(d.edad==='65')minimoPersonal+=1150;
    if(d.edad==='75')minimoPersonal+=1150+1400;
    let minimoHijos=0;
    for(let i=0;i<hijos;i++)minimoHijos+=f.minimoHijos[Math.min(i,3)]; // 1º, 2º, 3º, 4º y siguientes
    minimoHijos+=(d.hijosMenores3||0)*f.minimoHijoMenor3;               // extra por cada menor de 3 años
    if(!d.hijosPorEntero)minimoHijos/=2;                  // si lo comparten los dos progenitores
    const minimoAscendientes=(d.ascendientes||0)*f.minimoAscendiente;
    const minimoDiscapacidad=d.discapacidad===33?3000:d.discapacidad===65?12000:0; // 65 %: 9.000 € + 3.000 € de gastos de asistencia
    const minimo=minimoPersonal+minimoHijos+minimoAscendientes+minimoDiscapacidad;

    // 4. Cuota = escala sobre la base - escala sobre el mínimo (el mínimo NO se resta de la base)
    const escalaBase=aplicarEscala(base);
    const escalaMinimo=aplicarEscala(Math.min(minimo,base));
    let cuota=Math.max(0,escalaBase.cuota-escalaMinimo.cuota);

    // 5. Límites: por debajo del umbral no se retiene y hasta 35.200 € la cuota tiene tope del 43 %
    const situacion=(d.situacion===1&&hijos===0)?3:d.situacion;
    const limite=f.limiteRetener[situacion][Math.min(hijos,2)];
    const exento=bruto<=limite;
    const tope43=0.43*(bruto-limite);
    const limite43=!exento&&bruto<=35200&&cuota>tope43;   // ¿se ha aplicado el tope del 43 %?
    if(exento)cuota=0;
    else if(limite43)cuota=tope43;

    // 6. Tipo de retención con mínimo del 2 % en contratos de menos de un año.
    // Hacienda trunca el tipo al segundo decimal (no redondea); el 1e-9 evita que 16,42 se quede en 16,41
    let tipo=bruto>0?Math.floor(cuota/bruto*10000+1e-9)/100:0;
    const minimoTemporal=d.contrato==='temporal'&&tipo<2;
    if(minimoTemporal)tipo=2;
    const irpf=bruto*tipo/100;

    return {bruto,ss,tipoSS:tipoCotizacion(d.contrato),gastos,rendimientoNeto,reduccion,base,
        minimo,minimoPersonal,minimoHijos,cuotaBase:escalaBase.cuota,cuotaMinimo:escalaMinimo.cuota,
        tramos:escalaBase.tramos,marginal:exento?0:escalaBase.marginal,limite,exento,limite43,minimoTemporal,
        tipo,irpf,neto:bruto-ss-irpf,
        costeEmpresa:bruto+Math.min(bruto,DATOS.cotizacion.baseMaximaMes*12)*DATOS.cotizacion.empresa};
}
