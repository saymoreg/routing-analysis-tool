import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { Box } from "@mui/material";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <App />
    </Box>
  </React.StrictMode>
);
