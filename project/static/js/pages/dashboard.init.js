function getChartColorsArray(e) {
    var e = $(e).attr("data-colors");
    return (e = JSON.parse(e)).map(function (e) {
        e = e.replace(" ", "");
        if (-1 == e.indexOf("--")) return e;
        e = getComputedStyle(document.documentElement).getPropertyValue(e);
        return e || void 0
    })
}
var barchartColors = getChartColorsArray("#client-chart1"),
    options = {
        series: [0, 1],
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
    series: [1, 2],
    labels: ["Pendientes", "Pagadas"],
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

options = {
    series: [30, 5, 20],
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

options = {
    series: [30, 5, 20],
    labels: ["En Investigación", "Pdt. por Cliente", "Inv. Terminada"],

    chart: {
        type: "donut",
        height: 110
    },
    colors: barchartColors = getChartColorsArray("coord01-chart2"),
    legend: {
        show: !1
    },
    dataLabels: {
        enabled: !1
    }
};
(chart = new ApexCharts(document.querySelector("#coord01-chart2"), options)).render();


var user_login = document.getElementById("login-msg"),
    toastTrigger = document.getElementById("borderedToast1Btn"),
    toastLive = document.getElementById("borderedToast1");
user_login && (toastTrigger.addEventListener("click", function () {
    new bootstrap.Toast(toastLive).show()
}), toastTrigger.click());