
function personaUpdate(id) {
    var url = "/personas/update/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {
    $("#datatable-personas").DataTable({
        "serverSide": true,
        "ajax": "/personas/api/personas/?format=datatables",
        "columns": [
            {"data": "id", "title": "Id", "searchable": false},
            {"data": "nombre", "title": "Nombres"},
            {"data": "apellido", "title": "Apellidos"},
            {"data": "nss", "title": "NSS"},
            {"data": "email", "title": "Email"},
            {"data": "edad", "title": "Edad"},
            {"data": "curp", "title": "CURP"},
            {"data": "rfc", "title": "RCF"},
            {"data": "ife", "title": "IFE"},
            {"data": "pasaporte", "title": "Pasaporte"},
            {"data": "smn", "title": "SMN"},
            {"data": "estado_civil", "title": "Estado civil"},
            {"data": "fecha_matrimonio", "title": "Fecha Matrimonio"},
            {"data": "religion", "title": "Religión"},
            {"data": "tiempo_radicando", "title": "Tiempo radicado"},
            {"data": "medio_utilizado", "title": "Medio utilizado"},
            {"data": "fecha_registro", "title": "Fecha registro"},
            {"data": "estatus", "title": "Estado"},
            { "data": null,
            "orderable": false,
            "searchable": false,
            "width": "65px",
            "render": function (data, type, row, meta) {

              var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'
              a += '<a class="btn btn-primary" onclick="personaUpdate(\'' + row.id + '\')"><i class="bx bxs-user-detail font-size-16 align-middle"></i></a>';
           

              a += '</div>'
              return a;
            }
        },
        ],
        lengthChange: !1,
        // buttons: ["copy", "excel", "pdf", "colvis"],
        "initComplete": function (settings, json) {
            $('div.loading-table-data').hide()
          },
    });
});
