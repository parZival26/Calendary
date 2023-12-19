document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("myModal");
  var taskslistBtn = document.getElementById("taskslistBtn");

  function attachFormSubmitEvent() {
    if (!$('form').data('eventAttached')) {
      $(document).on('submit', 'form', function (e) {
        e.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
          url: '/eventhub/tasks/',
          type: 'GET',
          data: formData,
          success: function (data) {
            $(".modal-content").html(data);
          },
          error: function () {
            console.log("Error al filtrar los datos");
          }
        });
      }).data('eventAttached', true);
    }
  }

  function loadModal(view, closeBtnSelector) {
    $.ajax({
      url: view,
      type: "GET",
      success: function (data) {
        $(".modal-content").html(data);
        modal.style.display = "block";

        var closeBtn = document.querySelector(closeBtnSelector);
        if (closeBtn) {
          closeBtn.onclick = function () {
            modal.style.display = "none";
          };
        }

        attachFormSubmitEvent();
        attachPaginationClickEvent();
      },
      error: function () {
        console.log("Error al cargar la vista");
      }
    });
  }

  function attachPaginationClickEvent() {
    if (!$(document).data('paginationEventAttached')) {
      $(document).on('click', '.pagination-link', function (event) {
        event.preventDefault();
        var url = $(this).attr('href');

        // Obtener parámetros de filtro del formulario
        var formData = $('form').serialize();

        // Agregar parámetros de filtro a la URL de paginación
        if (url.indexOf('?') !== -1) {
          url += '&' + formData;
        } else {
          url += '?' + formData;
        }

        loadModal(url, ".modal-content .close");
      }).data('paginationEventAttached', true);
    }
  }

  taskslistBtn.onclick = function () {
    loadModal("/eventhub/tasks/", ".modal-content .close");
  }
});