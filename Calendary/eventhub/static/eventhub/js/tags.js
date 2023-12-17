var modal = document.getElementById("myModal");
var createTagBtn = document.getElementById("createTagBtn")
var updateTagBtn = document.querySelectorAll(".updateTagBtn")
var deleteTagBtn = document.querySelectorAll(".deleteTagBtn")

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

createTagBtn.onclick = function () {
        loadModal("/eventhub/create_tag/", ".modal-content .close");
}

updateTagBtn.forEach(function(element){
  element.onclick = function() {
    var tagId = element.getAttribute("data-tag-id")
    url = "/eventhub/update_tag/" + tagId + "/"
    loadModal(url, ".modal-content .close")
  }
})

deleteTagBtn.forEach(function(element){
  element.onclick = function() {
    var tagId = element.getAttribute("data-tag-id")
    url = "/eventhub/delete_tag/" + tagId + "/"
    loadModal(url, ".modal-content .close")
  }
})
