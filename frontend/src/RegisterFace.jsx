import React, { useState, useRef } from "react";
import axios from "axios";

function RegisterFace() {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  };

  const captureAndSend = async () => {
    if (!name) {
      setMessage("Please enter a name first.");
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("file", blob);

      try {
        const res = await axios.post("http://localhost:5000/register-face", formData);
        setMessage(res.data.message);
      } catch (err) {
        setMessage("Registration failed.");
      }
    }, "image/jpeg");
  };

  return (
    <div>
      <h2>Register Face</h2>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter name" />
      <button onClick={startCamera}>Start Camera</button>
      <video ref={videoRef} autoPlay playsInline />
      <canvas ref={canvasRef} style={{ display: "none" }}></canvas>
      <button onClick={captureAndSend}>Register Face</button>
      <p>{message}</p>
    </div>
  );
}

export default RegisterFace;
