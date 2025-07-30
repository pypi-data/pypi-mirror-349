import React from "react";
import { createRoot } from "react-dom/client";
import Sidebar from "./components/Sidebar";
import ChatPage from "./components/ChatPage";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar title="輿論雷達站" apiUrl={apiUrl} />
      <div style={{ flex: 1 }}>
        <ChatPage apiUrl={apiUrl} />
      </div>
    </div>
  );
}

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
