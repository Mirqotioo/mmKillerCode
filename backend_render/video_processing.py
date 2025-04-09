import os
import logging
import numpy as np
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MontageCompiler:
    """
    Classe per la compilazione del montaggio video finale basato sulle scene selezionate
    e sull'ordine definito dal riassunto.
    """
    
    def __init__(self, temp_folder, output_folder):
        """
        Inizializza il compilatore di montaggio.
        
        Args:
            temp_folder: Cartella per i file temporanei
            output_folder: Cartella per i file di output
        """
        self.temp_folder = temp_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def extract_scene_clips(self, video_path, scenes, selected_scene_ids):
        """
        Estrae i clip video per le scene selezionate.
        
        Args:
            video_path: Percorso del video originale
            scenes: Lista di tutte le scene con timestamp
            selected_scene_ids: Lista degli ID delle scene selezionate
            
        Returns:
            Lista di clip video
        """
        logger.info(f"Estrazione di {len(selected_scene_ids)} clip da {video_path}")
        
        try:
            # Carica il video
            video = VideoFileClip(video_path)
            
            # Estrai i clip per le scene selezionate
            clips = []
            for scene_id in selected_scene_ids:
                # Trova la scena corrispondente
                scene = next((s for s in scenes if s["id"] == scene_id), None)
                
                if scene:
                    start_time = scene["start_time"]
                    end_time = scene["end_time"]
                    
                    # Estrai il clip
                    clip = video.subclip(start_time, end_time)
                    clips.append(clip)
                else:
                    logger.warning(f"Scena con ID {scene_id} non trovata")
            
            return clips
            
        except Exception as e:
            logger.error(f"Errore durante l'estrazione dei clip: {str(e)}")
            return []
    
    def compile_montage(self, video_path, scenes, summary_segments, job_id):
        """
        Compila il montaggio finale basato sulle scene selezionate e sull'ordine del riassunto.
        
        Args:
            video_path: Percorso del video originale
            scenes: Lista di tutte le scene con timestamp
            summary_segments: Lista dei segmenti del riassunto con scene abbinate
            job_id: ID del job
            
        Returns:
            Percorso del montaggio finale
        """
        logger.info(f"Compilazione del montaggio per il job {job_id}")
        
        try:
            # Ordina i segmenti del riassunto per ID
            sorted_segments = sorted(summary_segments, key=lambda x: x["id"])
            
            # Estrai gli ID delle scene selezionate nell'ordine del riassunto
            selected_scene_ids = [segment["matchedSceneId"] for segment in sorted_segments]
            
            # In un'implementazione reale, qui estrarremmo i clip e creeremmo il montaggio
            # Per ora, creiamo un file di testo che descrive il montaggio
            
            output_path = os.path.join(self.output_folder, f"{job_id}_montage.mp4")
            
            # Crea un file di testo che descrive il montaggio
            description_path = os.path.join(self.output_folder, f"{job_id}_montage_description.txt")
            with open(description_path, 'w') as f:
                f.write(f"Montaggio video per il job {job_id}\n\n")
                f.write("Sequenza di scene:\n")
                
                for i, segment in enumerate(sorted_segments):
                    scene_id = segment["matchedSceneId"]
                    scene = next((s for s in scenes if s["id"] == scene_id), None)
                    
                    if scene:
                        f.write(f"Segmento {i+1}: {segment['text']}\n")
                        f.write(f"  Scena: {scene['id']}, {scene['start_time']:.2f}s - {scene['end_time']:.2f}s\n")
                        f.write(f"  Didascalia: {scene.get('caption', 'Nessuna didascalia')}\n\n")
            
            # Simula la creazione del file video
            with open(output_path, 'w') as f:
                f.write("Placeholder per il montaggio video")
            
            logger.info(f"Montaggio compilato: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Errore durante la compilazione del montaggio: {str(e)}")
            
            # Crea un file di errore
            error_path = os.path.join(self.output_folder, f"{job_id}_error.txt")
            with open(error_path, 'w') as f:
                f.write(f"Errore durante la compilazione del montaggio: {str(e)}")
            
            return error_path


