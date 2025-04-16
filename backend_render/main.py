import os
import logging
from flask import Flask, request, jsonify, send_from_directory # Aggiungi send_from_directory
from flask_cors import CORS
import json
from werkzeug.utils import secure_filename
from video_segmenter import VideoSegmenter
from ai_modules import CaptionGenerator, SemanticMatcher, MontageGenerator

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Abilita CORS

# --- MODIFICHE AI PERCORSI ---
# Configurazione delle directory per i file - USA I PERCORSI DEL CONTAINER!
# Leggi da variabili d'ambiente se impostate in docker-compose, altrimenti usa default /app/cartella
BASE_APP_DIR = '/app' # Directory base nel container
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_APP_DIR, 'uploads'))
TEMP_FOLDER = os.environ.get('TEMP_FOLDER', os.path.join(BASE_APP_DIR, 'temp'))
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', os.path.join(BASE_APP_DIR, 'output'))

logger.info(f"Using UPLOAD_FOLDER: {UPLOAD_FOLDER}")
logger.info(f"Using TEMP_FOLDER: {TEMP_FOLDER}")
logger.info(f"Using OUTPUT_FOLDER: {OUTPUT_FOLDER}")

# Creazione delle directory se non esistono all'interno del container
# (I volumi montati dovrebbero crearle se mappate a cartelle host esistenti,
# ma 'exist_ok=True' non fa danni e crea temp se non montata)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Applica la configurazione all'app Flask (UPLOAD_FOLDER è l'unico usato in app.config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max
# --- FINE MODIFICHE AI PERCORSI ---


# Estensioni consentite
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

