function investigacionCoordinadoVisitaDetail(id) {
    var url = "/investigaciones/investigaciones/coordinador-visitas/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $.fn.dataTable.moment( 'DD/MM/YYYY' );

    $("#datatable-investigaciones").DataTable({
        "serverSide": false,
        ajax: {
            url : "/investigaciones/api/investigaciones_coordinador_visita/",
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
            {
                targets: [2],
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
                "title": "Fecha de Registro",
                "data": "fecha_registro",
                "responsivePriority": 1,
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
            {
                "title": "Ejecutivo",
                "data": "ejecutivo_visitas.email",
                "defaultContent": "No asignado",
                "responsivePriority": 1,
            },
            {
                "title": "Gestor",
                "data": "agente.email",
                "defaultContent": "No asignado",
            },
            {
                "title": "Cita",
                "data": "cita",
                "defaultContent": "No asignado",
            }

        ],
        "order": [[2, "desc"]],
        dom: 'Blfrtip',
        buttons: [{
            extend: 'copyHtml5',
            text: '<i class="fa fa-copy"></i> Copiar',
            titleAttr: 'Copiar'
        },
            {
                extend: 'excelHtml5',
                text: '<i class="fa fa-file-excel"></i> Excel',
                titleAttr: 'Exportar a excel'
            },
            {
                extend: 'csvHtml5',
                text: '<i class="fa fa-file-contract"></i> CSV',
                titleAttr: 'CSV'
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="fa fa-file-pdf"></i> PDF',
                titleAttr: 'Exportar a PDF'
            }
        ],
        buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});