document.getElementById("completar-factura-pregunta").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Se enviará la factura al cliente",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, enviarla!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-success mt-2",
        cancelButtonClass: "btn btn-danger ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Completada!",
            text: "La factura se ha enciado correctamente al cliente",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "El proceso ha sido cancelado",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            window.location.href = "/investigaciones/investigaciones/completar_factura/"+investigacion_id+'/';
        }
    })
});