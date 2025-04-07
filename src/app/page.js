export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">mmKiller - Movie Montage Creator</h1>
      <p className="mb-4">
        Benvenuto in mmKiller, l'applicazione che crea montaggi video basati su riassunti scritti.
      </p>
      <div className="bg-gray-100 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Funzionalità principali:</h2>
        <ul className="list-disc pl-5">
          <li>Segmentazione automatica dei film in scene individuali</li>
          <li>Generazione di didascalie descrittive per ogni scena</li>
          <li>Matching semantico tra scene e frasi del riassunto</li>
          <li>Creazione automatica di montaggi video coerenti</li>
        </ul>
      </div>
    </div>
  )
}
