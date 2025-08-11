import axios from "axios";

export function useBrailleFile() {
  const download = async (text, table = "hi-in-g1.utb") => {
    if (!text) return;

    try {
      const response = await axios.get("http://127.0.0.1:8001/braille/pdf", {
        params: { text, table },
        responseType: "blob", // important for binary file
      });

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "braille_output.pdf";
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("PDF download failed:", error);
    }
  };

  return { download };
}
