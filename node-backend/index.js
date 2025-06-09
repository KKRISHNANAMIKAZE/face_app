const express = require("express");
const cors = require("cors");
const fs = require("fs");
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
const PORT = 5000;
const DB_PATH = path.join(__dirname, "db.json");

app.use(cors());
app.use(bodyParser.json({ limit: "10mb" })); // Supports base64 image data

// Ensure db.json exists
if (!fs.existsSync(DB_PATH)) {
  fs.writeFileSync(DB_PATH, JSON.stringify([]));
}

// Register face
app.post("/register", (req, res) => {
  const { name, imageBase64 } = req.body;

  if (!name || !imageBase64) {
    return res.status(400).json({ error: "Name and image are required" });
  }

  const entry = {
    name,
    imageBase64,
    timestamp: new Date().toISOString(),
  };

  const db = JSON.parse(fs.readFileSync(DB_PATH));
  db.push(entry);
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));

  res.json({ message: "Face registered successfully", entry });
});

// Get all registered faces
app.get("/faces", (req, res) => {
  const db = JSON.parse(fs.readFileSync(DB_PATH));
  res.json(db);
});

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
