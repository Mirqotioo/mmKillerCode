"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import apiClient from "@/lib/api/apiClient";

interface Scene {
  id: number;
  start_time: number;
  end_time: number;
  thumbnail: string;
  caption: string;
}

interface SummarySegment {
  id: number;
  text: string;
  matchedSceneId: number;
}

// Componente di caricamento
function LoadingState() {
  return (
    <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6 my-8 text-center">
      <p className="text-gray-600">Caricamento in corso...</p>
    </div>
  );
}

// Componente principale avvolto in Suspense
function ReviewPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const jobId = searchParams.get('jobId');
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [scenes, setScenes] = useState<Scene[]>([]);
  const [summarySegments, setSummarySegments] = useState<SummarySegment[]>([]);
  
  // Carica i dati all'inizializzazione
  useEffect(() => {
    if (!jobId) {
      setError("ID del job non trovato. Torna alla pagina di caricamento.");
      setIsLoading(false);
      return;
    }
    
    // Simula il caricamento dei dati dal backend
    const fetchData = async () => {
      try {
        // In un'implementazione reale, qui recupereremmo i dati dal backend
        // Dati simulati per ora
        const mockScenes: Scene[] = [
          { id: 1, start_time: 0, end_time: 10, thumbnail: "/placeholder.jpg", caption: "Un uomo cammina lungo una strada deserta al tramonto" },
          { id: 2, start_time: 15, end_time: 25, thumbnail: "/placeholder.jpg", caption: "Una donna guarda fuori dalla finestra con espressione preoccupata" },
          { id: 3, start_time: 30, end_time: 40, thumbnail: "/placeholder.jpg", caption: "Due persone conversano in un caffè affollato" },
          { id: 4, start_time: 45, end_time: 55, thumbnail: "/placeholder.jpg", caption: "Un'auto sfreccia lungo un'autostrada di notte" },
          { id: 5, start_time: 60, end_time: 70, thumbnail: "/placeholder.jpg", caption: "Un telefono squilla in una stanza vuota" },
          { id: 6, start_time: 75, end_time: 85, thumbnail: "/placeholder.jpg", caption: "Un gruppo di persone festeggia a una festa" },
        ];
        
        const mockSummarySegments: SummarySegment[] = [
          { id: 1, text: "John decide di intraprendere un viaggio per ritrovare se stesso.", matchedSceneId: 1 },
          { id: 2, text: "Maria è preoccupata per la scomparsa del marito.", matchedSceneId: 2 },
          { id: 3, text: "Gli amici di John si incontrano per discutere della situazione.", matchedSceneId: 3 },
          { id: 4, text: "John fugge dalla città in tutta fretta.", matchedSceneId: 4 },
          { id: 5, text: "Maria riceve una chiamata misteriosa.", matchedSceneId: 5 },
          { id: 6, text: "Alla fine, tutti si riuniscono per celebrare il ritorno di John.", matchedSceneId: 6 },
        ];
        
        setScenes(mockScenes);
        setSummarySegments(mockSummarySegments);
        setIsLoading(false);
      } catch (error) {
        console.error("Errore durante il recupero dei dati:", error);
        setError("Si è verificato un errore durante il recupero dei dati. Riprova.");
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [jobId]);
  
  // Funzione per aggiornare l'associazione tra segmento e scena
  const updateMatch = (segmentId: number, sceneId: number) => {
    setSummarySegments(prev => 
      prev.map(segment => 
        segment.id === segmentId ? { ...segment, matchedSceneId: sceneId } : segment
      )
    );
  };
  
  const handleFinalize = async () => {
    if (!jobId) return;
    
    setIsProcessing(true);
    
    try {
      // Aggiorna le corrispondenze nel backend
      const matches = summarySegments.map(segment => ({
        segmentId: segment.id,
        sceneId: segment.matchedSceneId
      }));
      
      await apiClient.updateMatches(jobId, matches);
      
      // Genera il montaggio
      await apiClient.generateMontage(jobId);
      
      // Reindirizza alla pagina di anteprima
      router.push(`/preview?jobId=${jobId}`);
    } catch (error) {
      console.error("Errore durante la finalizzazione:", error);
      setError("Si è verificato un errore durante la finalizzazione. Riprova.");
      setIsProcessing(false);
    }
  };

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6 my-8">
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
    <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6 my-8">
      <h2 className="text-2xl font-bold mb-6">Rivedi e Modifica le Corrispondenze</h2>
      
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-3">Istruzioni:</h3>
        <p className="text-gray-700 mb-4">
          Rivedi le corrispondenze automatiche tra le frasi del riassunto e le scene del film.
          Puoi modificare queste corrispondenze selezionando una scena diversa per ciascuna frase.
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Colonna sinistra: Frasi del riassunto */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Frasi del Riassunto</h3>
          <div className="space-y-4">
            {summarySegments.map(segment => (
              <div key={segment.id} className="p-4 border rounded-lg bg-gray-50">
                <p className="mb-2">{segment.text}</p>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 mr-2">Scena abbinata:</span>
                  <select 
                    value={segment.matchedSceneId}
                    onChange={(e) => updateMatch(segment.id, parseInt(e.target.value))}
                    className="border rounded px-2 py-1 text-sm"
                  >
                    {scenes.map(scene => (
                      <option key={scene.id} value={scene.id}>
                        {scene.id}: {scene.caption.substring(0, 30)}...
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Colonna destra: Scene disponibili */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Scene Disponibili</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {scenes.map(scene => (
              <div 
                key={scene.id} 
                className="scene-thumbnail rounded-lg overflow-hidden border bg-gray-100"
              >
                <div className="aspect-video bg-gray-300 flex items-center justify-center">
                  <span className="text-2xl font-bold text-gray-500">{scene.id}</span>
                </div>
                <div className="p-2">
                  <p className="text-xs text-gray-700 line-clamp-2">{scene.caption}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="mt-8 flex justify-between">
        <Link 
          href="/upload" 
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors"
        >
          Torna al Caricamento
        </Link>
        
        <button
          onClick={handleFinalize}
          disabled={isProcessing}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md transition-colors disabled:bg-blue-400"
        >
          {isProcessing ? "Elaborazione in corso..." : "Finalizza Montaggio"}
        </button>
      </div>
    </div>
  );
}

// Componente principale che utilizza Suspense
export default function ReviewPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <ReviewPageContent />
    </Suspense>
  );
}
