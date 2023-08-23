document.getElementById("enviar-solicitud").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Desea enviar la solicitud",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, enviarla!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-success mt-2",
        cancelButtonClass: "btn btn-danger ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Creada!",
            text: "La solicitud ha sido enviada con éxito",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "El envío de la solicitud ha sido cancelado",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            let pk = document.getElementById("cliente_solicitud_id").value
            window.location.href = "/clientes/solicitudes/enviar/"+ pk +"/"
        }
    })
});