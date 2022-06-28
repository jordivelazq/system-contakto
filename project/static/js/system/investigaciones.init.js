function investigacionDetail(id) {
    var url = "/investigaciones/investigaciones/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-investigaciones").DataTable({
        "serverSide": true,
        "ajax": "/investigaciones/api/investigaciones/?format=datatables",
        "language": {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        columnDefs: [{
                targets: 4,
                render: function (data, type, full, meta) {
                    var status = {
                        1: {
                            'title': 'Laboral',
                        },
                        2: {
                            'title': 'Socioeconómico',
                        },
                        4: {
                            'title': 'Psicometrías',
                        },
                        5: {
                            'title': 'Visita Domiciliaria',
                        },
                        5: {
                            'title': 'Visita Domiciliaria',
                        },
                        6: {
                            'title': 'Validación de Demandas',
                        },
                        7: {
                            'title': 'Visita Domiciliaria con demandas',
                        },
                    };
                    if (data == null) {
                        return data == null ? "no aplica" : data;
                    }

                    if (typeof status[data] === 'undefined') {
                        // console.log(data);
                        return data;
                    }

                    return status[data].title;

                    //   return '<span class="badge badge-' + status[data].state +
                    //     ' badge-dot">&nbsp;' + status[data].title +
                    //     '</span>';
                },
            },
            {
                targets: 5,
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
                        // console.log(data);
                        return data;
                    }

                    return '<span class="badge rounded-pill badge-soft-' + status[data].state + '">' + status[data].title + '</span>'

                },
            },
            {
                targets: [6],
                render: function (data) {
                    return moment(data).format('DD/MM/YYYY');
                },

            },

        ],
        "columns": [{
                "data": "id",
                "title": "Id",
            },
            {
                "data": "candidato.nombre",
                "title": "Nombres",
                "responsivePriority": 1,
            },
            {
                "data": "candidato.apellido",
                "title": "Apellidos",
                "responsivePriority": 1,
            },
            {
                "data": "compania.nombre",
                "title": "Compañia",
                "responsivePriority": 1,
            },
            {
                "title": "Tipo de Investigación",
                "data": "tipo_investigacion_status",
                "responsivePriority": 2,
            },
            {
                "title": "Resultado",
                "data": "resultado",
                "responsivePriority": 2,
            },
            {
                "data": "fecha_registro",
                "title": "Fecha de Registro"
            },
            {
                "title": "Ver detalles",
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary btn-sm btn-rounded" onclick="investigacionDetail(\'' + row.id + '\')" alt="Editar investigación">Ver detalles</a>';

                    a += '</div>'
                    return a;
                }
            }

        ],
        // dom: 'Blfrtip',
        // buttons: [{
        //     extend: 'copyHtml5',
        //     text: '<i class="fa fa-copy"></i> Copiar',
        //     titleAttr: 'Copiar'
        //   },
        //   {
        //     extend: 'excelHtml5',
        //     text: '<i class="fa fa-file-excel"></i> Excel',
        //     titleAttr: 'Exportar a excel'
        //   },
        //   {
        //     extend: 'csvHtml5',
        //     text: '<i class="fa fa-file-contract"></i> CSV',
        //     titleAttr: 'CSV'
        //   },
        //   {
        //     extend: 'pdfHtml5',
        //     text: '<i class="fa fa-file-pdf"></i> PDF',
        //     titleAttr: 'Exportar a PDF'
        //   }
        // ],
        // lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});