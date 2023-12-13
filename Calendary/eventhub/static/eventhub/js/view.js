document.addEventListener("DOMContentLoaded", function() {
    var calendarViewBtn = document.getElementById("calendar-view")
    var calendarContainer = document.querySelector(".calendar-container")

    function changeViewContent(view, elementToModify) {
        $.ajax({
          url: view,
          type: "GET",
          success: function(data) {
            $(elementToModify).html(data);
            
          },
          error: function() {
            console.log("Error al cargar la vista");
          }
        });
      }

    

    

});