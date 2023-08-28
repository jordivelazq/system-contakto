
function personaDetail(id) {
    var url = "/personas/personas/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {
    $.fn.dataTable.moment( 'DD/MM/YYYY' );
    
    $("#datatable-personas").DataTable({
        "serverSide": false,
        ajax: {
            url : "/personas/api/personas/",
            dataSrc: "results",
        },
        "language": {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        pageLength: 100,
        lengthMenu: [
            [25, 50, 100, -1],
            [25, 50, 100, "Todos"]
        ],
        columnDefs: [
            {
                targets: 17,
                render: function (data) {
                    return moment(data).format('DD/MM/YYYY');
                },

            },
            {
                targets: 18,
                className: 'dt-body-center', 
                render: function (data, type, row) {
                    if (data==true){
                        return '<i class="fa fa-check"></i>';
                    }else{
                        return '<i class="fa fa-times"></i>';
                    }
                },
            },
        ],
        "columns": [
            {"data": "id", "title": "Id", "searchable": false, "visible": false},
            {
                "title": "Ver detalles",
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary btn-sm btn-rounded" onclick="personaDetail(\'' + row.id + '\')" alt="Ver detalles">Ver detalles</a>';

                    a += '</div>'
                    return a;
                }
            },
            {"data": "nombre", "title": "Nombres"},
            {"data": "apellido", "title": "Apellidos"},
            {"data": "nss", "title": "NSS"},
            {"data": "email", "title": "Email"},
            {"data": "edad", "title": "Edad"},
            {"data": "curp", "title": "CURP"},
            {"data": "rfc", "title": "RCF"},
            {"data": "ife", "title": "IFE"},
            {"data": "pasaporte", "title": "Pasaporte"},
            {"data": "smn", "title": "SMN"},
            {"data": "estado_civil", "title": "Estado civil"},
            {"data": "fecha_matrimonio", "title": "Fecha Matrimonio"},
            {"data": "religion", "title": "Religión"},
            {"data": "tiempo_radicando", "title": "Tiempo radicado"},
            {"data": "medio_utilizado", "title": "Medio utilizado"},
            {"data": "fecha_registro", "title": "Fecha registro"},
            {"data": "estatus", "title": "Estado"},
           
        ],
        lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
          },
    });
});
