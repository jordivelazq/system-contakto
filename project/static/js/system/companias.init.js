function companiaDetail(id) {
    var url = "/empresa/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {
    $("#datatable-companias").DataTable({
        "serverSide": false,
        ajax: {
            url : "/empresa/api/companias/",
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
        //     {
        //     targets: 3,
        //     className: 'dt-body-center',
        //     render: function (data, type, row) {
        //         if (data == true) {
        //             return '<i class="fa fa-check"></i>';
        //         } else {
        //             return '<i class="fa fa-times"></i>';
        //         }
        //     },
        // },
     ],
        "columns": [
            {
                "title": "Acciones",
                "data": null,
                "orderable": false,
                "searchable": false,
              
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary btn-sm btn-rounded" onclick="companiaDetail(\'' + row.id + '\')" alt="Ver detalle del cliente">Ver detalles</a>';

                    a += '</div>'
                    return a;
                }
            },
            {"data": "id", "title": "Id", "searchable": false, "visible": false},
            {"data": "nombre", "title": "Cliente", "responsivePriority": 1,},
            // {"data": "es_cliente", "title": "Es cliente", "searchable": false, "responsivePriority": 1,},           
            {
                "data": "coordinador_ejecutivos", 
                "title": "Coord. Atn. Ctes.", 
                "responsivePriority": 1,
                // "orderable": false,
                "searchable": false,
                "render": function (data, type, row, meta) {
                    if (data == null) {
                        return "";
                    } else {
                        return data.first_name + " " + data.last_name;
                    }
                }

            },           
            {"data": "telefono", "title": "Teléfono"},
            {"data": "telefono_alt", "title": "Teléfono alterno"},
            {"data": "email", "title": "Correo Electrónico"},
            {"data": "role", "title": "Giro"},
            {"data": "rfc_direccion", "title": "Dirección fiscal"},
            {"data": "rfc", "title": "RFC"},
            {"data": "notas", "title": "Notas"},
            {"data": "razon_social", "title": "Razón Social"},
            {"data": "referencia_correo", "title": "Referencia por correo"},
        ],
        lengthChange: !1,
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
