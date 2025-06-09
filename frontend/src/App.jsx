import React, { useState } from "react";
import RegisterFace from "./RegisterFace";
import RecognizeFace from "./Recognise";
import ChatComponent from "./chatbot";

function App() {
  const [view, setView] = useState("register");

  const renderView = () => {
    switch (view) {
      case "register":
        return <RegisterFace />;
      case "recognize":
        return <RecognizeFace />;
      case "chat":
        return <ChatComponent />;
      default:
        return null;
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Face Recognition Platform</h1>
      <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setView("register")}>Register</button>
        <button onClick={() => setView("recognize")}>Recognize</button>
        <button onClick={() => setView("chat")}>Chat</button>
      </div>
      {renderView()}
    </div>
  );
}

export default App;
