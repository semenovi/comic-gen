import os
import json
import uuid
import logging
from datetime import datetime
from utils.sd_wrapper import StableDiffusionWrapper

logger = logging.getLogger(__name__)

class SceneGenerator:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.metadata_file = os.path.join(output_folder, 'scenes_metadata.json')
        self.sd = StableDiffusionWrapper()
        self.characters_folder = os.path.dirname(output_folder) + '/characters'
        self.characters_metadata = os.path.join(self.characters_folder, 'characters_metadata.json')
        
        # Создаем папку вывода, если не существует
        os.makedirs(output_folder, exist_ok=True)
        
        # Загружаем существующие метаданные
        self.load_metadata()
    
    def load_metadata(self):
        """Загружает метаданные о сценах из файла"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.scenes = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Ошибка при чтении файла метаданных: {self.metadata_file}")
                self.scenes = {}
        else:
            self.scenes = {}
        
        # Загружаем метаданные о персонажах
        if os.path.exists(self.characters_metadata):
            try:
                with open(self.characters_metadata, 'r', encoding='utf-8') as f:
                    self.characters = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Ошибка при чтении файла метаданных персонажей: {self.characters_metadata}")
                self.characters = {}
        else:
            self.characters = {}
    
    def save_metadata(self):
        """Сохраняет метаданные о сценах в файл"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.scenes, f, ensure_ascii=False, indent=2)
    
    def generate(self, character_id, plot_description):
        """
        Генерирует сюжетную сцену с указанным персонажем и описанием сюжета
        """
        # Проверяем, существует ли персонаж
        if character_id not in self.characters:
            logger.error(f"Персонаж с ID {character_id} не найден")
            return None
        
        character = self.characters[character_id]
        character_image = os.path.join(self.characters_folder, f"{character_id}.png")
        
        if not os.path.exists(character_image):
            logger.error(f"Изображение персонажа не найдено: {character_image}")
            return None
        
        # Генерируем уникальный ID для сцены
        scene_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Формируем промпт для генерации
        character_description = character.get('description', '')
        prompt = f"{character_description} in {plot_description}, anime style, high quality, detailed"
        
        # Генерируем сцену на основе персонажа и описания сюжета
        output_path = os.path.join(self.output_folder, f"{scene_id}.png")
        success = self.sd.generate_scene(
            prompt=prompt,
            character_image=character_image,
            output_path=output_path,
            negative_prompt="bad anatomy, bad proportions, blurry, low quality"
        )
        
        if not success:
            logger.error(f"Не удалось сгенерировать сцену с персонажем {character_id} и сюжетом: {plot_description}")
            return None
        
        # Создаем метаданные сцены
        scene = {
            "id": scene_id,
            "character_id": character_id,
            "plot_description": plot_description,
            "created_at": timestamp,
            "image_url": f"/uploads/scenes/{scene_id}.png"
        }
        
        # Сохраняем метаданные
        self.scenes[scene_id] = scene
        self.save_metadata()
        
        return scene