function investigacionDetail(id) {
    var url = "/investigaciones/investigaciones/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-investigaciones").DataTable({
        processing: true,
        serverSide: true,
        ajax: "/investigaciones/api/investigaciones/?format=datatables",
        language: {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        pageLength: 50,
        lengthMenu: [
          [25, 50, 100, -1],
          [25, 50, 100, "All"]
        ],
        columnDefs: [
            {
                targets: 6,
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
                targets: 9,
                render: function (data, type, full, meta) {
                    var status = {
                        0: {
                            'title': 'Por evaluar',
                            'state': 'warning',
                        },
                        1: {
                            'title': 'Viable',
                            'state': 'success',
                        },
                        2: {
                            'title': 'No viable',
                            'state': 'danger',
                        },
                        3: {
                            'title': 'Con reservas',
                            'state': 'info',
                        },
                        4: {
                            'title': 'Cancelado',
                            'state': 'secondary',
                        },
                    };
                    if (data == null) {
                        return data == null ? "no aplica" : data;
                    }

                    if (typeof status[data] === 'undefined') {
                        return data;
                    }

                    return '<span class="badge rounded-pill badge-soft-' + status[data].state + '">' + status[data].title + '</span>'

                },
            },
            {
                targets: [2],
                render: function (data) {
                    return moment(data).format('DD/MM/YYYY');
                },

            },

        ],
        "columns": [
            {
                "title": "Id",
                "data": "id",
                "visible": false,
            },
            {
                title: "Ver detalles",
                data: null,
                orderable: false,
                searchable: false,
                width: "65px",
                render: function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-soft-primary waves-effect waves-light" onclick="investigacionDetail(\'' + row.id + '\')"><i class="bx bxs-search label-icon"></i></a>';

                    a += '</div>'
                    return a;
                }
            },
            {
                title: "Fecha de Registro",
                data: "fecha_registro",
                responsivePriority: 1,
            },
            {
                title: "Hora",
                data: "hora_recibido",
                responsivePriority: 1,
            },
            {
                title: "Nombres",
                data: "candidato.nombre",
                responsivePriority: 1,
            },
            {
                title: "Apellidos",
                data: "candidato.apellido",
                responsivePriority: 1,
            },
            {
                title: "Datos verificados",
                data: "candidato.datos_validados",
                responsivePriority: 2,
            },
            {
                title: "Cliente",
                data: "compania.nombre",
                responsivePriority: 2,
            },
            {
                title: "Tipo de Investigación",
                data: 'tipo_investigacion',
                searchable: false,
                responsivePriority: 2,
                 render: function (data, type, row, meta) {
                    if(row.tipo_investigacion != undefined)
                        return row.tipo_investigacion;
                    return 'N/A';
                }
            },
            {
                title: "Resultado",
                data: "resultado",
                responsivePriority: 2,
                searchable: false,
            },
            {
                "title": "Estatus",
                data: "status",
                responsivePriority: 2,
            },
            {
                "title": "Asignado",
                "data": "agente_name",
                "responsivePriority": 2,
                "render": function (data, type, row, meta) {
                    if (row.agente_name != undefined)
                        return '<i class="fa fa-check text-success"></i>';
                    return '<i class="fa fa-times text-danger"></i>';
                }
            },

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
        lengthChange: !1,
        buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});