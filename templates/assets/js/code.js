let canSendMessage = true;

function updateTimer(seconds) {
    const timerElement = document.getElementById("timer");
    timerElement.innerText = seconds + " секунд";
}

function sendMessage() {
    if (canSendMessage) {
        const messageInput = document.getElementById("message");
        const message = messageInput.value;
        if (message) {
            fetch('/add', {
                method: 'POST',
                body: new URLSearchParams({ message: message }),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Перезагрузить страницу после успешной отправки
                    window.location.reload();
                } else {
                    // Перенаправить на страницу "stop.html" при неудачной отправке
                    window.location.href = "/stop.html";
                }
            });
        }
    }
}