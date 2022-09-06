function investigacionCoordinadoVisitaDetail(id) {
    var url = "/investigaciones/investigaciones/coordinador-visitas/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-investigaciones").DataTable({
        "serverSide": true,
        "ajax": "/pagos_a_gestores/api/gestor_investifaciones_pagos/?format=datatables",
        "language": {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        columnDefs: [
            {
                targets: 5,
                className: 'dt-body-center', 
                render: function (data, type, row) {
                    if (data==true){
                        return '<i class="fa fa-check"></i>';
                    }else{
                        return '<i class="fa fa-times"></i>';
                    }
                },
            },
            {
                targets: [4],
                render: function (data) {
                    return moment(data).format('DD/MM/YYYY HH:mm');
                },

            },

        ],
        
        "columns": [{
                "title": "Id",
                "data": "id",
            },
            {
                "title": "Ver detalles",
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary btn-sm btn-rounded" onclick="investigacionCoordinadoVisitaDetail(\'' + row.id + '\')" alt="Ver detalle">Ver detalles</a>';

                    a += '</div>'
                    return a;
                }
            },
            {
                "title": "Gestor Nombre",
                "data": "gestor.usuario.first_name",
                "responsivePriority": 1,
            },
            {
                "title": "Gestor Apellido",
                "data": "gestor.usuario.last_name",
                "responsivePriority": 1,
            },
            {
                "title": "Fecha de pago",
                "data": "fecha_de_pago",
            },
            {
                "title": "Pagado",
                "data": "pagado",
                "responsivePriority": 1,
            },
           

           

        ],
        "order": [[5, "desc"]],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});