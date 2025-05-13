import React, { useEffect, useState } from "react";
import "./tailwind.css";
import useGeolocation from "./hooks/useGeolocation";
import WeatherCard from "./components/WeatherCard";
import EventCard from "./components/EventCard";
import ChatCard from "./components/ChatCard";

const App = () => {
  const { latitude, longitude } = useGeolocation();
  const [assistantData, setAssistantData] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);

  const getTimestamp = () => {
    const now = new Date();
    return [
      String(now.getHours()).padStart(2, "0"),
      String(now.getMinutes()).padStart(2, "0"),
      String(now.getSeconds()).padStart(2, "0"),
    ].join(":");
  };

  useEffect(() => {
    const initApp = async () => {
      try {
        if (latitude && longitude) {
          const res = await fetch("http://localhost:5000/api/init", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ latitude, longitude }),
          });

          const { chat, ...data } = await res.json();

          setChatHistory([
            {
              timestamp: "Chat started",
              role: "assistant",
              message: "Hello! I'm your assistant. How can I help you today?",
            },
            ...chat,
          ]);
          setAssistantData(data);
        }
      } catch (error) {
        console.error("Init error:", error);
      }
    };

    initApp();
  }, [latitude, longitude]);

  const SendMessageToBackend = async (message) => {
    setChatHistory((prev) => [
      ...prev,
      {
        timestamp: getTimestamp(),
        role: "you",
        message: message,
      },
    ]);

    try {
      const res = await fetch("http://localhost:5000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });
      const response = await res.json();
      // Append the new response to chatHistory
      setChatHistory((prev) => [...prev, response]);
    } catch (error) {
      console.error("Send message error:", error);
    }
  };

  return (
    <div className="grid grid-cols-[1fr_3fr] gap-4 p-4">
      <div className="side-panel">
        {assistantData?.weather && (
          <WeatherCard weather={assistantData?.weather} />
        )}
        {assistantData?.events && <EventCard events={assistantData?.events} />}
      </div>
      <div className="main-content">
        <ChatCard
          chat={chatHistory}
          onSendMessage={SendMessageToBackend}
        ></ChatCard>
      </div>
    </div>
  );
};

export default App;
