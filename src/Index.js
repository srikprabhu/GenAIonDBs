import React, { useState } from "react";
import { Button } from "./Button"; // Adjust based on the file structure

export default function index() {
  const [selected, setSelected] = useState(null);

  const handleClick = (section) => {
    setSelected(section);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/5 bg-gray-800 text-white p-4 space-y-4">
        <Button onClick={() => handleClick("Connectors")}>Connectors</Button>
        <Button onClick={() => handleClick("Mapping/Matching")}>Mapping/Matching</Button>
        <Button onClick={() => handleClick("Report Repo")}>Report Repo</Button>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        {selected === "Connectors" && <h1>Connectors to GCP BigQuery/Cloud SQL</h1>}
        {selected === "Mapping/Matching" && <h1>Mapping/Matching Feature</h1>}
        {selected === "Report Repo" && <h1>Standard/Custom Reports</h1>}
      </div>
    </div>
  );
}
