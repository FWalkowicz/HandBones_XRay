"use stricts"

let swalNotification = null;

const connectionNotifications = new signalR.HubConnectionBuilder()
    .withUrl("/notifications")
    .build();

connectionNotifications.start()
    .then(() => {
        console.log('SignalR notifications');

    })
    .catch(err =>
        console.error('SignalR-Error: ' + err.toString())
    );

connectionNotifications.on("notify", function (notification) {

    console.log(notification);

    let type;
    if (notification.messageType == 0) {
        type = "info";
    } else if (notification.messageType == 1) {
        type = "success"
    } else if (notification.messageType == 2) {
        type = "error"
    }

    Swal.fire({
        title: 'Error',
        html: `<span id="notify-content">${notification.message}</span>`,
        type: type,
        position: 'top-end',
        toast: true,
        timer: 5000,
        showConfirmButton: !notification.autoHide,

    });

});



