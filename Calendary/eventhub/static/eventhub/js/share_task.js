var copyButtons = document.querySelectorAll('.shareTaskWithUserBtn');

copyButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
        event.preventDefault();

        var taskId = button.getAttribute('data-task-id');
        var taskLink = window.location.origin + button.getAttribute('data-link');

        console.log('Button clicked, taskId: ' + taskId + ', taskLink: ' + taskLink);

        var tempInput = document.createElement('input');
        tempInput.style = 'position: absolute; left: -1000px; top: -1000px';
        tempInput.value = taskLink;
        document.body.appendChild(tempInput);
        tempInput.select();

        // Copia el texto al portapapeles
        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Copying text command was ' + msg);
            alert('Enlace copiado al portapapeles para la tarea con ID ' + taskId);
        } catch (err) {
            console.error('Could not copy text: ', err);
        }

        // Elimina el elemento de entrada temporal
        document.body.removeChild(tempInput);
    });
});
