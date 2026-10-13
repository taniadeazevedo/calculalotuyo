// =====================================================================
// CIFRAS LEGALES 2026 — único sitio donde hay que tocar al cambiar de año.
// Las calculadoras leen de aquí; los textos de las páginas hay que
// repasarlos a mano (busca el año en los .html).
// Última revisión: 8 de octubre de 2026.
// =====================================================================
const DATOS={
    // Salario Mínimo Interprofesional (RD 126/2026)
    smi:{mes:1221,dia:40.70,anual:17094},

    // IPREM mensual (sigue prorrogado en 600 €)
    iprem:600,

    // Cotización al Régimen General (Orden PJC/297/2026)
    cotizacion:{
        comunes:0.0470,              // contingencias comunes (trabajador)
        desempleoIndefinido:0.0155,  // desempleo, contrato indefinido
        desempleoTemporal:0.0160,    // desempleo, contrato de duración determinada
        formacion:0.0010,            // formación profesional
        mei:0.0015,                  // Mecanismo de Equidad Intergeneracional
        baseMaximaMes:5101.20,       // por encima no se cotiza (salvo solidaridad)
        // Cuota de solidaridad del trabajador sobre lo que excede la base máxima: [hasta, tipo]
        solidaridad:[[5611.32,0.0019],[7651.80,0.0021],[Infinity,0.0024]],
        empresa:0.3065               // comunes 23,60 + desempleo 5,50 + FOGASA 0,20 + FP 0,60 + MEI 0,75
    },

    // Retenciones de IRPF sobre el trabajo (arts. 80-86 del Reglamento del IRPF)
    irpf:{
        escala:[[12450,0.19],[20200,0.24],[35200,0.30],[60000,0.37],[300000,0.45],[Infinity,0.47]],
        // Salario a partir del cual se retiene. Fila = situación; columna = 0, 1 o 2+ hijos
        limiteRetener:{
            1:[null,17644,18694],    // monoparental
            2:[17197,18130,19262],   // cónyuge a cargo (rentas <= 1.500 €)
            3:[15876,16342,16867]    // resto
        },
        gastos:2000,                 // gastos deducibles generales
        minimoPersonal:5550,
        minimoHijos:[2400,2700,4000,4500], // 1º, 2º, 3º, 4º y siguientes
        minimoHijoMenor3:2800,
        minimoAscendiente:1150,
        exencionDespido:180000       // indemnización por despido exenta hasta este importe
    },

    // Prestación por desempleo (SEPE)
    paro:{
        porcentajeInicial:0.70,      // primeros 180 días
        porcentajeDespues:0.60,      // desde el día 181
        // Topes en % del IPREM incrementado en 1/6, según hijos a cargo (0, 1, 2+)
        topeMaximo:[1.75,2,2.25],
        topeMinimo:[0.80,1.07,1.07],
        // [días cotizados mínimos, días de prestación]
        duracion:[[360,120],[540,180],[720,240],[900,300],[1080,360],[1260,420],[1440,480],[1620,540],[1800,600],[1980,660],[2160,720]]
    },

    // Autónomos (RETA)
    autonomos:{
        tipo:0.315,                  // 28,30 comunes + 1,30 profesionales + 0,90 cese + 0,10 FP + 0,90 MEI
        tarifaPlana:88.64,           // 80 € + MEI
        baseMinimaSocietario:1000,
        // [rendimiento neto mensual máximo del tramo, base mínima de cotización]
        tramos:[
            [670,653.59],[900,718.95],[1166.69,849.67],[1300,950.98],[1500,960.78],[1700,960.78],
            [1850,1143.79],[2030,1209.15],[2330,1274.51],[2760,1356.21],[3190,1437.91],[3620,1519.61],
            [4050,1601.31],[6000,1732.03],[Infinity,1928.10]
        ]
    },

    // IPC interanual de diciembre de cada año (INE)
    ipc:{2022:5.7,2023:3.1,2024:2.8,2025:2.9}
};
