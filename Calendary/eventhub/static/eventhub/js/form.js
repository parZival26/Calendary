var modal = document.getElementById("myModal");

function submitFormAndCloseModal(formId, event) {
  event.preventDefault();  // Evitar la presentación predeterminada del formulario

  // Realizar la solicitud AJAX
  $.ajax({
    url: $("#" + formId).attr("action"),
    type: $("#" + formId).attr("method"),
    data: $("#" + formId).serialize(),
    success: function (data) {
      // Cerrar el modal y mostrar un mensaje al usuario
      $(".modal-content").html("<p>" + data.message + "</p>");
      setTimeout(function () {
        modal.style.display = "none";
      }, 2000);
    },
    error: function () {
      console.log("Error al enviar el formulario");
    }
  });
}

$(document).ready(function () {
  // Attach a submit handler to the form
  $('#id_color').submit(function () {
    // Get the color value in RGB format
    var rgbColor = $('#id_color').val();

    // Convert RGB to hex
    var hexColor = rgbToHex(rgbColor);

    // Set the hex color back to the form field
    $('#id_color').val(hexColor);
  });

  // Function to convert RGB to hex
  function rgbToHex(rgb) {
    var hex = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    return "#" + ("0" + parseInt(hex[1], 10).toString(16)).slice(-2) +
      ("0" + parseInt(hex[2], 10).toString(16)).slice(-2) +
      ("0" + parseInt(hex[3], 10).toString(16)).slice(-2);
  }
});
