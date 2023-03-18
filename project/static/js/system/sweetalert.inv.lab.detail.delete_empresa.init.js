
function confirmation(ev) {
    ev.preventDefault();
    var urlToRedirect = ev.currentTarget.getAttribute('href'); //use currentTarget because the click may be on the nested i tag and not a tag causing the href to be empty
    console.log(urlToRedirect); // verify if this is the right URL

    Swal.fire({
        title: "¿Estás seguro(a)?",
        text: "¿Estás seguro(a) de que deseas eliminar esta empresa?",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Si, Eliminar!",
        cancelButtonText: "No, cancelar!",
        confirmButtonClass: "btn btn-danger mt-2",
        cancelButtonClass: "btn btn-success ms-2 mt-2",
        buttonsStyling: !1
    }).then(function (e) {
        e.value ? Swal.fire({
            title: "Completarda!",
            text: "El proceso para completar la investigación laboral ha sido completado",
            icon: "success",
            confirmButtonColor: "#1c84ee"
        }) : e.dismiss === Swal.DismissReason.cancel && Swal.fire({
            title: "Cancelada",
            text: "El proceso para completar la investigación laboral ha sido cancelado",
            icon: "error",
            confirmButtonColor: "#1c84ee"
        })

        if (e.value) {
            // window.location.href = "/investigaciones/investigaciones/completar_inv_laboral/"+investigacion_id+'/';
            window.location.href = urlToRedirect;
        }
    })
}
