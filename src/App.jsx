import React, { useState } from "react";
import { useBraille } from "./components/useBraille";
import { useBrailleFile } from "./components/useBrailleFile";

const languageTables = {
  "hi-in-g1.utb": "Hindi",
  "ta-in-g1.utb": "Tamil",
  "ml-in-g1.utb": "Malayalam",
  "mr-in-g1.utb": "Marathi",
  "bn-in-g1.utb": "Bengali",
  "gu-in-g1.utb": "Gujarati",
};

const App = () => {
  const [text, setText] = useState("");
  const [lang, setLang] = useState("hi-in-g1.utb");
  const { braille, error } = useBraille(text, lang);
  const { download } = useBrailleFile();

  const handleDownload = () => {
    if (text) download(text, lang);
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        fontFamily: "Segoe UI, sans-serif",
        color: "#000",
        backgroundColor: "#fff",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <header
        style={{
          padding: "20px",
          fontSize: "2rem",
          fontWeight: "bold",
          textAlign: "center",
          borderBottom: "4px solid blue",
        }}
      >
        Bharati Braille Converter
      </header>

      {/* Main Content */}
      <div style={{ display: "flex", flex: 1 }}>
        {/* Input Section */}
        <div
          style={{
            flex: 3,
            padding: "40px",
            backgroundColor: "#f5f5f5",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <textarea
            rows={6}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your text here..."
            style={{
              width: "100%",
              fontSize: "1.1rem",
              padding: "12px",
              borderRadius: "6px",
              background: "#fff",
              color: "#000",
              border: "1px solid #aaa",
              resize: "none",
              marginBottom: "20px",
            }}
          />

          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            style={{
              fontSize: "1rem",
              padding: "10px",
              borderRadius: "6px",
              background: "#fff",
              color: "#000",
              border: "1px solid #aaa",
            }}
          >
            {Object.entries(languageTables).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
        </div>

        {/* Action Section */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            gap: "20px",
            padding: "40px",
            backgroundColor: "#fff",
          }}
        >
          <button
            onClick={handleDownload}
            style={{
              padding: "12px 20px",
              fontSize: "1rem",
              fontWeight: 500,
              border: "none",
              backgroundColor: "#000",
              color: "#fff",
              borderRadius: "6px",
              cursor: "pointer",
              width: "160px",
            }}
          >
            Download PDF
          </button>
        </div>

        {/* Output Section */}
        <div
          style={{
            flex: 3,
            padding: "40px",
            background: "#f5f5f5",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            fontSize: "2rem",
            whiteSpace: "pre-wrap",
            lineHeight: 1.5,
            overflowY: "auto",
          }}
        >
          {error ? (
            <div style={{ color: "red", fontSize: "1rem" }}>{error}</div>
          ) : braille ? (
            braille
          ) : (
            "⠿⠿⠿ Braille output will appear here..."
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
