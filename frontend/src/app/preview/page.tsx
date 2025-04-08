"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import apiClient from "@/lib/api/apiClient";

// Componente di caricamento
function LoadingState() {
  return (
    <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6 my-8 text-center">
      <p className="text-gray-600">Caricamento in corso...</p>
    </div>
  );
}

// Componente principale avvolto in Suspense
function PreviewPageContent() {
  const searchParams = useSearchParams();
  const jobId = searchParams.get('jobId');
  
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");
  const [montageInfo, setMontageInfo] = useState({
    duration: "3:42",
    sceneCount: 6,
    resolution: "1920x1080",
    format: "MP4 (H.264)",
    summary: "John decide di intraprendere un viaggio per ritrovare se stesso. Maria è preoccupata per la scomparsa del marito. Gli amici di John si incontrano per discutere della situazione. John fugge dalla città in tutta fretta. Maria riceve una chiamata misteriosa. Alla fine, tutti si riuniscono per celebrare il ritorno di John."
  });
  
  // Carica i dati all'inizializzazione
  useEffect(() => {
    if (!jobId) {
      setError("ID del job non trovato. Torna alla pagina di caricamento.");
      setIsLoading(false);
      return;
    }
    
    const fetchData = async () => {
      try {
        // In un'implementazione reale, qui recupereremmo i dati dal backend
        // Per ora, utilizziamo dati simulati
        
        // Simula il recupero dell'URL di download
        const downloadData = await apiClient.getDownloadUrl(jobId);
        setDownloadUrl(downloadData.download_url);
        
        setIsLoading(false);
      } catch (error) {
        console.error("Errore durante il recupero dei dati:", error);
        setError("Si è verificato un errore durante il recupero dei dati. Riprova.");
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [jobId]);
  
  const handleDownload = async () => {
    if (!jobId || !downloadUrl) return;
    
    setIsDownloading(true);
    
    // Simula il download
    const interval = setInterval(() => {
      setDownloadProgress((prev) => {
        if (prev >= 95) {
          clearInterval(interval);
          return prev;
        }
        return prev + 5;
      });
    }, 300);

    // Simula il completamento del download
    setTimeout(() => {
      clearInterval(interval);
      setDownloadProgress(100);
      setTimeout(() => {
        setIsDownloading(false);
        // In un'applicazione reale, qui si attiverebbe il download effettivo
        window.open(downloadUrl, '_blank');
      }, 1000);
    }, 3000);
  };

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6 my-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
        <Link 
          href="/upload" 
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          Torna al Caricamento
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6 my-8">
      <h2 className="text-2xl font-bold mb-6">Anteprima del Montaggio</h2>
      
      <div className="mb-8">
        <div className="video-container bg-black rounded-lg overflow-hidden mb-4 relative h-64">
          {/* In un'applicazione reale, qui ci sarebbe un player video */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-white text-center">
              <svg 
                className="w-20 h-20 mx-auto mb-4 opacity-60" 
                fill="currentColor" 
                viewBox="0 0 20 20" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  fillRule="evenodd" 
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" 
                  clipRule="evenodd"
                />
              </svg>
              <p className="text-xl font-medium">Anteprima del Montaggio</p>
              <p className="text-sm opacity-75 mt-2">
                In un'applicazione reale, qui verrebbe visualizzato il montaggio video finale
              </p>
            </div>
          </div>
        </div>
        
        <div className="flex justify-center space-x-4">
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors flex items-center">
            <svg 
              className="w-5 h-5 mr-2" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" 
              />
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
            Riproduci
          </button>
          
          <button 
            onClick={handleDownload}
            disabled={isDownloading}
            className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md transition-colors flex items-center disabled:bg-green-400"
          >
            {!isDownloading && (
              <svg 
                className="w-5 h-5 mr-2" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" 
                />
              </svg>
            )}
            {isDownloading ? "Download in corso..." : "Scarica Montaggio"}
          </button>
        </div>
        
        {isDownloading && (
          <div className="mt-4 space-y-2">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-green-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${downloadProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 text-center">
              {downloadProgress < 100
                ? `Download in corso... ${downloadProgress}%`
                : "Download completato!"}
            </p>
          </div>
        )}
      </div>
      
      <div className="border-t pt-6">
        <h3 className="text-lg font-semibold mb-4">Riepilogo del Montaggio</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Statistiche</h4>
            <ul className="space-y-2 text-sm">
              <li className="flex justify-between">
                <span className="text-gray-600">Durata totale:</span>
                <span className="font-medium">{montageInfo.duration}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">Numero di scene:</span>
                <span className="font-medium">{montageInfo.sceneCount}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">Risoluzione:</span>
                <span className="font-medium">{montageInfo.resolution}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">Formato:</span>
                <span className="font-medium">{montageInfo.format}</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Riassunto Utilizzato</h4>
            <div className="bg-gray-50 p-3 rounded-md text-sm text-gray-700">
              <p>{montageInfo.summary}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-8 flex justify-between">
        <Link 
          href={jobId ? `/review?jobId=${jobId}` : "/review"} 
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors"
        >
          Torna alla Revisione
        </Link>
        
        <Link 
          href="/" 
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          Nuovo Montaggio
        </Link>
      </div>
    </div>
  );
}

// Componente principale che utilizza Suspense
export default function PreviewPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <PreviewPageContent />
    </Suspense>
  );
}
