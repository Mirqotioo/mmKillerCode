# Documentazione Tecnica di Movie Montage Creator

## Indice
1. [Panoramica del Sistema](#panoramica-del-sistema)
2. [Architettura](#architettura)
3. [Componenti del Frontend](#componenti-del-frontend)
4. [Componenti del Backend](#componenti-del-backend)
5. [API](#api)
6. [Modelli AI](#modelli-ai)
7. [Ottimizzazione delle Prestazioni](#ottimizzazione-delle-prestazioni)
8. [Deployment](#deployment)
9. [Sviluppi Futuri](#sviluppi-futuri)

## Panoramica del Sistema

Movie Montage Creator è un'applicazione web che permette di creare montaggi video basati su riassunti scritti. L'applicazione utilizza tecnologie di intelligenza artificiale per segmentare automaticamente i film in singole inquadrature, generare didascalie descrittive e abbinare semanticamente le scene al riassunto fornito.

## Architettura

L'applicazione segue un'architettura client-server:

- **Frontend**: Applicazione Next.js che fornisce l'interfaccia utente
- **Backend**: API RESTful basata su Flask che gestisce l'elaborazione video e l'integrazione dei modelli AI

### Diagramma dell'Architettura

```
+------------------+        +------------------+        +------------------+
|                  |        |                  |        |                  |
|  Client Browser  | <----> |  Next.js Server  | <----> |  Flask Backend   |
|                  |        |                  |        |                  |
+------------------+        +------------------+        +--------+---------+
                                                                 |
                                                                 v
                                                        +------------------+
                                                        |                  |
                                                        |  AI Models       |
                                                        |  - CLIP          |
                                                        |  - Caption Gen   |
                                                        |                  |
                                                        +------------------+
```

## Componenti del Frontend

### Struttura delle Directory

```
frontend/
├── src/
│   ├── app/
│   │   ├── upload/
│   │   │   └── page.tsx
│   │   ├── review/
│   │   │   └── page.tsx
│   │   ├── preview/
│   │   │   └── page.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/
│   │   └── video/
│   ├── hooks/
│   │   └── video/
│   ├── lib/
│   │   └── api/
│   │       └── apiClient.ts
│   └── tests/
│       └── frontend.test.tsx
├── public/
└── package.json
```

### Pagine Principali

- **Home (page.tsx)**: Pagina iniziale con introduzione all'applicazione
- **Upload (upload/page.tsx)**: Gestisce il caricamento del video e del riassunto
- **Review (review/page.tsx)**: Permette la revisione e la modifica delle corrispondenze
- **Preview (preview/page.tsx)**: Mostra l'anteprima del montaggio e permette il download

### Client API

Il file `apiClient.ts` gestisce tutte le chiamate API al backend:

- `uploadVideo`: Carica un video e un riassunto
- `processVideo`: Avvia l'elaborazione del video
- `updateMatches`: Aggiorna le corrispondenze tra scene e frasi
- `generateMontage`: Genera il montaggio finale
- `getDownloadUrl`: Ottiene l'URL di download del montaggio

## Componenti del Backend

### Struttura delle Directory

```
backend/
├── app.py
├── main.py
├── video_segmenter.py
├── ai_modules.py
├── ai_models_detailed.py
├── video_processing.py
├── optimized_processing.py
├── tests/
│   └── test_backend.py
├── uploads/
├── temp/
└── output/
```

### Moduli Principali

- **main.py**: Punto di ingresso dell'applicazione Flask
- **video_segmenter.py**: Gestisce la segmentazione del video in scene
- **ai_modules.py**: Implementa i moduli AI di base
- **ai_models_detailed.py**: Implementa versioni dettagliate dei moduli AI
- **video_processing.py**: Gestisce l'elaborazione video e la creazione del montaggio
- **optimized_processing.py**: Implementa ottimizzazioni per le prestazioni e la scalabilità

## API

Il backend espone le seguenti API RESTful:

### Endpoint

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/health` | GET | Verifica lo stato del backend |
| `/api/upload` | POST | Carica un video e un riassunto |
| `/api/process/<job_id>` | POST | Elabora un video caricato |
| `/api/matches/<job_id>` | POST | Aggiorna le corrispondenze |
| `/api/generate/<job_id>` | POST | Genera il montaggio finale |
| `/api/download/<job_id>` | GET | Ottiene l'URL di download |

### Esempi di Richieste e Risposte

#### Caricamento del Video

**Richiesta**:
```
POST /api/upload
Content-Type: multipart/form-data

{
  "video": [file binario],
  "summary": "Questo è un riassunto di esempio."
}
```

**Risposta**:
```json
{
  "message": "Upload successful",
  "job_id": "video_123456",
  "video_path": "/path/to/video.mp4",
  "summary_path": "/path/to/summary.txt"
}
```

#### Elaborazione del Video

**Richiesta**:
```
POST /api/process/video_123456
```

**Risposta**:
```json
{
  "message": "Processing complete",
  "job_id": "video_123456",
  "scenes": [...],
  "summary_segments": [...]
}
```

## Modelli AI

### CLIP (Contrastive Language-Image Pre-training)

CLIP è un modello di OpenAI che apprende rappresentazioni visive da descrizioni testuali naturali. Nell'applicazione, CLIP viene utilizzato per calcolare la similarità semantica tra le didascalie delle scene e le frasi del riassunto.

### Generatore di Didascalie

Il generatore di didascalie utilizza un modello di visione-linguaggio pre-addestrato per generare descrizioni testuali delle scene. Nell'implementazione attuale, utilizziamo un approccio simulato, ma in un'implementazione reale si utilizzerebbe un modello come BLIP o VinVL.

## Ottimizzazione delle Prestazioni

### Tecniche di Ottimizzazione

- **Parallelizzazione**: Utilizzo di ThreadPoolExecutor e ProcessPoolExecutor per elaborare più elementi contemporaneamente
- **Caching**: Memorizzazione dei risultati intermedi per evitare ricalcoli
- **Elaborazione in Batch**: Elaborazione degli elementi in gruppi per ottimizzare l'uso della memoria
- **Lazy Loading**: Caricamento dei modelli AI solo quando necessario

### Gestione della Memoria

- Utilizzo di tecniche di gestione efficiente della memoria per file video di grandi dimensioni
- Rilascio delle risorse non necessarie dopo l'uso
- Ottimizzazione del caricamento e della gestione dei modelli AI

## Deployment

### Requisiti di Deployment

- Server con almeno 4GB di RAM
- Almeno 10GB di spazio su disco
- Python 3.8 o superiore
- Node.js 16.x o superiore

### Istruzioni per il Deployment

1. **Preparazione dell'Ambiente**:
   ```bash
   # Installa le dipendenze del sistema
   apt-get update
   apt-get install -y python3-venv python3-dev ffmpeg
   ```

2. **Deployment del Backend**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

3. **Deployment del Frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   npm start
   ```

4. **Configurazione del Server Web**:
   Configura un server web come Nginx per servire il frontend e fare da proxy per il backend.

### Configurazione di Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Sviluppi Futuri

### Miglioramenti Pianificati

- **Integrazione di Modelli AI Più Avanzati**: Utilizzare modelli più recenti per migliorare la qualità delle didascalie e del matching semantico
- **Supporto per Più Formati Video**: Aggiungere supporto per formati video aggiuntivi
- **Interfaccia di Editing Avanzata**: Implementare un'interfaccia più avanzata per la modifica delle corrispondenze
- **Elaborazione Distribuita**: Implementare un sistema di elaborazione distribuita per gestire file video di dimensioni molto grandi
- **Personalizzazione del Montaggio**: Aggiungere opzioni per personalizzare lo stile e il ritmo del montaggio
- **Supporto per Sottotitoli**: Aggiungere la possibilità di includere sottotitoli nel montaggio finale
