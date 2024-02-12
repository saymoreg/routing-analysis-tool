import { useState } from "react";
import PropTypes from "prop-types";

export const ColoredJsonViewer = ({ jsonData, darkMode }) => {
  const renderJsonValue = (value) => {
    const color = value.includes("TRUE")
      ? darkMode
        ? "#9CCC65" // Light Green in dark mode
        : "#388E3C" // Dark Green in regular mode
      : value.includes("FALSE")
      ? darkMode
        ? "#EF5350" // Light Red in dark mode
        : "#D32F2F" // Dark Red in regular mode
      : darkMode
      ? "#64B5F6" // Light Blue in dark mode
      : "#1976D2"; // Dark Blue in regular mode

    const moddedValue = value.replace(" TRUE", "").replace(" FALSE", "");
    return <span style={{ color }}>{`"${moddedValue}"`}</span>;
  };

  const [collapsedKeys, setCollapsedKeys] = useState([]);

  const toggleCollapse = (key, index) => {
    setCollapsedKeys((prevCollapsedKeys) =>
      prevCollapsedKeys.includes(`${key}_${index}`)
        ? prevCollapsedKeys.filter((k) => k !== `${key}_${index}`)
        : [...prevCollapsedKeys, `${key}_${index}`]
    );
  };

  const isKeyCollapsed = (key, index) =>
    collapsedKeys.includes(`${key}_${index}`);

  const renderJson = (data, level = 1, parentKey = "") => {
    if (typeof data !== "object") {
      return <span>{`"${data}"`}</span>;
    }

    return (
      <div>
        {""}
        {Object.entries(data).map(([key, value], index) => (
          <div key={typeof key === "string" ? key : ""}>
            <span
              onClick={() => toggleCollapse(parentKey || key, index)}
              style={{ cursor: "pointer", marginRight: 5 }}
            >
              {isKeyCollapsed(parentKey || key, index) ? "▶" : "▼"}
            </span>
            {`${"  ".repeat(level)}"${key}": `}
            {isKeyCollapsed(parentKey || key, index) ? (
              <span
                style={{
                  fontStyle: "italic",
                  color: darkMode ? "#777" : "#666",
                }}
              >
                ...
              </span>
            ) : typeof value === "object" ? (
              renderJson(value, level + 1, `${parentKey || key}_${index}`)
            ) : (
              renderJsonValue(value, level + 1)
            )}
          </div>
        ))}
        {""}
      </div>
    );
  };

  return (
    <div
      className="json-viewer"
      style={{ fontFamily: "monospace", whiteSpace: "pre-wrap" }}
    >
      {renderJson(jsonData)}
    </div>
  );
};

ColoredJsonViewer.propTypes = {
  jsonData: PropTypes.any.isRequired,
  darkMode: PropTypes.any,
};
