function investigacionCoordinadoVisitaDetail(id) {
    var url = "/investigaciones/investigaciones/adjuntos/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-investigaciones").DataTable({
        "serverSide": true,
        "ajax": "/investigaciones/api/investigaciones_adjuntos/?format=datatables",
        "language": {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        columnDefs: [
            // {
            //     targets: 5,
            //     className: 'dt-body-center', 
            //     render: function (data, type, row) {
            //         if (data==true){
            //             return '<i class="fa fa-check"></i>';
            //         }else{
            //             return '<i class="fa fa-times"></i>';
            //         }
            //     },
            // },
            // {
            //     targets: 6,
            //     className: 'dt-body-center', 
            //     render: function (data, type, row) {
            //         if (data==true){
            //             return '<i class="fa fa-check"></i>';
            //         }else{
            //             return '<i class="fa fa-times"></i>';
            //         }
            //     },
            // },
            // {
            //     targets: 7,
            //     className: 'dt-body-center', 
            //     render: function (data, type, row) {
            //         if (data==true){
            //             return '<i class="fa fa-check"></i>';
            //         }else{
            //             return '<i class="fa fa-times"></i>';
            //         }
            //     },
            // },
            {
                targets: [5],
                render: function (data) {
                    return moment(data).format('DD/MM/YYYY');
                },

            },

        ],
        "columns": [{
                "title": "Id",
                "data": "id",
                "visible": false,
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
                "title": "Nombres",
                "data": "candidato.nombre",
                "responsivePriority": 1,
            },
            {
                "title": "Apellidos",
                "data": "candidato.apellido",
                "responsivePriority": 1,
            },
            {
                "title": "Cliente",
                "data": "compania.nombre",
                "responsivePriority": 1,
            },
            // {
            //     "title": "Psicométrico",
            //     "data": "psicometrico",
            // },
            // {
            //     "title": "Ejecutivo Asignado",
            //     "data": "psicometrico_ejecutivo_asignado",
            // },
            // {
            //     "title": "Datos Psicometricos completados",
            //     "data": "psicometrico_ejecutivo_asignado",
            // },
            {
                "title": "Fecha de Registro",
                "data": "fecha_registro",
            }

        ],
        "order": [[5, "desc"]],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});