var modal = document.getElementById("myModal");
var deleteTaskBtn = document.querySelectorAll(".deleteTaskBtn")
var uptdateTaskBtn = document.querySelectorAll(".updateTaskBtn")


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
          },
          error: function() {
            console.log("Error al cargar la vista");
          }
        });
}

deleteTaskBtn.forEach(function(element){
  element.onclick = function() {
    var taskId = element.getAttribute("data-task-id")
    url = "/eventhub/delete_task/" + taskId +"/"
    loadModal(url, ".modal-content .close") 
  }
})

uptdateTaskBtn.forEach(function(element) {
  element.onclick = function () {
    var taskId = element.getAttribute("data-task-id")
    url = "/eventhub/uptate_task/" + taskId + "/"
    loadModal(url, ".modal-content .close")
  }
})