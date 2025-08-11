import { useState, useEffect } from "react";
import axios from "axios";

export function useBraille(text, table = "hi-in-g1.utb") {
  const [braille, setBraille] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!text) return;

    const fetchBraille = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/braille", {
          params: { text, table },
        });
        setBraille(res.data.braille);
        setError(null);
      } catch (err) {
        setError(err.message || "Error fetching Braille");
        setBraille(null);
      }
    };

    fetchBraille();
  }, [text, table]);

  return { braille, error };
}
