import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8080;

// Serve the static React build files
app.use(express.static(path.join(__dirname, "build")));

// Catch-all route to serve React index.html
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT} or on Azure App Service`);
});
