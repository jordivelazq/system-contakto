$(document).ready(function () {
    $("#datatable-clientes").DataTable({
        "serverSide": true,
        "ajax": "/clientes/api/clientes/?format=datatables",
        "columns": [
            {"data": "id", "title": "Id", "searchable": false},
            {"data": "first_name", "title": "Nombres"},
            {"data": "last_name", "title": "Apellidos"},
            {"data": "telefono", "title": "Telefono"},
            {"data": "compania.nombre", "title": "Compañia"},
           
        ],
        lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
          },
    });
});