# Inizializzazione dei moduli (questo rimane uguale, usa le variabili aggiornate)
video_segmenter = VideoSegmenter(TEMP_FOLDER)
caption_generator = CaptionGenerator(TEMP_FOLDER)
semantic_matcher = SemanticMatcher(TEMP_FOLDER)
montage_generator = MontageGenerator(TEMP_FOLDER, OUTPUT_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info("====> Richiesta ricevuta su /api/health <====") # Manteniamo il log di test
    return jsonify({"status": "ok", "message": "Backend server is running"}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    logger.info("Richiesta ricevuta su /api/upload")
    # Verifica se la richiesta contiene un file
    if 'video' not in request.files:
        logger.warning("Nessun file video fornito in /api/upload")
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']

    # Verifica se il file ha un nome
    if file.filename == '':
        logger.warning("Nessun file selezionato in /api/upload")
        return jsonify({"error": "No file selected"}), 400

    # Verifica se il file è di un tipo consentito
    if not allowed_file(file.filename):
        logger.warning(f"Tipo file non consentito: {file.filename}")
        return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    # Verifica se è stato fornito un riassunto
    if 'summary' not in request.form:
        logger.warning("Nessun riassunto fornito in /api/upload")
        return jsonify({"error": "No summary provided"}), 400

    summary = request.form['summary']

    # Salva il file
    filename = secure_filename(file.filename)
    # Usa app.config['UPLOAD_FOLDER'] che abbiamo impostato correttamente
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logger.info(f"Salvataggio video in: {file_path}")
    try:
        file.save(file_path)
        logger.info(f"Video salvato con successo.")
    except Exception as e:
        logger.error(f"Errore durante il salvataggio del video {file_path}: {e}")
        return jsonify({"error": f"Could not save video file: {e}"}), 500


    # Salva il riassunto
    summary_filename = f"{os.path.splitext(filename)[0]}_summary.txt"
    summary_path = os.path.join(app.config['UPLOAD_FOLDER'], summary_filename)
    logger.info(f"Salvataggio riassunto in: {summary_path}")
    try:
        with open(summary_path, 'w') as f:
            f.write(summary)
        logger.info("Riassunto salvato con successo.")
    except Exception as e:
        logger.error(f"Errore durante il salvataggio del riassunto {summary_path}: {e}")
        # Considera se eliminare il video caricato se il riassunto fallisce?
        return jsonify({"error": f"Could not save summary file: {e}"}), 500

    # Crea un ID per il job
    job_id = os.path.splitext(filename)[0]
    logger.info(f"Upload completato per job_id: {job_id}")

    return jsonify({
        "message": "Upload successful",
        "job_id": job_id,
        "video_path": file_path, # Restituisce il percorso *interno* al container
        "summary_path": summary_path # Restituisce il percorso *interno* al container
    }), 200

@app.route('/api/process/<job_id>', methods=['POST'])
def process_video(job_id):
    logger.info(f"Richiesta ricevuta su /api/process/{job_id}")
    try:
        # Recupera i percorsi dei file usando i percorsi corretti del container
        # NOTA: Qui stiamo assumendo l'estensione .mp4 o cercando altre
        # Sarebbe meglio salvare il nome file effettivo durante l'upload
        base_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}") # Senza estensione
        summary_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_summary.txt")
        video_path = None

        logger.info(f"Ricerca video per job {job_id} in {app.config['UPLOAD_FOLDER']}")
        for ext in ALLOWED_EXTENSIONS:
            potential_path = f"{base_video_path}.{ext}"
            if os.path.exists(potential_path):
                video_path = potential_path
                logger.info(f"Trovato video: {video_path}")
                break

        if not video_path:
            logger.error(f"Video non trovato per job {job_id}")
            return jsonify({"error": "Video file not found for job ID"}), 404

        if not os.path.exists(summary_path):
            logger.error(f"Riassunto non trovato: {summary_path}")
            return jsonify({"error": "Summary file not found"}), 404

        # Leggi il riassunto
        with open(summary_path, 'r') as f:
            summary = f.read()

        # Dividi il riassunto in frasi
        import re
        sentences = re.split(r'(?<=[.!?])\s+', summary)

        summary_segments = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():  # Ignora le frasi vuote
                summary_segments.append({
                    "id": i + 1,
                    "text": sentence.strip()
                })

        # Esegui la segmentazione del video (usando dati simulati come prima)
        logger.info(f"Avvio segmentazione (simulata) per {job_id}")
        scenes = [
            {"id": 1, "start_time": 0, "end_time": 10, "thumbnail": "/thumbnails/1.jpg"}, # Path thumbnail da rivedere
            {"id": 2, "start_time": 15, "end_time": 25, "thumbnail": "/thumbnails/2.jpg"},
            {"id": 3, "start_time": 30, "end_time": 40, "thumbnail": "/thumbnails/3.jpg"},
            {"id": 4, "start_time": 45, "end_time": 55, "thumbnail": "/thumbnails/4.jpg"},
            {"id": 5, "start_time": 60, "end_time": 70, "thumbnail": "/thumbnails/5.jpg"},
            {"id": 6, "start_time": 75, "end_time": 85, "thumbnail": "/thumbnails/6.jpg"}
        ]
        logger.info(f"Segmentazione (simulata) completata.")

        # Genera didascalie per le scene
        logger.info(f"Avvio generazione didascalie per {job_id}")
        scenes = caption_generator.generate_captions(scenes, job_id) # Assicurati che questa funzione salvi in TEMP_FOLDER
        logger.info(f"Generazione didascalie completata.")

        # Abbina le scene alle frasi del riassunto
        logger.info(f"Avvio matching semantico per {job_id}")
        summary_segments = semantic_matcher.match_scenes_to_summary(scenes, summary_segments, job_id) # Assicurati che questa usi TEMP_FOLDER
        logger.info(f"Matching semantico completato.")

        # Salva i risultati
        results = {
            "job_id": job_id,
            "scenes": scenes,
            "summary_segments": summary_segments
        }

        results_path = os.path.join(TEMP_FOLDER, f"{job_id}_results.json")
        logger.info(f"Salvataggio risultati in: {results_path}")
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2) # Aggiungi indent per leggibilità
        logger.info(f"Risultati salvati.")

        return jsonify({
            "message": "Processing complete",
            "job_id": job_id,
            "scenes": scenes,
            "summary_segments": summary_segments
        }), 200

    except Exception as e:
        logger.exception(f"Errore durante l'elaborazione del video {job_id}: {e}") # Usa logger.exception per includere traceback
        return jsonify({"error": f"Error processing video: {str(e)}"}), 500

@app.route('/api/matches/<job_id>', methods=['POST'])
def update_matches(job_id):
    logger.info(f"Richiesta ricevuta su /api/matches/{job_id}")
    if not request.is_json:
        logger.warning("Richiesta non JSON per /api/matches")
        return jsonify({"error": "Request must be JSON"}), 400

    matches_data = request.json # Rinomina per chiarezza
    if not isinstance(matches_data, dict) or 'matches' not in matches_data:
         logger.warning(f"Formato JSON non valido per /api/matches/{job_id}")
         return jsonify({"error": "Invalid JSON format. Expecting an object with a 'matches' key."}), 400

    matches = matches_data.get('matches', [])

    # Recupera i risultati precedenti
    results_path = os.path.join(TEMP_FOLDER, f"{job_id}_results.json")
    logger.info(f"Caricamento risultati precedenti da: {results_path}")

    if not os.path.exists(results_path):
        logger.error(f"File risultati non trovato: {results_path}")
        return jsonify({"error": "Results not found. Process the video first."}), 404

    try:
        with open(results_path, 'r') as f:
            results = json.load(f)

        # Aggiorna le corrispondenze
        # È più efficiente creare una mappa per cercare i segmenti
        segment_map = {segment['id']: segment for segment in results.get('summary_segments', [])}
        updated_count = 0
        for match in matches:
            segment_id = match.get('segmentId')
            scene_id = match.get('sceneId') # Può essere None se si scollega

            if segment_id in segment_map:
                segment_map[segment_id]['matchedSceneId'] = scene_id # Aggiorna direttamente
                updated_count += 1

        logger.info(f"Aggiornate {updated_count} corrispondenze per job {job_id}")

        # Salva i risultati aggiornati
        logger.info(f"Salvataggio risultati aggiornati in: {results_path}")
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)

        return jsonify({
            "message": "Matches updated",
            "job_id": job_id,
            "summary_segments": results.get('summary_segments', [])
        }), 200

    except Exception as e:
        logger.exception(f"Errore durante l'aggiornamento delle corrispondenze per {job_id}: {e}")
        return jsonify({"error": f"Error updating matches: {str(e)}"}), 500

