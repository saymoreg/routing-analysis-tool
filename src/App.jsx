import { Box, ThemeProvider, createTheme } from "@mui/material";
import Footer from "./Footer";
import Header from "./Header";
import { useState } from "react";
import RequestForm from "./RequestForm";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const paletteType = darkMode ? "dark" : "light";
  const theme = createTheme({
    palette: {
      primary: {
        main: "#D2D600",
      },
      secondary: {
        main: "#1b5e20",
      },
      mode: paletteType,
      background: {
        default: paletteType === "light" ? "#eaeaea" : "#121212",
      },
    },
  });

  function handThemeChange() {
    setDarkMode(!darkMode);
  }

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}
      >
        <Header darkMode={darkMode} handleThemeChange={handThemeChange} />
        <RequestForm darkMode={darkMode} />
        <Footer />
      </Box>
    </ThemeProvider>
  );
}
