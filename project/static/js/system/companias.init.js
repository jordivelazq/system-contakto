$(document).ready(function () {
    $("#datatable-companias").DataTable({
        "serverSide": true,
        "ajax": "/empresa/api/companias/?format=datatables",
        "columns": [
            {"data": "id", "title": "Id", "searchable": false},
            {"data": "nombre", "title": "Comañia"},
            {"data": "telefono", "title": "Telefono"},
            {"data": "es_cliente", "title": "Es cliente", "searchable": false},           
        ],
        lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
          },
    });
});
