var copyButtons = document.querySelectorAll('.shareTaskWithUserBtn');

copyButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
        event.preventDefault();

        var taskId = button.getAttribute('data-task-id');
        var taskLink = window.location.origin + button.getAttribute('data-link');

        console.log('Button clicked, taskId: ' + taskId + ', taskLink: ' + taskLink);

        // Copia el enlace al portapapeles
        navigator.clipboard.writeText(taskLink).then(function() {
            console.log('Copying to clipboard was successful!');
        }, function(err) {
            console.error('Could not copy text: ', err);
        });
    });
});
