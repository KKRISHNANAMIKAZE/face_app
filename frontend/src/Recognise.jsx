import React, { useRef, useEffect, useState } from "react";
import axios from "axios";

function Recognize() {
  const videoRef = useRef();
  const canvasRef = useRef();
  const [recognizedNames, setRecognizedNames] = useState([]);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;

    setInterval(async () => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);

      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob);

        const res = await axios.post("http://localhost:5000/recognize", formData);
        const names = res.data.faces.map(f => f.name);
        setRecognizedNames(names);
      }, "image/jpeg");
    }, 3000); // every 3 sec
  };

  return (
    <div>
      <h2>Face Recognition</h2>
      <video ref={videoRef} autoPlay />
      <canvas ref={canvasRef} style={{ display: "none" }}></canvas>
      <button onClick={startCamera}>Start Recognition</button>
      <div>
        {recognizedNames.map((name, index) => (
          <p key={index}>Detected: {name}</p>
        ))}
      </div>
    </div>
  );
}

export default Recognize;
