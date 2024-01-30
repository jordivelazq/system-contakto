function investigacionDetail(id) {
    var url = "/investigaciones/investigaciones/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $.fn.dataTable.moment( 'DD/MM/YYYY' );
    $.fn.dataTable.moment( 'HH:mm' );

    $("#datatable-investigaciones").DataTable({
        serverSide: false,
        ajax: {
            url : "/clientes/api/candidatos_empresa/",
            dataSrc: "results",
        },
        language: {
            "url": "/static/libs/datatables.net/lang/es-ES.json"
        },
        pageLength: 100,
        lengthMenu: [
            [25, 50, 100, -1],
            [25, 50, 100, "Todos"]
        ],
        columnDefs: [
            {
                targets: 7,
                className: 'dt-body-center',
                render: function (data, type, row) {
                    if (data == true) {
                        return '<i class="fa fa-check"></i>';
                    } else {
                        return '<i class="fa fa-times"></i>';
                    }
                },
            },
            {
                targets: 6,
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
                targets: [1],
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
                title: "Tipo de Investigación",
                data: 'tipo_investigacion',
                searchable: false,
                responsivePriority: 2,
                render: function (data, type, row, meta) {
                    if (row.tipo_investigacion != undefined)
                        return row.tipo_investigacion;
                    return 'N/A';
                }
            },
            {
                title: "Resultado",
                data: "resultado_des",
                responsivePriority: 2,
                searchable: false,
            },
            /*{
                "title": "Estatus",
                data: "status",
                responsivePriority: 2,
            },*/
            {
                title: "Datos verificados",
                data: "candidato.datos_validados",
            },
            {
                "title": "Asignado",
                "data": "agente",
                "render": function (data, type, row, meta) {
                    if (row.agente_name != undefined && row.agente_name != 'No asignado')
                        return '<i class="fa fa-check text-success"></i>';
                    return '<i class="fa fa-times text-danger"></i>';
                }
            },
            {
                "title": "Fecha de asignación",
                "data": "fecha_asignacion",
                "render": function (data, type, row, meta) {
                    if (moment(data).isValid()){
                        return moment(data).format('DD/MM/YYYY HH:mm');
                    }
                    return "Pendiente";
                }
            },
            {
                "title": "Cita",
                "data": "cita",
                "defaultContent": "No asignado",
            },
            {
                "title": "Documento",
                "data": "tipo_investigacion",
                searchable: false,
                responsivePriority: 2,
                render: function (data, type, row, meta) {
                    /**
                     *  Laboral
                     *  Psicométrico
                     *  Socioeconómico
                     *  Validación de demandas
                     *  Visita domiciliaria
                     */

                    if (row.tipo_investigacion != undefined) {
                        if (row.tipo_investigacion === 'Laboral' && row.laboral_completado)
                                return `<a href="/personas/investigacion/exportar/reporte-laboral/${row.id}" target="_blank" class="btn btn-primary"><i class="fa fa-file-pdf"></i> ${row.tipo_investigacion}</a>`;
                            else if (row.tipo_investigacion === 'Socioeconómico'){
                                if (row.laboral_completado && row.entrevista_from_completado){
                                    return `<a href="/personas/investigacion/exportar/reporte-socioeconomico/${row.id}" target="_blank" class="btn btn-primary"><i class="fa fa-file-pdf"></i> ${row.tipo_investigacion}</a>`;
                                }else if (row.laboral_completado){
                                    return `<a href="/personas/investigacion/exportar/reporte-laboral/${row.id}" target="_blank" class="btn btn-primary"><i class="fa fa-file-pdf"></i>Laboral</a>`;
                                }else{
                                    return 'En proceso'
                                }
                            }else if (row.tipo_investigacion === 'Validación de demandas' && row.laboral_completado)
                                return `<a href="/personas/investigacion/exportar/reporte-demandas/${row.id}" target="_blank" class="btn btn-primary"><i class="fa fa-file-pdf"></i> ${row.tipo_investigacion}</a>`;
                            else if (row.tipo_investigacion === 'Visita domiciliaria' && row.entrevista_from_completado)
                                return `<a href="/personas/investigacion/exportar/reporte-visita-domiciliaria/${row.id}" target="_blank" class="btn btn-primary"><i class="fa fa-file-pdf"></i> ${row.tipo_investigacion}</a>`;
                            else
                                return 'En proceso';
                    }
                    return 'No terminada';
                }
            },
            {
                "title": "Empresas y demandas",
                "data": "candidato.id",
                searchable: false,
                render: function (data, type, row, meta) {

                    if (row.candidato.id != undefined) {
                        return `<a href="/investigaciones/investigaciones/cliente/detail/${row.id}" target="_blank" data-id="${row.candidato.id}" class="btn btn-secondary btn-demandas"><i class="fa fa-link"></i></a>`;
                    }
                    return 'Sin información';
                }
            }

        ],
        "order": [[1, "desc"],[2,"desc"]],
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

    /*$(document).on("click",".btn-demandas",function(event){
        event.preventDefault();
        var id = $(this).data("id");
        alert("clicked "+id );
    })*/
});