import React from "react";

function LiveMonitor() {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Live Face Recognition</h2>
      <img
        src="http://localhost:5002/live-feed"
        alt="Live Feed"
        className="border rounded"
      />
    </div>
  );
}

export default LiveMonitor;
