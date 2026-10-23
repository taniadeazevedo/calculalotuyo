// =====================================================================
// Funciones compartidas por las calculadoras de despido
// (despido-improcedente, despido-objetivo y ere).
// =====================================================================

// Fecha de entrada en vigor de la reforma laboral de 2012
const CORTE_2012=new Date('2012-02-12');

// Meses entre dos fechas; la fracción de mes cuenta como mes completo
// ("prorrateándose por meses los periodos inferiores a un año", arts. 53 y 56 ET)
function mesesProrrateados(desde,hasta){
    let m=(hasta.getUTCFullYear()-desde.getUTCFullYear())*12+hasta.getUTCMonth()-desde.getUTCMonth();
    if(hasta.getUTCDate()<desde.getUTCDate())m--;              // el último mes no está completo
    const ref=new Date(desde);ref.setUTCMonth(ref.getUTCMonth()+m);
    if(hasta>ref)m++;                                          // sobran días: se redondea al alza
    return Math.max(0,m);
}

// El día del despido también se trabaja: el periodo acaba al día siguiente
function diaSiguiente(fecha){return new Date(fecha.getTime()+864e5)}

// Indemnización legal por despido improcedente (art. 56 ET y disp. transitoria 11ª)
function indemnizacionImprocedente(salarioAnual,inicio,despido){
    const pre=inicio<CORTE_2012;                               // contrato anterior a la reforma
    const fin=diaSiguiente(despido);
    const diario=salarioAnual/365;
    // Si el despido fue antes de la reforma, el tramo de 45 días llega solo hasta el despido (no hasta el corte)
    const finPre=fin<CORTE_2012?fin:CORTE_2012;
    const mesesPre=pre?mesesProrrateados(inicio,finPre):0;
    const mesesPost=fin>CORTE_2012?mesesProrrateados(pre?CORTE_2012:inicio,fin):0;
    const diasPre=mesesPre*45/12;                              // 45 días por año hasta el 11/02/2012
    const diasPost=mesesPost*33/12;                            // 33 días por año desde el 12/02/2012
    // Topes: 720 días de salario; si el tramo anterior a 2012 ya los supera, ese importe (máx. 42 mensualidades)
    let dias,tope='';
    if(pre&&diasPre>720){
        dias=Math.min(diasPre,1260);
        tope=diasPre>1260?'42 mens.':'Tramo pre-2012';
    }else{
        dias=diasPre+diasPost;
        if(dias>720){dias=720;tope='720 días'}
    }
    return {pre,diario,mesesPre,mesesPost,meses:mesesPre+mesesPost,
        tramoPre:diario*diasPre,tramoPost:diario*diasPost,dias,tope,importe:diario*dias};
}
