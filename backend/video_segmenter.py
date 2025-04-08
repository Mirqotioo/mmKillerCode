import os
import logging
from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSegmenter:
    def __init__(self, temp_folder):
        self.temp_folder = temp_folder
        
    def detect_scenes(self, video_path, job_id, threshold=30.0):
        """
        Segmenta il video in scene utilizzando PySceneDetect.
        
        Args:
            video_path: Percorso del file video
            job_id: ID del job per identificare i file temporanei
            threshold: Soglia di rilevamento delle scene (default: 30.0)
            
        Returns:
            List di scene rilevate con timestamp di inizio e fine
        """
        logger.info(f"Iniziando la segmentazione del video: {video_path}")
        
        # Crea la directory per i thumbnail se non esiste
        thumbnails_dir = os.path.join(self.temp_folder, f"{job_id}_thumbnails")
        os.makedirs(thumbnails_dir, exist_ok=True)
        
        try:
            # Crea il video manager e carica il video
            video_manager = VideoManager([video_path])
            stats_manager = StatsManager()
            scene_manager = SceneManager(stats_manager)
            
            # Aggiungi il detector di contenuto
            scene_manager.add_detector(ContentDetector(threshold=threshold))
            
            # Imposta il downscale per migliorare le prestazioni
            video_manager.set_downscale_factor()
            
            # Inizia il processo di rilevamento
            video_manager.start()
            scene_manager.detect_scenes(frame_source=video_manager)
            
            # Ottieni l'elenco delle scene
            scene_list = scene_manager.get_scene_list()
            
            # Salva i thumbnail per ogni scena
            save_images(
                scene_list,
                video_manager,
                num_images=1,
                output_dir=thumbnails_dir,
                image_name_template='$SCENE_NUMBER',
                format='jpg'
            )
            
            # Converti le scene in un formato più utile
            scenes = []
            for i, scene in enumerate(scene_list):
                start_time = scene[0].get_seconds()
                end_time = scene[1].get_seconds()
                thumbnail_path = os.path.join(thumbnails_dir, f"{i+1:03d}.jpg")
                
                scenes.append({
                    "id": i + 1,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                    "thumbnail": thumbnail_path
                })
            
            logger.info(f"Segmentazione completata. Rilevate {len(scenes)} scene.")
            return scenes
            
        except Exception as e:
            logger.error(f"Errore durante la segmentazione del video: {str(e)}")
            raise
        finally:
            video_manager.release()
