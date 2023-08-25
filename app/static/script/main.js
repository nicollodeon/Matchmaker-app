document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    console.log(recipientUsername);
    console.log(socket.connected);
    let controlPanelTimeout;

    function startControlPanelTimer() {
        clearTimeout(controlPanelTimeout);
        controlPanelTimeout = setTimeout(() => {
            document.getElementById('control-panel').style.display = 'block';
            $(".chat-box").slideToggle("slow");
        }, 60000);  // 300000 milliseconds = 5 minutes
    }

    startControlPanelTimer();

    socket.on('connect', () => {
        console.log("Joining room", {recipient_username: recipientUsername});
        socket.emit('join_room', {recipient_username: recipientUsername});
    });

    socket.on('message', (data) => {
        console.log("Received message:", data);
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.sender_username}: ${data.message}`;
        messageElement.className = "client-chat";
        document.querySelector('#messages').append(messageElement);
    });

    document.querySelector('#send-message').onclick = () => {
        const message = document.querySelector('#message-input').value;
        if (message) {
            console.log("Sending message:", message);
            console.log({recipient_username: recipientUsername, message: message});
            socket.emit('send_message', {recipient_username: recipientUsername, message: message});
            const messageElement = document.createElement('div');
            messageElement.textContent = `${message}`;
            messageElement.className = "user-chat";
            document.querySelector('#messages').append(messageElement);
            document.querySelector('#message-input').value = '';
        }
    };

    document.querySelector('#message-input').onkeypress = (e) => {
        if (e.key === 'Enter') {
            console.log("Enter key pressed");
            document.querySelector('#send-message').click();
        }
    };
    document.getElementById('btn-cancel').onclick = () => {
        socket.emit('end_chat', { action: 'cancel', recipient_username: recipientUsername });
        document.getElementById('control-panel').style.display = 'none';
    };
    
    document.getElementById('btn-match').onclick = () => {
        socket.emit('end_chat', { action: 'match', recipient_username: recipientUsername });
        document.getElementById('control-panel').style.display = 'none';
    };
    
    document.getElementById('btn-extend').onclick = () => {
        socket.emit('end_chat', { action: 'extend', recipient_username: recipientUsername });
        document.getElementById('control-panel').style.display = 'none';
    };

    socket.on('chat_decision', (data) => {
        if (data.action == 'end') {
            window.location.href = `/index/${currentUsername}`;  // Go back to the home page
        } else if (data.action == 'match') {
            connected_user = recipientUsername;
            window.location.href = `/index/${recipientUsername}`;  // TODO other person's profile
        } else {
            document.getElementById('control-panel').style.display = 'none';  // Hide the control panel
            $(".chat-box").slideToggle("slow")
            startControlPanelTimer();
        }
    });    
});

$(document).ready(()=>{
    $(".match-btn").click(()=>{
        $(".chat-box").slideToggle("slow")
    })
})
