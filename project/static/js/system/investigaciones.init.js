
function investigacionUpdate(id) {
    var url = "/investigaciones/investigaciones/update/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {   

    $("#datatable-investigaciones").DataTable({
        "serverSide": true,
        "ajax": "/investigaciones/api/investigaciones/?format=datatables",
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
                targets: [5],
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
                "title": "Nombres"
            },
            {
                "data": "candidato.apellido",
                "title": "Apellidos"
            },
            {
                "data": "compania.nombre",
                "title": "Compañia"
            },
            {
                "title": "Tipo de Investigación",
                "data": "tipo_investigacion_status",
                "responsivePriority": 1,
            },
            {
                "data": "fecha_registro",
                "title": "Fecha de Registro"
            },
            {
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary" onclick="investigacionUpdate(\'' + row.id + '\')" alt="Editar investigación"><i class="bx bxs-edit font-size-16 align-middle"></i></a>';

                    a += '</div>'
                    return a;
                }
            }

        ],
        // lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
        },
    });
});