document.addEventListener("DOMContentLoaded", function() {
  var modal = document.getElementById("myModal");
  var createTaskBtn = document.getElementById("createTaskBtn");
  var listTasksBtn = document.querySelectorAll(".listTasksBtn");
  var listTagsBtn = document.getElementById("listTagsBtn");


  // let viewState = 0;
  // const calendarContainer = document.querySelector('.calendar-container');
  // const originalContent = calendarContainer.innerHTML;

  // document.getElementById('calendar-view').addEventListener('click', function() {
  //   viewState = (viewState + 1) % 3;
  
  //   if (viewState === 1) {
  //     // Show weeks
  //     calendarContainer.innerHTML = '';
  //     document.querySelectorAll('.week').forEach(function(week) {
  //       calendarContainer.appendChild(week.cloneNode(true));
  //     });
  //   } else if (viewState === 2) {
  //     // Show months
  //     calendarContainer.innerHTML = '';
  //     document.querySelectorAll('.month').forEach(function(month) {
  //       calendarContainer.appendChild(month.cloneNode(true));
  //     });
  //   } else {
  //     // Show days
  //     calendarContainer.innerHTML = originalContent;
  //   }
  // });


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

  createTaskBtn.onclick = function() {
    loadModal("/eventhub/create_task/", ".modal-content .close");
  };

  listTasksBtn.forEach(function(element) {
    element.onclick = function(){
        var year = element.getAttribute('data-year');
        var month = element.getAttribute('data-month');
        var day = element.getAttribute('data-day');

        var url = "/eventhub/list_tasks/" + year + "/" + month + "/" + day

        loadModal(url, ".modal-content .close");
    }
  });

  listTagsBtn.onclick = function() {
    loadModal("/eventhub/list_tags/", ".modal-content .close")
  }
  
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
});
