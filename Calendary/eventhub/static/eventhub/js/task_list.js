document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("myModal");
    var taskslistBtn = document.getElementById("taskslistBtn");
    
    function attachFormSubmitEvent() {
        var form = document.querySelector('form');
        form.onsubmit = function(e) {
          e.preventDefault();
      
          // Aquí puedes hacer la petición AJAX para filtrar los datos
          var stateInputs = document.querySelectorAll('input[name="state"]:checked');
          var tagsInputs = document.querySelectorAll('input[name="tags"]:checked');
          var dateRangeInput = document.querySelector('select[name="date_range"]');
      
          var state = Array.from(stateInputs).map(input => input.value);
          var tags = Array.from(tagsInputs).map(input => input.value);
          var date_range = dateRangeInput ? dateRangeInput.value : null;
      
          var data = {
            state: state,
            tags: tags,
            date_range: date_range
          };
      
          $.ajax({
            url: '/eventhub/tasks/',
            type: 'GET',
            data: $.param(data, true),  // Serializar los datos del formulario
            success: function(data) {
              // Actualizar la vista con los datos filtrados
              $(".modal-content").html(data);
      
              // Adjuntar el evento onsubmit al nuevo formulario
              attachFormSubmitEvent();
            },
            error: function() {
              console.log("Error al filtrar los datos");
            }
          });
        };
      }
      
      function loadModal(view, closeBtnSelector) {
        $.ajax({
          url: view,
          type: "GET",
          success: function(data) {
            $(".modal-content").html(data);
            modal.style.display = "block";
      
            // Agregar el evento onclick al span de cierre dentro del contenido cargado
            var closeBtn = document.querySelector(closeBtnSelector);
            if (closeBtn) {
              closeBtn.onclick = function() {
                modal.style.display = "none";
              };
            }
      
            // Adjuntar el evento onsubmit al formulario
            attachFormSubmitEvent();
          },
          error: function() {
            console.log("Error al cargar la vista");
          }
        });
      }
      
      taskslistBtn.onclick = function (){
        loadModal("/eventhub/tasks/", ".modal-content .close")
      }
});