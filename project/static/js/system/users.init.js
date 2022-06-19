function userDetail(id) {
    var url = "/core/user/detail/999999999/";
    document.location.href = url.replace('999999999', id);

}

function userUpdate(id) {
    var url = "/core/user/update/999999999/";
    document.location.href = url.replace('999999999', id);
}

function userUpdatePassword(id) {
    var url = "/core/user/password/update/999999999/";
    document.location.href = url.replace('999999999', id);
}


$(document).ready(function () {

    $("#datatable-users").DataTable({
        "serverSide": true,
        "ajax": "/core/api/users/?format=datatables",
        "columns": [
            {"data": "id", "title": "Id", "searchable": false},
            {"data": "first_name", "title": "Nombres"},
            {"data": "last_name", "title": "Apellidos"}, 
            {"data": "email", "title": "Email"},
            {"data": "is_active", "title": "Activo", "searchable": false},
            { "data": null,
                "orderable": false,
                "searchable": false,
                "width": "65px",
                "render": function (data, type, row, meta) {
    
                  var a = '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">'
                  a += '<a class="btn btn-primary" onclick="userDetail(\'' + row.id + '\')"><i class="bx bxs-user-detail font-size-16 align-middle"></i></a>';
                  a += '<a class="btn btn-primary" onclick="userUpdate(\'' + row.id + '\')"><i class="bx bx-edit-alt font-size-16 align-middle"></i></a>';
                  a += '<a class="btn btn-primary" onclick="userUpdatePassword(\'' + row.id + '\')"><i class="bx bx bx-key font-size-16 align-middle"></i></a>';
    
    
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
