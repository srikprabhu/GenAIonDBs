import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Home, Database, FileText } from "lucide-react";
import express from "express";
import path from "path";

const app = express();
const PORT = 8081;

app.use(express.static(path.join(__dirname, "build")));
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

export default function App() {
  const [activeTab, setActiveTab] = useState("connectors");

  const renderContent = () => {
    switch (activeTab) {
      case "connectors":
        return <p>BigQuery & Cloud SQL Connector UI</p>;
      case "mapping":
        return <p>Data Mapping & Matching UI</p>;
      case "reports":
        return <p>Standard & Custom Reports UI</p>;
      default:
        return <p>Welcome to GCP Data Tools</p>;
    }
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/5 bg-gray-900 text-white p-4 flex flex-col gap-4">
        <Button variant="ghost" onClick={() => setActiveTab("connectors")}>
          <Database className="mr-2" /> Connectors
        </Button>
        <Button variant="ghost" onClick={() => setActiveTab("mapping")}>
          <Home className="mr-2" /> Mapping
        </Button>
        <Button variant="ghost" onClick={() => setActiveTab("reports")}>
          <FileText className="mr-2" /> Reports
        </Button>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        <Card className="p-4">{renderContent()}</Card>
      </div>
    </div>
  );
}
