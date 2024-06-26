import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';
import PitchRungs from "./components/PitchRungs";

const Dashboard = () => {
  const [socketData, setSocketData] = useState("");
  const [socketStatus, setSocketStatus] = useState("Off");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const sensorEndpoint = "http://localhost:5001";
    const socketInstance = io.connect(sensorEndpoint, {
      reconnection: true,
      // transports: ['websocket']
    });
    
    console.log("component mounted");

    socketInstance.on("responseMessage", (message) => {
      setSocketData(message.pitch);
      console.log("responseMessage", message);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.close();
      console.log("component unmounted");
    };
  }, []);

  const handleEmit = () => {
    if (socketStatus === "On") {
      socket.emit("message", { data: 'Stop Sending', status: 'Off' });
      setSocketStatus("Off");
    } else {
      socket.emit("message", { data: 'Start Sending', status: 'On' });
      setSocketStatus("On");
    }
    console.log("Emit Clicked");
  };

  return (
    <div>
        <React.Fragment>
            <div>Data: {socketData}</div>
            <div>Status: {socketStatus}</div>
            <div onClick={handleEmit}> Start/Stop</div>
        </React.Fragment>
        <PitchRungs />
    </div>
    
  );
};

export default Dashboard;
