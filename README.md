# Movie Montage Creator - README

## Panoramica

Movie Montage Creator è un'applicazione web che permette di creare montaggi video basati su riassunti scritti. L'applicazione utilizza tecnologie di intelligenza artificiale per segmentare automaticamente i film in singole inquadrature, generare didascalie descrittive e abbinare semanticamente le scene al riassunto fornito.

## Caratteristiche Principali

- Segmentazione automatica dei film in scene individuali
- Generazione di didascalie descrittive per ogni scena
- Matching semantico tra scene e frasi del riassunto
- Interfaccia intuitiva per la revisione e la modifica delle corrispondenze
- Creazione automatica di montaggi video coerenti
- Ottimizzazione delle prestazioni per file video di grandi dimensioni

## Struttura del Progetto

```
movie_montage_app/
├── backend/                # Backend Flask
│   ├── app.py              # Applicazione Flask
│   ├── main.py             # Punto di ingresso
│   ├── video_segmenter.py  # Segmentazione video
│   ├── ai_modules.py       # Moduli AI di base
│   ├── ai_models_detailed.py # Moduli AI dettagliati
│   ├── video_processing.py # Elaborazione video
│   ├── optimized_processing.py # Ottimizzazioni
│   └── tests/              # Test del backend
├── frontend/               # Frontend Next.js
│   ├── src/                # Codice sorgente
│   │   ├── app/            # Pagine dell'applicazione
│   │   ├── components/     # Componenti React
│   │   ├── hooks/          # Hook personalizzati
│   │   ├── lib/            # Librerie e utilità
│   │   └── tests/          # Test del frontend
│   └── public/             # File statici
├── docs/                   # Documentazione
│   ├── user_guide.md       # Guida utente
│   └── technical_docs.md   # Documentazione tecnica
├── deploy.sh               # Script di deployment
└── todo.md                 # Piano di sviluppo completato
```

## Installazione

Per installare e avviare l'applicazione, seguire questi passaggi:

1. Clonare il repository
2. Eseguire lo script di deployment:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
3. Avviare l'applicazione:
   ```bash
   ./start.sh
   ```

Per istruzioni dettagliate, consultare la [Guida Utente](docs/user_guide.md).

## Documentazione

- [Guida Utente](docs/user_guide.md): Istruzioni per l'installazione e l'utilizzo dell'applicazione
- [Documentazione Tecnica](docs/technical_docs.md): Dettagli sull'architettura e l'implementazione

## Tecnologie Utilizzate

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: Flask, Python
- **Elaborazione Video**: PySceneDetect, OpenCV, MoviePy
- **AI**: CLIP, Transformers

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
