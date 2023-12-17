var modal = document.getElementById("myModal");
var deleteTaskBtn = document.querySelectorAll(".deleteTaskBtn")
var uptdateTaskBtn = document.querySelectorAll(".updateTaskBtn")
var shareTaskBtn = document.querySelectorAll(".shareTaskBtn")


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

            var copyLinkBtn = document.querySelector(".copyLinkBtn");
            if (copyLinkBtn) {
              copyLinkBtn.onclick = function() {
                var taskLink = this.getAttribute("data-link");
                navigator.clipboard.writeText(taskLink).then(function() {
                  console.log('Copying to clipboard was successful!');
                }, function(err) {
                  console.error('Could not copy text: ', err);
                });
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
    url = "/eventhub/update_task/" + taskId + "/"
    loadModal(url, ".modal-content .close")
  }
})

shareTaskBtn.forEach(function(element){
  element.onclick=function() {
    var taskId = element.getAttribute("data-task-id")
    url = "/eventhub/task/" + taskId + "/share/"
    loadModal(url, ".modal-content .close")
  }
})