import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const askQuestion = async () => {
    try {
      const res = await axios.post("http://localhost:5000/chat", { query });
      setResponse(res.data.response);
    } catch (err) {
      setResponse("Failed to connect to backend.");
    }
  };

  return (
    <div>
      <h2>Chat with Memory</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask something..." />
      <button onClick={askQuestion}>Ask</button>
      <p><strong>Answer:</strong> {response}</p>
    </div>
  );
}

export default Chat;
