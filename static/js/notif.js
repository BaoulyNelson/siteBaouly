const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const socket = new WebSocket(
        protocol + window.location.host + "/ws/articles/"
    );

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        alert(data.message);
        // Ici, tu pourrais aussi créer dynamiquement un <div> ou une <li> dans la page
    };

    socket.onclose = function(e) {
        console.error("WebSocket fermé de façon inattendue");
    };