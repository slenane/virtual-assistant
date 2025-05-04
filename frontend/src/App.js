import React, { useEffect, useState } from "react";
import "./tailwind.css";

const App = () => {
  const [input, setInput] = useState("");
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    const initApp = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/init");
        const data = await res.json();
        if (data.response) {
          setGreeting(data.response);
        }
      } catch (error) {
        console.error("Init error:", error);
      }
    };

    initApp();
  }, []);

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
      <h1 className="text-xl font-bold mb-4">{greeting}</h1>
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