@app.route('/api/generate/<job_id>', methods=['POST'])
def generate_montage(job_id):
    logger.info(f"Richiesta ricevuta su /api/generate/{job_id}")
    try:
        # Recupera i risultati
        results_path = os.path.join(TEMP_FOLDER, f"{job_id}_results.json")
        logger.info(f"Caricamento risultati da: {results_path}")
        if not os.path.exists(results_path):
            logger.error(f"File risultati non trovato: {results_path}")
            return jsonify({"error": "Results not found. Process the video first."}), 404

        with open(results_path, 'r') as f:
            results = json.load(f)

        # Recupera il percorso del video originale (come fatto in /process)
        base_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}")
        video_path = None
        logger.info(f"Ricerca video originale per job {job_id} in {app.config['UPLOAD_FOLDER']}")
        for ext in ALLOWED_EXTENSIONS:
            potential_path = f"{base_video_path}.{ext}"
            if os.path.exists(potential_path):
                video_path = potential_path
                logger.info(f"Trovato video originale: {video_path}")
                break

        if not video_path:
            logger.error(f"Video originale non trovato per job {job_id} durante la generazione montaggio")
            return jsonify({"error": "Original video file not found for job ID"}), 404

        # Genera il montaggio
        logger.info(f"Avvio generazione montaggio per job {job_id}")
        output_filename = f"{job_id}_montage.mp4" # Nome file di output standard
        output_path_internal = montage_generator.create_montage(
            video_path,
            results.get('scenes', []),
            results.get('summary_segments', []),
            job_id # Passa job_id per nome file output? Assicurati che create_montage lo usi
                   # e salvi in OUTPUT_FOLDER
        ) # Assicurati che ritorni il percorso completo /app/output/nomefile.mp4

        logger.info(f"Montaggio generato: {output_path_internal}")

        # --- MODIFICA PER DOWNLOAD ---
        # Invece di un URL finto, forniamo un endpoint per scaricare il file
        download_endpoint = f"/api/download/{output_filename}" # Usa il nome file generato

        return jsonify({
            "message": "Montage generated",
            "job_id": job_id,
            "output_path": output_path_internal, # Percorso interno al container
            "download_endpoint": download_endpoint # L'URL che il frontend userà per scaricare
        }), 200

    except Exception as e:
        logger.exception(f"Errore durante la generazione del montaggio per {job_id}: {e}")
        return jsonify({"error": f"Error generating montage: {str(e)}"}), 500

# --- NUOVA ROUTE PER IL DOWNLOAD EFFETTIVO ---
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    logger.info(f"Richiesta download per: {filename}")
    # Assicurati che il nome file sia sicuro
    safe_filename = secure_filename(filename)
    if not safe_filename: # Se secure_filename lo svuota, non è valido
        logger.warning(f"Tentativo di download con nome file non valido: {filename}")
        return jsonify({"error": "Invalid filename"}), 400

    logger.info(f"Invio file da directory: {OUTPUT_FOLDER}, nome file: {safe_filename}")
    try:
        # Usa send_from_directory per inviare il file in modo sicuro
        # OUTPUT_FOLDER deve essere il percorso assoluto nel container
        return send_from_directory(OUTPUT_FOLDER, safe_filename, as_attachment=True)
    except FileNotFoundError:
        logger.error(f"File non trovato per il download: {os.path.join(OUTPUT_FOLDER, safe_filename)}")
        return jsonify({"error": "Montage file not found"}), 404
    except Exception as e:
        logger.exception(f"Errore durante l'invio del file {safe_filename}: {e}")
        return jsonify({"error": f"Error sending file: {str(e)}"}), 500

# Rimuovi il blocco if __name__ == "__main__" perché Gunicorn non lo usa
# if __name__ == "__main__":
#    # Questo non viene eseguito quando si usa Gunicorn
#    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))