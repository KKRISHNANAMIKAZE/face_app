import React, { useState, useEffect, useRef } from "react";

function AskBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:5003/ws");

    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, { type: "bot", text: event.data }]);
    };

    ws.current.onopen = () => {
      setMessages((prev) => [...prev, { type: "bot", text: "🤖 Hello! Ask me about face registrations." }]);
    };

    return () => ws.current.close();
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      setMessages((prev) => [...prev, { type: "user", text: input }]);
      ws.current.send(input);
      setInput("");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">AskBot (Chat with RAG)</h2>
      <div className="h-64 overflow-y-auto border p-2 mb-2">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-1 ${msg.type === "user" ? "text-right" : "text-left"}`}>
            <span className="px-2 py-1 bg-gray-200 rounded">{msg.text}</span>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        placeholder="Ask something..."
        onChange={(e) => setInput(e.target.value)}
        className="border p-2 mr-2"
      />
      <button onClick={sendMessage} className="bg-blue-500 text-white px-4 py-1 rounded">
        Send
      </button>
    </div>
  );
}

export default AskBot;
