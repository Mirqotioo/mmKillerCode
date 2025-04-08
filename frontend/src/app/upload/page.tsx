"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import apiClient from "@/lib/api/apiClient";

export default function UploadPage() {
  const router = useRouter();
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [summary, setSummary] = useState("");
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setVideoFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!videoFile) {
      setError("Seleziona un file video");
      return;
    }
    
    if (!summary.trim()) {
      setError("Inserisci un riassunto");
      return;
    }
    
    setError("");
    setIsUploading(true);
    
    try {
      // Simula il progresso di caricamento
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 5;
        });
      }, 500);
      
      // Carica il video e il riassunto
      const uploadResult = await apiClient.uploadVideo(videoFile, summary);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Elabora il video
      const jobId = uploadResult.job_id;
      await apiClient.processVideo(jobId);
      
      // Reindirizza alla pagina di revisione
      setTimeout(() => {
        router.push(`/review?jobId=${jobId}`);
      }, 1000);
      
    } catch (error) {
      console.error("Errore durante il caricamento:", error);
      setError("Si è verificato un errore durante il caricamento. Riprova.");
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8 my-8">
      <h2 className="text-2xl font-bold mb-6">Carica Video e Riassunto</h2>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Video File
          </label>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input
              type="file"
              accept="video/*"
              className="hidden"
              id="video-upload"
              onChange={handleFileChange}
              required
            />
            <label
              htmlFor="video-upload"
              className="cursor-pointer flex flex-col items-center justify-center"
            >
              <svg
                className="w-12 h-12 text-gray-400 mb-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                ></path>
              </svg>
              <p className="text-sm text-gray-600">
                {videoFile ? videoFile.name : "Clicca per caricare o trascina qui il tuo file video"}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Supporta MP4, MOV, AVI (max 2GB)
              </p>
            </label>
          </div>
        </div>

        <div>
          <label
            htmlFor="summary"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Riassunto Scritto
          </label>
          <textarea
            id="summary"
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Inserisci il riassunto scritto che verrà utilizzato per creare il montaggio video..."
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            required
          ></textarea>
        </div>

        {isUploading ? (
          <div className="space-y-3">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 text-center">
              {uploadProgress < 100
                ? `Caricamento in corso... ${uploadProgress}%`
                : "Caricamento completato! Elaborazione in corso..."}
            </p>
          </div>
        ) : (
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          >
            Carica e Procedi
          </button>
        )}
      </form>
    </div>
  );
}
