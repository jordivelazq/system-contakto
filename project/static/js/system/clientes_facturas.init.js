function investigacionDetail(id) {
    var url = "/clientes/facturas/detail/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-investigaciones").DataTable({
        "serverSide": true,
        "ajax": "/clientes/api/clientes_facturas/?format=datatables",
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
                targets: 7,
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
                targets: 8,
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
           

        ],
        "columns": [
            
            {
                "title": "Ver detalles",
                "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {

                    var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'

                    a += '<a class="btn btn-primary btn-sm btn-rounded" onclick="investigacionDetail(\'' + row.id + '\')">Ver detalles</a>';

                    a += '</div>'
                    return a;
                }
            },
            {
                "title": "#",
                "data": "id",
                "visible": true,
            },
            {
                "title": "Contacto",
                "data": "compania.nombre",
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
                "title": "Enviada",
                "data": "investigacion_factura_completada",
                "responsivePriority": 1,
            },
            {
                "title": "Pagado",
                "data": "investigacion_factura_pago_completado",
                "responsivePriority": 1,
            },
            {
                "title": "Verificado",
                "data": "investigacion_factura_pago_verificado",
                "responsivePriority": 1,
            },
            {
                "title": "Tipo de Investigación",
                "data": "tipo_investigacion",
                "responsivePriority": 2,
            },
            {
                "title": "Resultado",
                "data": "resultado",
                "responsivePriority": 2,
            },
            {
                "title": "Fecha de Registro",
                "data": "fecha_registro",
            },
            {
                "title": "Hora",
                "data": "hora_recibido",
            }

        ],
        "order": [[8, "desc"]],
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