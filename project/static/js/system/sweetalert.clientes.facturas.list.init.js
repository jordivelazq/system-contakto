document.getElementById("enviar-comprobante-pregunta").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Se enviará el comprobante a cobranzas",
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
            text: "La comprobante se ha enviado correctamente al cliente",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "El proceso ha sido cancelado",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            window.location.href = "/investigaciones/investigaciones/completar_comprobante_factura/"+investigacion_id+'/';
        }
    })
});