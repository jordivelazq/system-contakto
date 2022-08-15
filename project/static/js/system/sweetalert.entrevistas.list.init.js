document.getElementById("completar-inv-entrevista-pregunta").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "Se completará la entrevista",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, completarla!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-success mt-2",
        cancelButtonClass: "btn btn-danger ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Completada!",
            text: "La entrevita ha sido completada con éxito",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "El proceso ha sido cancelado",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            window.location.href = "/investigaciones/investigaciones/completar_entrevista/"+investigacion_id+'/';
        }
    })
});