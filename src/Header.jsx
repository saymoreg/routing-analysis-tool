import {
  Box,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Switch,
} from "@mui/material";
import CodeIcon from "@mui/icons-material/Code";
import PropTypes from "prop-types";
import { DarkMode, WbSunny } from "@mui/icons-material";

export default function Header({ darkMode, handleThemeChange }) {
  return (
    <AppBar position="static">
      <CssBaseline />
      <Toolbar
        sx={{
          pr: "24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            sx={{ flexGrow: 1, mr: "5px", ml: "10px" }}
          >
            Routing Analysis
          </Typography>
          <CodeIcon fontSize="medium" sx={{ pl: "5px" }} />
        </Box>
        <Box display="flex" alignItems="center" justifySelf="flex-end">
          <WbSunny />
          <Switch checked={darkMode} onChange={handleThemeChange} />
          <DarkMode />
        </Box>
      </Toolbar>
    </AppBar>
  );
}

Header.propTypes = {
  darkMode: PropTypes.any,
  handleThemeChange: PropTypes.any,
};
