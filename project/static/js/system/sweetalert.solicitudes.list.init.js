document.getElementById("sa-params").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Se creará una nueva solicitud",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, crearla!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-success mt-2",
        cancelButtonClass: "btn btn-danger ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Creada!",
            text: "La solicitud ha sido creada con éxito",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "La creación de la solicitud ha sido cancelada",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            window.location.href = "/clientes/solicitudes/create/"
        }
    })
});