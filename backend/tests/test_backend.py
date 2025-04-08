import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Aggiungi la directory del backend al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from video_segmenter import VideoSegmenter
from ai_models_detailed import CaptionGeneratorDetailed, CLIPModelIntegration, SemanticMatchingEngine
from video_processing import MontageCompiler, VideoProcessingPipeline

class TestVideoSegmenter(unittest.TestCase):
    def setUp(self):
        self.temp_folder = "/tmp/test_movie_montage"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.segmenter = VideoSegmenter(self.temp_folder)
    
    @patch('scenedetect.VideoManager')
    @patch('scenedetect.SceneManager')
    @patch('scenedetect.StatsManager')
    @patch('scenedetect.scene_manager.save_images')
    def test_detect_scenes(self, mock_save_images, mock_stats_manager, mock_scene_manager, mock_video_manager):
        # Configura i mock
        mock_video_instance = MagicMock()
        mock_video_manager.return_value = mock_video_instance
        
        mock_stats_instance = MagicMock()
        mock_stats_manager.return_value = mock_stats_instance
        
        mock_scene_instance = MagicMock()
        mock_scene_manager.return_value = mock_scene_instance
        
        # Configura il mock per restituire una lista di scene
        mock_scene = MagicMock()
        mock_scene[0].get_seconds.return_value = 0
        mock_scene[1].get_seconds.return_value = 10
        mock_scene_instance.get_scene_list.return_value = [mock_scene]
        
        # Esegui il test
        scenes = self.segmenter.detect_scenes("test_video.mp4", "test_job", threshold=30.0)
        
        # Verifica i risultati
        self.assertEqual(len(scenes), 1)
        self.assertEqual(scenes[0]["start_time"], 0)
        self.assertEqual(scenes[0]["end_time"], 10)
        self.assertEqual(scenes[0]["duration"], 10)
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

class TestCaptionGenerator(unittest.TestCase):
    def setUp(self):
        self.temp_folder = "/tmp/test_movie_montage"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.caption_generator = CaptionGeneratorDetailed()
    
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('transformers.AutoModelForSeq2SeqLM.from_pretrained')
    def test_load_model(self, mock_model, mock_tokenizer):
        # Configura i mock
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Esegui il test
        self.caption_generator.load_model()
        
        # Verifica che i modelli siano stati caricati
        self.assertIsNotNone(self.caption_generator.model)
        self.assertIsNotNone(self.caption_generator.tokenizer)
    
    def test_generate_caption(self):
        # Crea un'immagine di test
        test_image_path = os.path.join(self.temp_folder, "1.jpg")
        with open(test_image_path, 'w') as f:
            f.write("test image")
        
        # Esegui il test
        caption = self.caption_generator.generate_caption(test_image_path)
        
        # Verifica che sia stata generata una didascalia
        self.assertIsNotNone(caption)
        self.assertIsInstance(caption, str)
        self.assertTrue(len(caption) > 0)
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

class TestCLIPIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_folder = "/tmp/test_movie_montage"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.clip_model = CLIPModelIntegration()
    
    @patch('clip.load')
    def test_load_model(self, mock_clip_load):
        # Configura i mock
        mock_model = MagicMock()
        mock_preprocess = MagicMock()
        mock_clip_load.return_value = (mock_model, mock_preprocess)
        
        # Esegui il test
        self.clip_model.load_model()
        
        # Verifica che il modello sia stato caricato
        self.assertIsNotNone(self.clip_model.model)
        self.assertIsNotNone(self.clip_model.preprocess)
    
    def test_compute_similarity(self):
        # Crea un'immagine di test
        test_image_path = os.path.join(self.temp_folder, "1.jpg")
        with open(test_image_path, 'w') as f:
            f.write("test image")
        
        # Esegui il test
        similarity = self.clip_model.compute_similarity(test_image_path, "Un uomo cammina lungo una strada")
        
        # Verifica che sia stato calcolato un punteggio di similarità
        self.assertIsNotNone(similarity)
        self.assertIsInstance(similarity, float)
        self.assertTrue(0 <= similarity <= 1)
    
    def test_find_best_match(self):
        # Crea immagini di test
        image_paths = []
        for i in range(3):
            path = os.path.join(self.temp_folder, f"{i+1}.jpg")
            with open(path, 'w') as f:
                f.write(f"test image {i+1}")
            image_paths.append(path)
        
        texts = [
            "Un uomo cammina lungo una strada",
            "Una donna guarda fuori dalla finestra",
            "Due persone conversano in un caffè"
        ]
        
        # Esegui il test
        similarity_matrix, best_matches = self.clip_model.find_best_match(image_paths, texts)
        
        # Verifica i risultati
        self.assertEqual(similarity_matrix.shape, (3, 3))
        self.assertEqual(len(best_matches), 3)
        for match in best_matches:
            self.assertTrue(0 <= match < 3)
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

class TestSemanticMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.temp_folder = "/tmp/test_movie_montage"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.matching_engine = SemanticMatchingEngine()
    
    def test_process_scenes(self):
        # Crea scene di test
        scenes = []
        for i in range(3):
            thumbnail_path = os.path.join(self.temp_folder, f"{i+1}.jpg")
            with open(thumbnail_path, 'w') as f:
                f.write(f"test image {i+1}")
            
            scenes.append({
                "id": i+1,
                "start_time": i*10,
                "end_time": (i+1)*10,
                "thumbnail": thumbnail_path
            })
        
        # Esegui il test
        processed_scenes = self.matching_engine.process_scenes(scenes, "test_job")
        
        # Verifica i risultati
        self.assertEqual(len(processed_scenes), 3)
        for scene in processed_scenes:
            self.assertIn("caption", scene)
            self.assertTrue(len(scene["caption"]) > 0)
    
    def test_match_scenes_to_summary(self):
        # Crea scene di test
        scenes = []
        for i in range(3):
            thumbnail_path = os.path.join(self.temp_folder, f"{i+1}.jpg")
            with open(thumbnail_path, 'w') as f:
                f.write(f"test image {i+1}")
            
            scenes.append({
                "id": i+1,
                "start_time": i*10,
                "end_time": (i+1)*10,
                "thumbnail": thumbnail_path,
                "caption": f"Didascalia per la scena {i+1}"
            })
        
        # Crea segmenti del riassunto di test
        summary_segments = [
            {"id": 1, "text": "Prima frase del riassunto."},
            {"id": 2, "text": "Seconda frase del riassunto."},
            {"id": 3, "text": "Terza frase del riassunto."}
        ]
        
        # Esegui il test
        matched_segments = self.matching_engine.match_scenes_to_summary(scenes, summary_segments, "test_job")
        
        # Verifica i risultati
        self.assertEqual(len(matched_segments), 3)
        for segment in matched_segments:
            self.assertIn("matchedSceneId", segment)
            self.assertTrue(1 <= segment["matchedSceneId"] <= 3)
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

class TestMontageCompiler(unittest.TestCase):
    def setUp(self):
        self.temp_folder = "/tmp/test_movie_montage/temp"
        self.output_folder = "/tmp/test_movie_montage/output"
        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        self.montage_compiler = MontageCompiler(self.temp_folder, self.output_folder)
    
    @patch('moviepy.editor.VideoFileClip')
    def test_extract_scene_clips(self, mock_video_clip):
        # Configura i mock
        mock_clip_instance = MagicMock()
        mock_video_clip.return_value = mock_clip_instance
        
        mock_subclip = MagicMock()
        mock_clip_instance.subclip.return_value = mock_subclip
        
        # Crea scene di test
        scenes = [
            {"id": 1, "start_time": 0, "end_time": 10},
            {"id": 2, "start_time": 15, "end_time": 25},
            {"id": 3, "start_time": 30, "end_time": 40}
        ]
        
        # Esegui il test
        clips = self.montage_compiler.extract_scene_clips("test_video.mp4", scenes, [1, 3])
        
        # Verifica i risultati
        self.assertEqual(len(clips), 2)
        mock_clip_instance.subclip.assert_any_call(0, 10)
        mock_clip_instance.subclip.assert_any_call(30, 40)
    
    def test_compile_montage(self):
        # Crea scene di test
        scenes = [
            {"id": 1, "start_time": 0, "end_time": 10, "caption": "Didascalia 1"},
            {"id": 2, "start_time": 15, "end_time": 25, "caption": "Didascalia 2"},
            {"id": 3, "start_time": 30, "end_time": 40, "caption": "Didascalia 3"}
        ]
        
        # Crea segmenti del riassunto di test
        summary_segments = [
            {"id": 1, "text": "Prima frase.", "matchedSceneId": 2},
            {"id": 2, "text": "Seconda frase.", "matchedSceneId": 1},
            {"id": 3, "text": "Terza frase.", "matchedSceneId": 3}
        ]
        
        # Esegui il test
        output_path = self.montage_compiler.compile_montage("test_video.mp4", scenes, summary_segments, "test_job")
        
        # Verifica i risultati
        self.assertTrue(os.path.exists(output_path))
        
        # Verifica che sia stato creato anche il file di descrizione
        description_path = os.path.join(self.output_folder, "test_job_montage_description.txt")
        self.assertTrue(os.path.exists(description_path))
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists("/tmp/test_movie_montage"):
            shutil.rmtree("/tmp/test_movie_montage")

class TestVideoProcessingPipeline(unittest.TestCase):
    def setUp(self):
        self.upload_folder = "/tmp/test_movie_montage/uploads"
        self.temp_folder = "/tmp/test_movie_montage/temp"
        self.output_folder = "/tmp/test_movie_montage/output"
        
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Crea un file video di test
        self.test_video_path = os.path.join(self.upload_folder, "test_job.mp4")
        with open(self.test_video_path, 'w') as f:
            f.write("test video content")
        
        self.pipeline = VideoProcessingPipeline(self.upload_folder, self.temp_folder, self.output_folder)
    
    def test_process_video(self):
        # Esegui il test
        results = self.pipeline.process_video(self.test_video_path, "Questo è un riassunto di test.", "test_job")
        
        # Verifica i risultati
        self.assertIn("job_id", results)
        self.assertIn("scenes", results)
        self.assertIn("summary_segments", results)
        
        # Verifica che sia stato creato il file dei risultati
        results_path = os.path.join(self.temp_folder, "test_job_results.json")
        self.assertTrue(os.path.exists(results_path))
    
    def test_generate_montage(self):
        # Prima elabora il video per creare i risultati
        self.pipeline.process_video(self.test_video_path, "Questo è un riassunto di test.", "test_job")
        
        # Esegui il test
        output_path = self.pipeline.generate_montage("test_job")
        
        # Verifica i risultati
        self.assertIsNotNone(output_path)
        self.assertTrue(os.path.exists(output_path))
    
    def tearDown(self):
        # Pulisci i file temporanei
        import shutil
        if os.path.exists("/tmp/test_movie_montage"):
            shutil.rmtree("/tmp/test_movie_montage")

if __name__ == '__main__':
    unittest.main()
