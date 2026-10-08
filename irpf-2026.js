// =====================================================================
// Motor de cálculo compartido: Seguridad Social + retención de IRPF 2026
// Lo usan sueldo-neto.html e irpf.html para que las dos den el mismo dato.
// Fuentes: Orden PJC/297/2026 (cotización) y arts. 80-86 del Reglamento
// del IRPF (procedimiento general de retenciones sobre el trabajo).
// =====================================================================

// --- Cotización del trabajador (Régimen General, 2026) ---
const COTIZACION_2026={
    comunes:0.0470,              // contingencias comunes
    desempleoIndefinido:0.0155,  // desempleo, contrato indefinido
    desempleoTemporal:0.0160,    // desempleo, contrato de duración determinada
    formacion:0.0010,            // formación profesional
    mei:0.0015,                  // Mecanismo de Equidad Intergeneracional
    baseMaximaMes:5101.20,       // por encima de esta base no se cotiza (salvo solidaridad)
    // Cuota de solidaridad: parte del trabajador sobre lo que excede la base máxima
    solidaridad:[[5611.32,0.0019],[7651.80,0.0021],[Infinity,0.0024]],
    empresa:0.3065               // comunes 23,60 + desempleo 5,50 + FOGASA 0,20 + FP 0,60 + MEI 0,75
};

// --- Escala de retención del IRPF (tope del tramo, tipo) ---
const ESCALA_IRPF=[[12450,0.19],[20200,0.24],[35200,0.30],[60000,0.37],[300000,0.45],[Infinity,0.47]];

// --- Salario a partir del cual hay que retener (art. 81 RIRPF) ---
// Fila = situación, columna = 0, 1 o 2+ hijos
const LIMITE_RETENER={
    1:[null,17644,18694],   // monoparental (soltero/viudo/divorciado con hijos en exclusiva)
    2:[17197,18130,19262],  // cónyuge a cargo (rentas del cónyuge <= 1.500 €)
    3:[15876,16342,16867]   // resto de situaciones
};

// Tipo de cotización del trabajador según el contrato (6,50 % o 6,55 %)
function tipoCotizacion(contrato){
    const c=COTIZACION_2026;
    const desempleo=contrato==='temporal'?c.desempleoTemporal:c.desempleoIndefinido;
    return c.comunes+desempleo+c.formacion+c.mei;
}

// Cotización anual del trabajador, con base máxima y cuota de solidaridad
function cotizacionTrabajador(bruto,contrato){
    const c=COTIZACION_2026;
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
    for(const [hasta,tipo] of ESCALA_IRPF){
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
    let gastos=2000;
    if(d.discapacidad===33)gastos+=3500;
    if(d.discapacidad===65)gastos+=7750;
    const rendimientoNeto=Math.max(0,bruto-ss-gastos);

    // 2. Reducciones: rendimientos del trabajo y 600 € si hay más de dos hijos
    const reduccion=reduccionTrabajo(rendimientoNeto)+(hijos>2?600:0);
    const base=Math.max(0,rendimientoNeto-reduccion);

    // 3. Mínimo personal y familiar
    let minimoPersonal=5550;
    if(d.edad==='65')minimoPersonal+=1150;
    if(d.edad==='75')minimoPersonal+=1150+1400;
    const porHijo=[2400,2700,4000,4500];                  // 1º, 2º, 3º, 4º y siguientes
    let minimoHijos=0;
    for(let i=0;i<hijos;i++)minimoHijos+=porHijo[Math.min(i,3)];
    minimoHijos+=(d.hijosMenores3||0)*2800;               // extra por cada menor de 3 años
    if(!d.hijosPorEntero)minimoHijos/=2;                  // si lo comparten los dos progenitores
    const minimoAscendientes=(d.ascendientes||0)*1150;
    const minimoDiscapacidad=d.discapacidad===33?3000:d.discapacidad===65?9000:0;
    const minimo=minimoPersonal+minimoHijos+minimoAscendientes+minimoDiscapacidad;

    // 4. Cuota = escala sobre la base - escala sobre el mínimo (el mínimo NO se resta de la base)
    const escalaBase=aplicarEscala(base);
    const escalaMinimo=aplicarEscala(Math.min(minimo,base));
    let cuota=Math.max(0,escalaBase.cuota-escalaMinimo.cuota);

    // 5. Límites: por debajo del umbral no se retiene y hasta 35.200 € la cuota tiene tope del 43 %
    const situacion=(d.situacion===1&&hijos===0)?3:d.situacion;
    const limite=LIMITE_RETENER[situacion][Math.min(hijos,2)];
    const exento=bruto<=limite;
    const tope43=0.43*(bruto-limite);
    const limite43=!exento&&bruto<=35200&&cuota>tope43;   // ¿se ha aplicado el tope del 43 %?
    if(exento)cuota=0;
    else if(limite43)cuota=tope43;

    // 6. Tipo de retención (2 decimales) con mínimo del 2 % en contratos de menos de un año
    let tipo=bruto>0?Math.round(cuota/bruto*10000)/100:0;
    const minimoTemporal=d.contrato==='temporal'&&tipo<2;
    if(minimoTemporal)tipo=2;
    const irpf=bruto*tipo/100;

    return {bruto,ss,tipoSS:tipoCotizacion(d.contrato),gastos,rendimientoNeto,reduccion,base,
        minimo,minimoPersonal,minimoHijos,cuotaBase:escalaBase.cuota,cuotaMinimo:escalaMinimo.cuota,
        tramos:escalaBase.tramos,marginal:exento?0:escalaBase.marginal,limite,exento,limite43,minimoTemporal,
        tipo,irpf,neto:bruto-ss-irpf,
        costeEmpresa:bruto+Math.min(bruto,COTIZACION_2026.baseMaximaMes*12)*COTIZACION_2026.empresa};
}
