import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import WebSocketCall from './components/WebSocketCall';

function App() {
  const [socketInstance, setSocketInstance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState(5);


  useEffect(() => {
    console.log("Effect running");

    const socket = io("http://localhost:5001", {
      transports: ["websocket"],
      cors: {
        origin: "http://localhost:3000",
      },
    });

    setSocketInstance(socket);

    socket.on("connected", () => {
      console.log("Connected to the server");
    });

    setLoading(false);

    socket.on("disconnect", () => {
      console.log("Disconnected from the server");
    });

    socket.on("backend data", (data) => {
      setMessage(data.data);
    });

    return () => {
      console.log("Disconnecting")
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      <h1>App</h1>
      {!loading && message}
    </div>
  );
}

export default App;
