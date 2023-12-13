var modal = document.getElementById("myModal");

function submitFormAndCloseModal(formId, event) {
  event.preventDefault();  // Evitar la presentación predeterminada del formulario
  
  // Realizar la solicitud AJAX
  $.ajax({
    url: $("#" + formId).attr("action"),
    type: $("#" + formId).attr("method"),
    data: $("#" + formId).serialize(),
    success: function(data) {
      // Cerrar el modal y mostrar un mensaje al usuario
      $(".modal-content").html("<p>" + data.message + "</p>");
      setTimeout(function() {
        modal.style.display = "none";
      }, 2000); 
    },
    error: function() {
      console.log("Error al enviar el formulario");
    }
  });
}
