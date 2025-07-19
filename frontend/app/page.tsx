"use client";
import { useState } from "react";

export default function Home() {
  const [date, setDate] = useState("");
  const [status, setStatus] = useState("");
  const [files, setFiles] = useState<string[]>([]);

  const handleFetch = async () => {
    if (!date) {
      setStatus("Please select a date.");
      return;
    }
    setStatus("Fetching data...");
    setFiles([]);
    try {
      // const res = await fetch("http://localhost:5000/api/fetch-data", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ date }),
      // });

      const res = await fetch("https://rites-api.onrender.com/api/fetch-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date }),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch data from server");
      }

      const data = await res.json();
      console.log("Backend response:", data);
      if (data.success) {
        setStatus(data.message);
        setFiles(data.files_created || []);
      } else {
        setStatus(data.error || "Failed to fetch data");
      }
    } catch (err: any) {
      console.error("Error fetching data:", err);
      setStatus("Request failed: " + err.message);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 p-4">
      <div className="bg-white rounded-2xl shadow-xl px-8 py-10 max-w-md w-full border border-gray-200">
        <h1 className="text-2xl font-bold text-purple-700 mb-6 text-center">
          Data Fetcher <span className="text-gray-500 text-lg font-medium">| RITES</span>
        </h1>
        <div className="mb-6 flex flex-col items-center gap-4">
          <label htmlFor="date-input" className="text-gray-700 font-medium">
            Select Date:
          </label>
          <input
            id="date-input"
            type="date"
            value={date}
            onChange={e => setDate(e.target.value)}
            className="rounded border border-gray-300 px-4 py-2 focus:ring-2 focus:ring-purple-300 focus:outline-none"
          />
          <button
            className="mt-2 bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded shadow font-semibold transition"
            onClick={handleFetch}
          >
            Fetch Data
          </button>
        </div>
        <div className={`text-base mb-4 p-3 rounded ${status.startsWith("Data fetched") ? "bg-green-100 text-green-800" : "bg-yellow-50 text-gray-700"}`}>
          <strong>Status:</strong> {status}
        </div>
        {files.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-2">Generated Files:</h2>
            <ul className="space-y-2">
              {files.map((file, idx) => (
                <li key={idx}>
                  <a
                    href={`https://rites-api.onrender.com/api/download/${file}`}

                    target="_blank"
                    rel="noopener noreferrer"
                    download
                    className="text-purple-600 hover:underline font-mono break-all"
                  >
                    {file}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}

