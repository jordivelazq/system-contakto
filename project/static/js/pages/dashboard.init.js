function getChartColorsArray(e) {
    var e = $(e).attr("data-colors");
    return (e = JSON.parse(e)).map(function (e) {
        e = e.replace(" ", "");
        if (-1 == e.indexOf("--")) return e;
        e = getComputedStyle(document.documentElement).getPropertyValue(e);
        return e || void 0
    })
}

let is_cliente = document.getElementById("is_cliente").value;
if (is_cliente == 1) {


    let cliente_solicitudes_enviadas = document.getElementById("cliente_solicitudes_enviadas").value;
    let cliente_solicitudes_pendientes = document.getElementById("cliente_solicitudes_pendientes").value;
    let total_facturas_por_pagar = document.getElementById("total_facturas_por_pagar").value;
    let total_facturas_pagadas = document.getElementById("total_facturas_pagadas").value;


    var barchartColors = getChartColorsArray("#client-chart1"),
        options = {
            series: [cliente_solicitudes_pendientes, cliente_solicitudes_enviadas],
            labels: ["Pendientes", "Enviadas"],
            chart: {
                type: "donut",
                height: 110
            },
            colors: barchartColors,
            legend: {
                show: !1
            },
            dataLabels: {
                enabled: !1
            }
        },
        chart = new ApexCharts(document.querySelector("#client-chart1"), options);
    chart.render();

    options = {
        series: [total_facturas_pagadas, total_facturas_por_pagar],
        labels: ["Pagadas", "Pendientes",],
        chart: {
            type: "donut",
            height: 110
        },
        colors: barchartColors = getChartColorsArray("#client-chart2"),
        legend: {
            show: !1
        },
        dataLabels: {
            enabled: !1
        }
    };
    (chart = new ApexCharts(document.querySelector("#client-chart2"), options)).render();


}


coord_de_atencion_a_clientes = document.getElementById("coord_de_atencion_a_clientes").value;

if (coord_de_atencion_a_clientes == 1) {

    let en_investigacion = document.getElementById("en_investigacion").value;
    let pte_por_el_cliente = document.getElementById("pte_por_el_cliente").value;
    let inv_terminada = document.getElementById("inv_terminada").value;
   

    options = {
        series: [en_investigacion, pte_por_el_cliente, inv_terminada],
        labels: ["En Investigación", "Pdt. por Cliente", "Inv. Terminada"],
        chart: {
            type: "donut",
            height: 110
        },
        colors: barchartColors = getChartColorsArray("#coord01-chart1"),
        legend: {
            show: !1
        },
        dataLabels: {
            enabled: !1
        }
    };
    (chart = new ApexCharts(document.querySelector("#coord01-chart1"), options)).render();

    // options = {
    //     series: [30, 5, 20],
    //     labels: ["En Investigación", "Pdt. por Cliente", "Inv. Terminada"],

    //     chart: {
    //         type: "donut",
    //         height: 110
    //     },
    //     colors: barchartColors = getChartColorsArray("coord01-chart2"),
    //     legend: {
    //         show: !1
    //     },
    //     dataLabels: {
    //         enabled: !1
    //     }
    // };
    // (chart = new ApexCharts(document.querySelector("#coord01-chart2"), options)).render();

}

var user_login = document.getElementById("login-msg"),
    toastTrigger = document.getElementById("borderedToast1Btn"),
    toastLive = document.getElementById("borderedToast1");
user_login && (toastTrigger.addEventListener("click", function () {
    new bootstrap.Toast(toastLive).show()
}), toastTrigger.click());