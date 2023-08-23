

function gestorUpdate(id) {
    var url = "/agente/update/999999999/";
    document.location.href = url.replace('999999999', id);
}

function gestorDelete(id) {
    var url = "/agente/delete/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-gestor-info").DataTable({
        "serverSide": false,
        ajax: {
            url : "/agente/api/gestores/",
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
        "columns": [

            {
                "data": "id",
                "title": "Id",
                "searchable": false,
                "orderable": false,
                "visible": false,    
            },
            {
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'
                    a += '<a class="btn btn-primary" onclick="gestorUpdate(\'' + row.id + '\')"><i class="bx bx-edit-alt font-size-16 align-middle"></i></a>';
                    a += '<a class="btn btn-danger" onclick="gestorDelete(\'' + row.id + '\')"><i class="bx bx bx-trash font-size-16 align-middle"></i></a>';


                    a += '</div>'
                    return a;
                }
            },
            {
                "data": "usuario.first_name",
                "title": "Nombres"
            },
            {
                "data": "usuario.last_name",
                "title": "Apellidos"
            },
            {
                "data": "usuario.email",
                "title": "Email"
            },
            {
                "data": "telefono",
                "title": "Telefono"
            },
            {
                "data": "ciudad",
                "title": "Ciudad"
            },
            {
                "data": "estado",
                "title": "Estado"
            },
            {
                "data": "zona",
                "title": "Zona"
            },
            {
                "data": "fecha_ingreso",
                "title": "Fecha de ingreso"
            },
            {
                "data": "estatus",
                "title": "Estatus"
            },
            {
                "data": "tipo_pago",
                "title": "Tipo de pago"
            },

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