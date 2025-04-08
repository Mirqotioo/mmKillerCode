import os
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import json

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Classe per ottimizzare le prestazioni della pipeline di elaborazione video.
    Implementa tecniche di parallelizzazione, caching e gestione efficiente della memoria.
    """
    
    def __init__(self, temp_folder, max_workers=None):
        """
        Inizializza l'ottimizzatore di prestazioni.
        
        Args:
            temp_folder: Cartella per i file temporanei e di cache
            max_workers: Numero massimo di worker per l'elaborazione parallela
        """
        self.temp_folder = temp_folder
        self.cache_folder = os.path.join(temp_folder, "cache")
        os.makedirs(self.cache_folder, exist_ok=True)
        
        # Determina il numero ottimale di worker
        if max_workers is None:
            # Usa il 75% dei core disponibili, con un minimo di 2
            self.max_workers = max(2, int(multiprocessing.cpu_count() * 0.75))
        else:
            self.max_workers = max_workers
        
        logger.info(f"Inizializzato ottimizzatore di prestazioni con {self.max_workers} worker")
    
    def get_cache_path(self, job_id, stage):
        """
        Ottiene il percorso del file di cache per un determinato job e stage.
        
        Args:
            job_id: ID del job
            stage: Nome dello stage (es. "segmentation", "captions", "matching")
            
        Returns:
            Percorso del file di cache
        """
        return os.path.join(self.cache_folder, f"{job_id}_{stage}_cache.json")
    
    def cache_exists(self, job_id, stage):
        """
        Verifica se esiste una cache per un determinato job e stage.
        
        Args:
            job_id: ID del job
            stage: Nome dello stage
            
        Returns:
            True se la cache esiste, False altrimenti
        """
        cache_path = self.get_cache_path(job_id, stage)
        return os.path.exists(cache_path)
    
    def save_to_cache(self, job_id, stage, data):
        """
        Salva i dati nella cache.
        
        Args:
            job_id: ID del job
            stage: Nome dello stage
            data: Dati da salvare
            
        Returns:
            Percorso del file di cache
        """
        cache_path = self.get_cache_path(job_id, stage)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
            
            logger.info(f"Dati salvati nella cache per il job {job_id}, stage {stage}")
            return cache_path
        except Exception as e:
            logger.error(f"Errore durante il salvataggio nella cache: {str(e)}")
            return None
    
    def load_from_cache(self, job_id, stage):
        """
        Carica i dati dalla cache.
        
        Args:
            job_id: ID del job
            stage: Nome dello stage
            
        Returns:
            Dati caricati dalla cache, o None se la cache non esiste
        """
        cache_path = self.get_cache_path(job_id, stage)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Dati caricati dalla cache per il job {job_id}, stage {stage}")
            return data
        except Exception as e:
            logger.error(f"Errore durante il caricamento dalla cache: {str(e)}")
            return None
    
    def process_in_parallel(self, items, process_func, *args, **kwargs):
        """
        Elabora una lista di elementi in parallelo.
        
        Args:
            items: Lista di elementi da elaborare
            process_func: Funzione da applicare a ciascun elemento
            *args, **kwargs: Argomenti aggiuntivi da passare alla funzione
            
        Returns:
            Lista dei risultati
        """
        start_time = time.time()
        logger.info(f"Avvio elaborazione parallela di {len(items)} elementi con {self.max_workers} worker")
        
        # Usa ThreadPoolExecutor per operazioni I/O-bound
        # Usa ProcessPoolExecutor per operazioni CPU-bound
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Applica la funzione a ciascun elemento
            results = list(executor.map(lambda item: process_func(item, *args, **kwargs), items))
        
        elapsed_time = time.time() - start_time
        logger.info(f"Elaborazione parallela completata in {elapsed_time:.2f} secondi")
        
        return results
    
    def batch_process(self, items, process_func, batch_size=10, *args, **kwargs):
        """
        Elabora una lista di elementi in batch per ottimizzare l'uso della memoria.
        
        Args:
            items: Lista di elementi da elaborare
            process_func: Funzione da applicare a ciascun batch
            batch_size: Dimensione di ciascun batch
            *args, **kwargs: Argomenti aggiuntivi da passare alla funzione
            
        Returns:
            Lista dei risultati
        """
        start_time = time.time()
        logger.info(f"Avvio elaborazione in batch di {len(items)} elementi con batch di dimensione {batch_size}")
        
        results = []
        
        # Dividi gli elementi in batch
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            
            # Elabora il batch
            batch_results = process_func(batch, *args, **kwargs)
            results.extend(batch_results)
            
            logger.info(f"Batch {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size} completato")
        
        elapsed_time = time.time() - start_time
        logger.info(f"Elaborazione in batch completata in {elapsed_time:.2f} secondi")
        
        return results


class ScalableVideoProcessor:
    """
    Versione scalabile del processore video che utilizza tecniche di ottimizzazione
    per gestire file video di grandi dimensioni e migliorare le prestazioni.
    """
    
    def __init__(self, upload_folder, temp_folder, output_folder, max_workers=None):
        """
        Inizializza il processore video scalabile.
        
        Args:
            upload_folder: Cartella per i file caricati
            temp_folder: Cartella per i file temporanei
            output_folder: Cartella per i file di output
            max_workers: Numero massimo di worker per l'elaborazione parallela
        """
        self.upload_folder = upload_folder
        self.temp_folder = temp_folder
        self.output_folder = output_folder
        
        # Crea le cartelle se non esistono
        for folder in [upload_folder, temp_folder, output_folder]:
            os.makedirs(folder, exist_ok=True)
        
        # Inizializza l'ottimizzatore di prestazioni
        self.optimizer = PerformanceOptimizer(temp_folder, max_workers)
        
        # Importa i moduli necessari
        from video_segmenter import VideoSegmenter
        from ai_models_detailed import SemanticMatchingEngine
        from video_processing import MontageCompiler
        
        # Inizializza i componenti
        self.video_segmenter = VideoSegmenter(temp_folder)
        self.semantic_engine = SemanticMatchingEngine()
        self.montage_compiler = MontageCompiler(temp_folder, output_folder)
    
    def segment_video(self, video_path, job_id):
        """
        Segmenta il video in scene con ottimizzazione delle prestazioni.
        
        Args:
            video_path: Percorso del video
            job_id: ID del job
            
        Returns:
            Lista di scene
        """
        logger.info(f"Segmentazione ottimizzata del video per il job {job_id}")
        
        # Verifica se esiste una cache
        cached_scenes = self.optimizer.load_from_cache(job_id, "segmentation")
        if cached_scenes:
            logger.info(f"Utilizzando scene dalla cache per il job {job_id}")
            return cached_scenes
        
        # In un'implementazione reale, qui utilizzeremmo:
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
        
        # Salva nella cache
        self.optimizer.save_to_cache(job_id, "segmentation", scenes)
        
        return scenes
    
    def generate_captions(self, scenes, job_id):
        """
        Genera didascalie per le scene con elaborazione parallela.
        
        Args:
            scenes: Lista di scene
            job_id: ID del job
            
        Returns:
            Scene con didascalie
        """
        logger.info(f"Generazione ottimizzata di didascalie per il job {job_id}")
        
        # Verifica se esiste una cache
        cached_scenes = self.optimizer.load_from_cache(job_id, "captions")
        if cached_scenes:
            logger.info(f"Utilizzando didascalie dalla cache per il job {job_id}")
            return cached_scenes
        
        # Funzione per generare la didascalia per una singola scena
        def generate_caption_for_scene(scene):
            thumbnail_path = scene.get("thumbnail", "")
            if thumbnail_path and os.path.exists(thumbnail_path):
                scene["caption"] = self.semantic_engine.caption_generator.generate_caption(thumbnail_path)
            else:
                scene["caption"] = "Scena senza thumbnail"
            return scene
        
        # Genera didascalie in parallelo
        scenes_with_captions = self.optimizer.process_in_parallel(scenes, generate_caption_for_scene)
        
        # Salva nella cache
        self.optimizer.save_to_cache(job_id, "captions", scenes_with_captions)
        
        return scenes_with_captions
    
    def match_scenes_to_summary(self, scenes, summary_segments, job_id):
        """
        Abbina le scene alle frasi del riassunto con ottimizzazione delle prestazioni.
        
        Args:
            scenes: Lista di scene con didascalie
            summary_segments: Lista di segmenti del riassunto
            job_id: ID del job
            
        Returns:
            Segmenti del riassunto con scene abbinate
        """
        logger.info(f"Matching semantico ottimizzato per il job {job_id}")
        
        # Verifica se esiste una cache
        cached_segments = self.optimizer.load_from_cache(job_id, "matching")
        if cached_segments:
            logger.info(f"Utilizzando matching dalla cache per il job {job_id}")
            return cached_segments
        
        # Estrai i percorsi dei thumbnail e i testi dei segmenti
        thumbnail_paths = [scene.get("thumbnail", "") for scene in scenes]
        segment_texts = [segment.get("text", "") for segment in summary_segments]
        
        # Calcola le similarità in batch per ottimizzare l'uso della memoria
        batch_size = min(10, len(segment_texts))  # Limita la dimensione del batch
        
        # Funzione per calcolare le similarità per un batch di testi
        def calculate_similarities_for_batch(batch_texts):
            batch_results = []
            for text in batch_texts:
                # Calcola la similarità per ciascuna immagine
                similarities = []
                for path in thumbnail_paths:
                    similarity = self.semantic_engine.clip_model.compute_similarity(path, text)
                    similarities.append(similarity)
                batch_results.append(similarities)
            return batch_results
        
        # Calcola le similarità in batch
        similarity_batches = self.optimizer.batch_process(segment_texts, calculate_similarities_for_batch, batch_size)
        
        # Trova la migliore corrispondenza per ciascun segmento
        for i, segment in enumerate(summary_segments):
            if i < len(similarity_batches):
                similarities = similarity_batches[i]
                best_match_index = similarities.index(max(similarities))
                if best_match_index < len(scenes):
                    segment["matchedSceneId"] = scenes[best_match_index]["id"]
                elif len(scenes) > 0:
                    segment["matchedSceneId"] = scenes[0]["id"]
        
        # Salva nella cache
        self.optimizer.save_to_cache(job_id, "matching", summary_segments)
        
        return summary_segments
    
    def process_video(self, video_path, summary, job_id):
        """
        Elabora un video e un riassunto per creare un montaggio con ottimizzazione delle prestazioni.
        
        Args:
            video_path: Percorso del video
            summary: Testo del riassunto
            job_id: ID del job
            
        Returns:
            Risultati dell'elaborazione
        """
        logger.info(f"Avvio dell'elaborazione ottimizzata del video per il job {job_id}")
        
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
            scenes = self.segment_video(video_path, job_id)
            
            # Genera didascalie per le scene
            scenes = self.generate_captions(scenes, job_id)
            
            # Abbina le scene alle frasi del riassunto
            summary_segments = self.match_scenes_to_summary(scenes, summary_segments, job_id)
            
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
            logger.error(f"Errore durante l'elaborazione ottimizzata del video: {str(e)}")
            return {"error": str(e)}
    
    def generate_montage(self, job_id):
        """
        Genera il montaggio finale per un job con ottimizzazione delle prestazioni.
        
        Args:
            job_id: ID del job
            
        Returns:
            Percorso del montaggio finale
        """
        logger.info(f"Generazione ottimizzata del montaggio per il job {job_id}")
        
        try:
            # Carica i risultati
            results_path = os.path.join(self.temp_folder, f"{job_id}_results.json")
            
            if not os.path.exists(
(Content truncated due to size limit. Use line ranges to read in chunks)