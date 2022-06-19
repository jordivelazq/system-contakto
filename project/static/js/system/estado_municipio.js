/* Project specific Javascript goes here. */
$(document).ready(function() {


  // File type Select after Network selection
    function update_parroquia(_network, _type) {
        var response = $.ajax({
            async: false,
            dataType: "json",
            url: "/clientes/municipios/" + _network
        }).responseText;
        response = JSON.parse(response);
        type = $("#id_municipio");
        type.empty();
        type.append("<option value>---------</option>");
        for (var i = response.length - 1; i >= 0; i--) {
            var new_option = "<option value=\"" + response[i].id + "\">" + response[i].municipio + "</option>";
            type.append(new_option);
        }
        type.val(_type);
    }
    if ($("#id_municipio")) {
        network = $("#id_estado").val();
        if (network) {
            update_parroquia(network, $("#id_municipio").val());
        }
        else {
            type = $("#id_municipio");
            type.empty();
            type.append("<option value>---------</option>");
        }
    }
    $("#id_estado").change(function() {
        update_parroquia($(this).val(), "");
    });

});