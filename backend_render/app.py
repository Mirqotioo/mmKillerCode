from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import json
from werkzeug.utils import secure_filename

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurazione delle directory per i file
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# Creazione delle directory se non esistono
for folder in [UPLOAD_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max

# Estensioni consentite
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend server is running"}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Verifica se la richiesta contiene un file
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    file = request.files['video']
    
    # Verifica se il file ha un nome
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Verifica se il file è di un tipo consentito
    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
    
    # Verifica se è stato fornito un riassunto
    if 'summary' not in request.form:
        return jsonify({"error": "No summary provided"}), 400
    
    summary = request.form['summary']
    
    # Salva il file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Salva il riassunto
    summary_filename = f"{os.path.splitext(filename)[0]}_summary.txt"
    summary_path = os.path.join(app.config['UPLOAD_FOLDER'], summary_filename)
    with open(summary_path, 'w') as f:
        f.write(summary)
    
    # Crea un ID per il job
    job_id = os.path.splitext(filename)[0]
    
    # In un'implementazione reale, qui si avvierebbe il processo di elaborazione in background
    
    return jsonify({
        "message": "Upload successful",
        "job_id": job_id,
        "video_path": file_path,
        "summary_path": summary_path
    }), 200

@app.route('/api/process/<job_id>', methods=['POST'])
def process_video(job_id):
    # In un'implementazione reale, qui si avvierebbe il processo di segmentazione e analisi
    # Per ora, restituiamo dati simulati
    
    scenes = [
        {"id": 1, "start_time": 0, "end_time": 10, "thumbnail": "/thumbnails/1.jpg", "caption": "Un uomo cammina lungo una strada deserta al tramonto"},
        {"id": 2, "start_time": 15, "end_time": 25, "thumbnail": "/thumbnails/2.jpg", "caption": "Una donna guarda fuori dalla finestra con espressione preoccupata"},
        {"id": 3, "start_time": 30, "end_time": 40, "thumbnail": "/thumbnails/3.jpg", "caption": "Due persone conversano in un caffè affollato"},
        {"id": 4, "start_time": 45, "end_time": 55, "thumbnail": "/thumbnails/4.jpg", "caption": "Un'auto sfreccia lungo un'autostrada di notte"},
        {"id": 5, "start_time": 60, "end_time": 70, "thumbnail": "/thumbnails/5.jpg", "caption": "Un telefono squilla in una stanza vuota"},
        {"id": 6, "start_time": 75, "end_time": 85, "thumbnail": "/thumbnails/6.jpg", "caption": "Un gruppo di persone festeggia a una festa"}
    ]
    
    # Leggi il riassunto
    summary_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_summary.txt")
    try:
        with open(summary_path, 'r') as f:
            summary = f.read()
    except FileNotFoundError:
        return jsonify({"error": "Summary file not found"}), 404
    
    # Dividi il riassunto in frasi
    import re
    sentences = re.split(r'(?<=[.!?])\s+', summary)
    
    summary_segments = []
    for i, sentence in enumerate(sentences[:6]):  # Limita a 6 frasi per semplicità
        summary_segments.append({
            "id": i + 1,
            "text": sentence,
            "matchedSceneId": i + 1  # Associazione semplificata 1:1
        })
    
    # Salva i risultati
    results = {
        "job_id": job_id,
        "scenes": scenes,
        "summary_segments": summary_segments
    }
    
    results_path = os.path.join(app.config['TEMP_FOLDER'], f"{job_id}_results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f)
    
    return jsonify({
        "message": "Processing complete",
        "job_id": job_id,
        "scenes": scenes,
        "summary_segments": summary_segments
    }), 200

@app.route('/api/matches/<job_id>', methods=['POST'])
def update_matches(job_id):
    # Aggiorna le corrispondenze tra scene e frasi
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    matches = request.json.get('matches', [])
    
    # In un'implementazione reale, qui si salverebbero le corrispondenze
    # Per ora, restituiamo semplicemente i dati ricevuti
    
    return jsonify({
        "message": "Matches updated",
        "job_id": job_id,
        "matches": matches
    }), 200

@app.route('/api/generate/<job_id>', methods=['POST'])
def generate_montage(job_id):
    # In un'implementazione reale, qui si genererebbe il montaggio finale
    # Per ora, restituiamo dati simulati
    
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{job_id}_montage.mp4")
    
    # Simula la creazione di un file
    with open(output_path, 'w') as f:
        f.write("Placeholder for video montage")
    
    return jsonify({
        "message": "Montage generated",
        "job_id": job_id,
        "output_path": output_path,
        "download_url": f"/api/download/{job_id}"
    }), 200

@app.route('/api/download/<job_id>', methods=['GET'])
def download_montage(job_id):
    # In un'implementazione reale, qui si restituirebbe il file del montaggio
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{job_id}_montage.mp4")
    
    if not os.path.exists(output_path):
        return jsonify({"error": "Montage file not found"}), 404
    
    # In un'implementazione reale, qui si restituirebbe il file
    return jsonify({
        "message": "Download link generated",
        "job_id": job_id,
        "download_url": f"/static/output/{job_id}_montage.mp4"
    }), 200

if __name__ == '__main__':
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

