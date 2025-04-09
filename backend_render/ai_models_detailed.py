import os
import logging
import numpy as np
from PIL import Image
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import clip

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptionGeneratorDetailed:
    """
    Classe per la generazione di didascalie dettagliate per le scene video
    utilizzando un modello di visione-linguaggio pre-addestrato.
    """
    
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Inizializza il generatore di didascalie.
        
        Args:
            model_name: Nome del modello Hugging Face da utilizzare
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Utilizzo del dispositivo: {self.device}")
    
    def load_model(self):
        """
        Carica il modello di generazione delle didascalie.
        """
        try:
            logger.info(f"Caricamento del modello {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
            logger.info("Modello caricato con successo")
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello: {str(e)}")
            raise
    
    def generate_caption(self, image_path):
        """
        Genera una didascalia per un'immagine.
        
        Args:
            image_path: Percorso dell'immagine
            
        Returns:
            Didascalia generata
        """
        if self.model is None:
            self.load_model()
        
        try:
            # In un'implementazione reale, qui utilizzeremmo un modello di visione-linguaggio
            # per generare una didascalia basata sull'immagine
            # Per ora, restituiamo una didascalia predefinita basata sul nome del file
            
            # Estrai il nome del file senza estensione
            filename = os.path.basename(image_path)
            scene_number = int(os.path.splitext(filename)[0])
            
            # Didascalie predefinite per la simulazione
            captions = [
                "Un uomo cammina lungo una strada deserta al tramonto, con lo sguardo pensieroso",
                "Una donna guarda fuori dalla finestra con espressione preoccupata, tenendo un telefono in mano",
                "Due persone conversano animatamente in un caffè affollato, gesticolando con enfasi",
                "Un'auto sportiva rossa sfreccia lungo un'autostrada di notte, con i fari che illuminano la strada",
                "Un telefono squilla insistentemente in una stanza vuota, mentre la luce del sole filtra dalle tende",
                "Un gruppo di amici festeggia con entusiasmo a una festa in giardino, alzando i bicchieri in un brindisi",
                "Un bambino gioca spensierato in un parco soleggiato, lanciando un aquilone colorato nel cielo",
                "Una coppia cammina mano nella mano sulla spiaggia al tramonto, lasciando impronte sulla sabbia",
                "Un uomo in abito formale entra con determinazione in un imponente edificio d'ufficio in vetro e acciaio",
                "Una donna legge assorta un libro in una biblioteca silenziosa, circondata da scaffali pieni di volumi"
            ]
            
            # Seleziona una didascalia in base al numero della scena
            caption_index = (scene_number - 1) % len(captions)
            return captions[caption_index]
            
        except Exception as e:
            logger.error(f"Errore durante la generazione della didascalia: {str(e)}")
            return "Scena non identificata"


class CLIPModelIntegration:
    """
    Classe per l'integrazione del modello CLIP per il matching semantico
    tra testo e immagini.
    """
    
    def __init__(self, model_name="ViT-B/32"):
        """
        Inizializza l'integrazione CLIP.
        
        Args:
            model_name: Nome del modello CLIP da utilizzare
        """
        self.model_name = model_name
        self.model = None
        self.preprocess = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Utilizzo del dispositivo: {self.device}")
    
    def load_model(self):
        """
        Carica il modello CLIP.
        """
        try:
            logger.info(f"Caricamento del modello CLIP {self.model_name}...")
            self.model, self.preprocess = clip.load(self.model_name, device=self.device)
            logger.info("Modello CLIP caricato con successo")
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello CLIP: {str(e)}")
            raise
    
    def compute_similarity(self, image_path, text):
        """
        Calcola la similarità semantica tra un'immagine e un testo.
        
        Args:
            image_path: Percorso dell'immagine
            text: Testo da confrontare
            
        Returns:
            Punteggio di similarità
        """
        if self.model is None:
            self.load_model()
        
        try:
            # In un'implementazione reale, qui utilizzeremmo CLIP per calcolare
            # la similarità tra l'immagine e il testo
            # Per ora, simuliamo il calcolo della similarità
            
            # Estrai il numero della scena dal nome del file
            filename = os.path.basename(image_path)
            scene_number = int(os.path.splitext(filename)[0])
            
            # Calcola una similarità simulata basata sulla lunghezza del testo e sul numero della scena
            text_length = len(text)
            similarity = 0.5 + 0.3 * np.sin(scene_number * 0.5 + text_length * 0.01)
            
            # Limita il valore tra 0 e 1
            similarity = max(0, min(1, similarity))
            
            return similarity
            
        except Exception as e:
            logger.error(f"Errore durante il calcolo della similarità: {str(e)}")
            return 0.0
    
    def find_best_match(self, image_paths, texts):
        """
        Trova la migliore corrispondenza tra un insieme di immagini e testi.
        
        Args:
            image_paths: Lista di percorsi delle immagini
            texts: Lista di testi
            
        Returns:
            Matrice di similarità e indici delle migliori corrispondenze
        """
        if self.model is None:
            self.load_model()
        
        try:
            # Crea una matrice di similarità
            similarity_matrix = np.zeros((len(texts), len(image_paths)))
            
            # Calcola la similarità per ogni coppia immagine-testo
            for i, text in enumerate(texts):
                for j, image_path in enumerate(image_paths):
                    similarity_matrix[i, j] = self.compute_similarity(image_path, text)
            
            # Trova la migliore corrispondenza per ogni testo
            best_matches = np.argmax(similarity_matrix, axis=1)
            
            return similarity_matrix, best_matches
            
        except Exception as e:
            logger.error(f"Errore durante la ricerca delle migliori corrispondenze: {str(e)}")
            # Restituisci una corrispondenza 1:1 come fallback
            return np.zeros((len(texts), len(image_paths))), list(range(min(len(texts), len(image_paths))))


class SemanticMatchingEngine:
    """
    Motore di matching semantico che combina la generazione di didascalie
    e l'embedding cross-modale per associare scene a frasi del riassunto.
    """
    
    def __init__(self):
        """
        Inizializza il motore di matching semantico.
        """
        self.caption_generator = CaptionGeneratorDetailed()
        self.clip_model = CLIPModelIntegration()
    
    def process_scenes(self, scenes, job_id):
        """
        Elabora le scene generando didascalie.
        
        Args:
            scenes: Lista di scene con percorsi dei thumbnail
            job_id: ID del job
            
        Returns:
            Scene con didascalie
        """
        logger.info(f"Elaborazione di {len(scenes)} scene per il job {job_id}")
        
        for scene in scenes:
            # Genera una didascalia per la scena
            thumbnail_path = scene.get("thumbnail", "")
            if thumbnail_path and os.path.exists(thumbnail_path):
                scene["caption"] = self.caption_generator.generate_caption(thumbnail_path)
            else:
                scene["caption"] = "Scena senza thumbnail"
        
        return scenes
    
    def match_scenes_to_summary(self, scenes, summary_segments, job_id):
        """
        Abbina le scene alle frasi del riassunto.
        
        Args:
            scenes: Lista di scene con didascalie
            summary_segments: Lista di segmenti del riassunto
            job_id: ID del job
            
        Returns:
            Segmenti del riassunto con scene abbinate
        """
        logger.info(f"Abbinamento di {len(scenes)} scene a {len(summary_segments)} segmenti per il job {job_id}")
        
        try:
            # Estrai i percorsi dei thumbnail e i testi dei segmenti
            thumbnail_paths = [scene.get("thumbnail", "") for scene in scenes]
            segment_texts = [segment.get("text", "") for segment in summary_segments]
            
            # Trova le migliori corrispondenze
            _, best_matches = self.clip_model.find_best_match(thumbnail_paths, segment_texts)
            
            # Assegna le scene ai segmenti
            for i, segment in enumerate(summary_segments):
                if i < len(best_matches) and best_matches[i] < len(scenes):
                    segment["matchedSceneId"] = scenes[best_matches[i]]["id"]
                elif len(scenes) > 0:
                    # Fallback alla prima scena
                    segment["matchedSceneId"] = scenes[0]["id"]
            
            return summary_segments
            
        except Exception as e:
            logger.error(f"Errore durante l'abbinamento delle scene: {str(e)}")
            
            # Fallback: associa ogni segmento alla scena con lo stesso indice, se disponibile
            for i, segment in enumerate(summary_segments):
                if i < len(scenes):
                    segment["matchedSceneId"] = scenes[i]["id"]
                elif len(scenes) > 0:
                    segment["matchedSceneId"] = scenes[0]["id"]
            
            return summary_segments
