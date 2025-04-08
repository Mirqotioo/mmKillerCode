# Guida all'Installazione e Utilizzo di Movie Montage Creator

## Indice
1. [Introduzione](#introduzione)
2. [Requisiti di Sistema](#requisiti-di-sistema)
3. [Installazione](#installazione)
4. [Utilizzo dell'Applicazione](#utilizzo-dellapplicazione)
5. [Architettura del Sistema](#architettura-del-sistema)
6. [Risoluzione dei Problemi](#risoluzione-dei-problemi)
7. [FAQ](#faq)

## Introduzione

Movie Montage Creator è un'applicazione web che permette di creare montaggi video basati su riassunti scritti. L'applicazione utilizza tecnologie di intelligenza artificiale per segmentare automaticamente i film in singole inquadrature, generare didascalie descrittive e abbinare semanticamente le scene al riassunto fornito.

### Caratteristiche Principali

- Segmentazione automatica dei film in scene individuali
- Generazione di didascalie descrittive per ogni scena
- Matching semantico tra scene e frasi del riassunto
- Interfaccia intuitiva per la revisione e la modifica delle corrispondenze
- Creazione automatica di montaggi video coerenti
- Ottimizzazione delle prestazioni per file video di grandi dimensioni

## Requisiti di Sistema

### Frontend
- Node.js 16.x o superiore
- npm 7.x o superiore o pnpm 6.x o superiore

### Backend
- Python 3.8 o superiore
- Almeno 4GB di RAM
- Almeno 10GB di spazio su disco
- Connessione a Internet per il download dei modelli AI

### Dipendenze Python Principali
- Flask 2.x
- PySceneDetect
- OpenCV
- MoviePy
- Transformers
- CLIP

## Installazione

### Clonare il Repository

```bash
git clone https://github.com/yourusername/movie-montage-app.git
cd movie-montage-app
```

### Installazione del Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Installazione del Frontend

```bash
cd frontend
npm install  # o pnpm install
```

## Utilizzo dell'Applicazione

### Avvio del Backend

```bash
cd backend
source venv/bin/activate  # Su Windows: venv\Scripts\activate
python main.py
```

Il server backend sarà disponibile all'indirizzo `http://localhost:5000`.

### Avvio del Frontend

```bash
cd frontend
npm run dev  # o pnpm dev
```

L'applicazione frontend sarà disponibile all'indirizzo `http://localhost:3000`.

### Flusso di Utilizzo

1. **Caricamento del Video e del Riassunto**
   - Accedi alla pagina principale dell'applicazione
   - Carica un file video (formati supportati: MP4, MOV, AVI)
   - Inserisci il riassunto scritto nella casella di testo
   - Clicca su "Carica e Procedi"

2. **Revisione delle Corrispondenze**
   - Esamina le scene segmentate e le didascalie generate
   - Verifica le corrispondenze automatiche tra le frasi del riassunto e le scene
   - Modifica le corrispondenze se necessario utilizzando i menu a discesa
   - Clicca su "Finalizza Montaggio" quando sei soddisfatto

3. **Anteprima e Download del Montaggio**
   - Visualizza l'anteprima del montaggio finale
   - Controlla le statistiche del montaggio (durata, numero di scene, ecc.)
   - Clicca su "Scarica Montaggio" per salvare il video sul tuo dispositivo

## Architettura del Sistema

L'applicazione è strutturata in due componenti principali:

### Frontend (Next.js)
- **Pagine**:
  - `upload`: Gestisce il caricamento del video e del riassunto
  - `review`: Permette la revisione e la modifica delle corrispondenze
  - `preview`: Mostra l'anteprima del montaggio e permette il download

- **Componenti**:
  - Interfaccia utente reattiva e mobile-friendly
  - Gestione dello stato dell'applicazione
  - Comunicazione con il backend tramite API REST

### Backend (Flask)
- **Moduli**:
  - `video_segmenter.py`: Segmentazione del video in scene
  - `ai_models_detailed.py`: Generazione di didascalie e matching semantico
  - `video_processing.py`: Elaborazione video e creazione del montaggio
  - `optimized_processing.py`: Ottimizzazione delle prestazioni e scalabilità

- **Pipeline di Elaborazione**:
  1. Segmentazione del video in scene
  2. Generazione di didascalie per ogni scena
  3. Matching semantico tra scene e frasi del riassunto
  4. Compilazione del montaggio finale

## Risoluzione dei Problemi

### Problemi Comuni

#### Il caricamento del video è lento o fallisce
- Verifica che il file video non superi i 2GB
- Assicurati di avere una connessione Internet stabile
- Prova a utilizzare un formato video diverso (MP4 è consigliato)

#### La segmentazione del video non è accurata
- I video con molte transizioni rapide possono causare problemi
- Prova a utilizzare un video con scene più distinte
- Regola manualmente le corrispondenze nella pagina di revisione

#### Il matching semantico non è preciso
- Fornisci un riassunto più dettagliato e descrittivo
- Utilizza frasi che descrivono elementi visivi concreti
- Regola manualmente le corrispondenze nella pagina di revisione

#### L'applicazione è lenta o si blocca
- Verifica di avere abbastanza memoria disponibile
- Chiudi altre applicazioni che consumano molte risorse
- Riavvia l'applicazione e il browser

## FAQ

### Quali formati video sono supportati?
L'applicazione supporta i formati video più comuni come MP4, MOV e AVI.

### Qual è la dimensione massima del file video?
La dimensione massima consigliata è di 2GB.

### Posso modificare manualmente le corrispondenze?
Sì, nella pagina di revisione puoi modificare le corrispondenze tra le frasi del riassunto e le scene del video.

### Come funziona il matching semantico?
Il matching semantico utilizza il modello CLIP per calcolare la similarità tra le didascalie delle scene e le frasi del riassunto, associando ogni frase alla scena che meglio rappresenta il suo significato.

### Posso utilizzare l'applicazione offline?
No, l'applicazione richiede una connessione Internet per il download dei modelli AI e per il funzionamento corretto.

### I miei video vengono salvati sui vostri server?
No, tutti i video vengono elaborati localmente sul tuo dispositivo e non vengono caricati su server esterni.

### Come posso migliorare la qualità del montaggio?
- Utilizza video di alta qualità
- Fornisci un riassunto dettagliato e ben strutturato
- Rivedi e modifica manualmente le corrispondenze
- Utilizza video con scene ben definite e distinte
