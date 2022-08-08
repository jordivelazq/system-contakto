document.getElementById("completar-inv-pregunta").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Se completará la investigación",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, completarla!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-success mt-2",
        cancelButtonClass: "btn btn-danger ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Completarda!",
            text: "La solicitud ha sido completada y se ha generado el pago correspondiente",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "La investigación no ha sido completada",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            window.location.href = "/investigaciones/investigaciones/completar/"+investigacion_id+'/';
        }
    })
});