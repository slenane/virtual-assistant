import React, { useEffect, useState } from "react";
import "./tailwind.css";
import useGeolocation from "./hooks/useGeolocation";
import WeatherCard from "./components/WeatherCard";
import EventCard from "./components/EventCard";

const App = () => {
  const { latitude, longitude } = useGeolocation();
  const [assistantData, setAssistantData] = useState(null);
  const [input, setInput] = useState("");

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

          const data = await res.json();
          console.log(data);
          setAssistantData(data);
        }
      } catch (error) {
        console.error("Init error:", error);
      }
    };

    initApp();
  }, [latitude, longitude]);

  const sendMessageToBackend = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      console.log("Response from backend:", data);
    } catch (error) {
      console.error("Send message error:", error);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Virtual Assistant</h1>
      {assistantData?.weather && (
        <WeatherCard weather={assistantData?.weather} />
      )}
      <div className="grid gap-4">
        {assistantData?.events.length > 0 && (
          <EventCard events={assistantData?.events} />
        )}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="border px-2 py-1 mr-2"
        placeholder="Type your message"
      />
      <button
        onClick={sendMessageToBackend}
        className="bg-blue-500 text-white px-4 py-1 rounded"
      >
        Submit
      </button>
    </div>
  );
};

export default App;
