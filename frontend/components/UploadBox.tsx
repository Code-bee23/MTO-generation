"use client";

import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function UploadBox() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const [ocrText, setOcrText] = useState("");
  const [aiData, setAiData] = useState<any>(null);
  const [mto, setMto] = useState<any[]>([]);

  async function uploadFile() {
    if (!selectedFile) {
      alert("Please select a drawing.");
      return;
    }

    setLoading(true);
    setStatus("Processing Drawing...");

    setOcrText("");
    setAiData(null);
    setMto([]);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log("Backend Response:", data);

      if (data.status !== "success") {
        setStatus(data.message || "Backend Error");
        setLoading(false);
        return;
      }

      setStatus("MTO Generated Successfully");

      setOcrText(data.ocr_text ?? "");

      setAiData(data.ai_data ?? {});

      setMto(Array.isArray(data.mto) ? data.mto : []);

    } catch (error) {
      console.error(error);

      setStatus("Cannot connect to backend.");
    }

    setLoading(false);
  }

  return (
    <div className="upload-card">

      <input
        type="file"
        accept=".pdf,.png,.jpg,.jpeg"
        onChange={(e) => {
          if (e.target.files) {
            setSelectedFile(e.target.files[0]);
          }
        }}
      />

      <br /><br />

      <button onClick={uploadFile}>
        Generate MTO
      </button>

      <br /><br />

      {loading && <h3>Processing Drawing...</h3>}

      <h3>{status}</h3>

      {ocrText && (
        <>
          <h2>OCR Text</h2>

          <textarea
            rows={10}
            value={ocrText}
            readOnly
            style={{
              width: "100%"
            }}
          />
        </>
      )}

      {aiData && (
        <>
          <h2>AI Data</h2>

          <pre>{JSON.stringify(aiData, null, 2)}</pre>
        </>
      )}

      {mto.length > 0 && (
        <>
          <h2>Material Take-Off</h2>

          <table className="mto-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Description</th>
                <th>Size</th>
                <th>Quantity</th>
              </tr>
            </thead>

            <tbody>
              {mto.map((item, index) => (
                <tr key={index}>
                  <td>{item.Item}</td>
                  <td>{item.Description}</td>
                  <td>{item.Size}</td>
                  <td>{item.Quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <br />

          <button
            onClick={() =>
              window.open(`${API_URL}/download`, "_blank")
            }
          >
            Download Excel
          </button>
        </>
      )}
    </div>
  );
}