class VideoProcessingPipeline:
    """
    Pipeline completa per l'elaborazione video, che integra tutti i moduli AI
    e di elaborazione video.
    """
    
    def __init__(self, upload_folder, temp_folder, output_folder):
        """
        Inizializza la pipeline di elaborazione video.
        
        Args:
            upload_folder: Cartella per i file caricati
            temp_folder: Cartella per i file temporanei
            output_folder: Cartella per i file di output
        """
        self.upload_folder = upload_folder
        self.temp_folder = temp_folder
        self.output_folder = output_folder
        
        # Importa i moduli necessari
        from video_segmenter import VideoSegmenter
        from ai_models_detailed import SemanticMatchingEngine
        
        # Inizializza i componenti
        self.video_segmenter = VideoSegmenter(temp_folder)
        self.semantic_engine = SemanticMatchingEngine()
        self.montage_compiler = MontageCompiler(temp_folder, output_folder)
    
    def process_video(self, video_path, summary, job_id):
        """
        Elabora un video e un riassunto per creare un montaggio.
        
        Args:
            video_path: Percorso del video
            summary: Testo del riassunto
            job_id: ID del job
            
        Returns:
            Risultati dell'elaborazione
        """
        logger.info(f"Avvio dell'elaborazione del video per il job {job_id}")
        
        try:
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
            
            # Segmenta il video in scene
            # In un'implementazione reale, utilizzeremmo:
            # scenes = self.video_segmenter.detect_scenes(video_path, job_id)
            # Per ora, utilizziamo dati simulati
            scenes = [
                {"id": 1, "start_time": 0, "end_time": 10, "thumbnail": os.path.join(self.temp_folder, "1.jpg")},
                {"id": 2, "start_time": 15, "end_time": 25, "thumbnail": os.path.join(self.temp_folder, "2.jpg")},
                {"id": 3, "start_time": 30, "end_time": 40, "thumbnail": os.path.join(self.temp_folder, "3.jpg")},
                {"id": 4, "start_time": 45, "end_time": 55, "thumbnail": os.path.join(self.temp_folder, "4.jpg")},
                {"id": 5, "start_time": 60, "end_time": 70, "thumbnail": os.path.join(self.temp_folder, "5.jpg")},
                {"id": 6, "start_time": 75, "end_time": 85, "thumbnail": os.path.join(self.temp_folder, "6.jpg")}
            ]
            
            # Crea i file di thumbnail simulati
            for scene in scenes:
                with open(scene["thumbnail"], 'w') as f:
                    f.write(f"Placeholder per thumbnail della scena {scene['id']}")
            
            # Elabora le scene con il motore semantico
            scenes = self.semantic_engine.process_scenes(scenes, job_id)
            
            # Abbina le scene alle frasi del riassunto
            summary_segments = self.semantic_engine.match_scenes_to_summary(scenes, summary_segments, job_id)
            
            # Salva i risultati
            results = {
                "job_id": job_id,
                "scenes": scenes,
                "summary_segments": summary_segments
            }
            
            results_path = os.path.join(self.temp_folder, f"{job_id}_results.json")
            with open(results_path, 'w') as f:
                json.dump(results, f)
            
            return results
            
        except Exception as e:
            logger.error(f"Errore durante l'elaborazione del video: {str(e)}")
            return {"error": str(e)}
    
    def generate_montage(self, job_id):
        """
        Genera il montaggio finale per un job.
        
        Args:
            job_id: ID del job
            
        Returns:
            Percorso del montaggio finale
        """
        logger.info(f"Generazione del montaggio per il job {job_id}")
        
        try:
            # Carica i risultati
            results_path = os.path.join(self.temp_folder, f"{job_id}_results.json")
            
            if not os.path.exists(results_path):
                raise FileNotFoundError(f"Risultati non trovati per il job {job_id}")
            
            with open(results_path, 'r') as f:
                results = json.load(f)
            
            # Recupera il percorso del video
            video_path = os.path.join(self.upload_folder, f"{job_id}.mp4")
            
            if not os.path.exists(video_path):
                # Prova altre estensioni
                for ext in ['mov', 'avi', 'mkv']:
                    alt_path = os.path.join(self.upload_folder, f"{job_id}.{ext}")
                    if os.path.exists(alt_path):
                        video_path = alt_path
                        break
            
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video non trovato per il job {job_id}")
            
            # Compila il montaggio
            output_path = self.montage_compiler.compile_montage(
                video_path, 
                results['scenes'], 
                results['summary_segments'], 
                job_id
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Errore durante la generazione del montaggio: {str(e)}")
            return None
