import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="max-w-3xl w-full bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold text-center mb-6">Benvenuto in Movie Montage Creator</h2>
        
        <p className="text-gray-700 mb-8 text-center">
          Questa applicazione ti permette di creare montaggi video coerenti basati su riassunti scritti.
          Carica un film completo e un riassunto scritto, e l'applicazione creerà automaticamente un montaggio
          che rappresenta visivamente la narrativa fornita.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
            <h3 className="font-semibold text-lg mb-2">1. Carica</h3>
            <p className="text-sm text-gray-600 mb-4">
              Carica un film completo e un riassunto scritto per iniziare il processo.
            </p>
          </div>
          
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
            <h3 className="font-semibold text-lg mb-2">2. Rivedi</h3>
            <p className="text-sm text-gray-600 mb-4">
              Esamina le scene segmentate e le didascalie generate, e modifica le corrispondenze se necessario.
            </p>
          </div>
          
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
            <h3 className="font-semibold text-lg mb-2">3. Crea</h3>
            <p className="text-sm text-gray-600 mb-4">
              Visualizza l'anteprima del montaggio finale e scarica il video completato.
            </p>
          </div>
        </div>
        
        <div className="flex justify-center">
          <Link 
            href="/upload" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-lg transition-colors"
          >
            Inizia Ora
          </Link>
        </div>
      </div>
    </div>
  );
}
