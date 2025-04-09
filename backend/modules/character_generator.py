import os
import json
import uuid
import shutil
import logging
from datetime import datetime
from utils.sd_wrapper import StableDiffusionWrapper

logger = logging.getLogger(__name__)

class CharacterGenerator:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.metadata_file = os.path.join(output_folder, 'characters_metadata.json')
        self.sd = StableDiffusionWrapper()
        
        # Создаем папку вывода, если не существует
        os.makedirs(output_folder, exist_ok=True)
        
        # Загружаем существующие метаданные
        self.load_metadata()
    
    def load_metadata(self):
        """Загружает метаданные о персонажах из файла"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.characters = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Ошибка при чтении файла метаданных: {self.metadata_file}")
                self.characters = {}
        else:
            self.characters = {}
    
    def save_metadata(self):
        """Сохраняет метаданные о персонажах в файл"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.characters, f, ensure_ascii=False, indent=2)
    
    def get_all_characters(self):
        """Возвращает список всех персонажей"""
        return list(self.characters.values())
    
    def get_character(self, character_id):
        """Получает персонажа по ID"""
        return self.characters.get(character_id)
    
    def generate(self, description, reference_image=None):
        """
        Генерирует персонажа на основе текстового описания
        и опционального референсного изображения
        """
        # Генерируем уникальный ID для персонажа
        character_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Формируем промпт для генерации
        base_prompt = f"anime character, full body, white background, high quality, detailed"
        prompt = f"{description}, {base_prompt}"
        
        # Если есть референсное изображение, используем его
        if reference_image:
            image_path = self._save_character_image(character_id, reference_image, "reference")
            # Генерируем персонажа на основе референса и описания
            output_path = os.path.join(self.output_folder, f"{character_id}.png")
            success = self.sd.generate_with_reference(
                prompt=prompt,
                reference_image=reference_image,
                output_path=output_path,
                negative_prompt="bad anatomy, bad proportions, blurry, low quality"
            )
        else:
            # Генерируем персонажа только на основе описания
            output_path = os.path.join(self.output_folder, f"{character_id}.png")
            success = self.sd.generate(
                prompt=prompt,
                output_path=output_path,
                negative_prompt="bad anatomy, bad proportions, blurry, low quality"
            )
        
        if not success:
            logger.error(f"Не удалось сгенерировать персонажа с описанием: {description}")
            return None
        
        # Создаем метаданные персонажа
        character = {
            "id": character_id,
            "description": description,
            "created_at": timestamp,
            "updated_at": timestamp,
            "image_url": f"/uploads/characters/{character_id}.png",
            "references": [f"/uploads/characters/{character_id}_reference.png"] if reference_image else []
        }
        
        # Сохраняем метаданные
        self.characters[character_id] = character
        self.save_metadata()
        
        return character
    
    def update(self, character_id, data, new_image=None):
        """
        Обновляет данные персонажа и/или заменяет изображение
        """
        if character_id not in self.characters:
            return None
        
        character = self.characters[character_id]
        
        # Обновляем описание, если оно предоставлено
        if 'description' in data:
            character['description'] = data['description']
        
        # Обновляем изображение, если оно предоставлено
        if new_image:
            # Сохраняем новое изображение
            self._save_character_image(character_id, new_image, "main")
        
        # Обновляем временную метку
        character['updated_at'] = datetime.now().isoformat()
        self.save_metadata()
        
        return character
    
    def delete(self, character_id):
        """
        Удаляет персонажа и все его изображения
        """
        if character_id not in self.characters:
            return False
        
        # Удаляем изображения персонажа
        main_image = os.path.join(self.output_folder, f"{character_id}.png")
        if os.path.exists(main_image):
            os.remove(main_image)
        
        # Удаляем все референсные изображения
        for ref_pattern in [f"{character_id}_reference.png"]:
            ref_path = os.path.join(self.output_folder, ref_pattern)
            if os.path.exists(ref_path):
                os.remove(ref_path)
        
        # Удаляем метаданные
        del self.characters[character_id]
        self.save_metadata()
        
        return True
    
    def _save_character_image(self, character_id, image_path, image_type="main"):
        """
        Сохраняет изображение персонажа в нужную папку
        """
        if image_type == "main":
            destination = os.path.join(self.output_folder, f"{character_id}.png")
        elif image_type == "reference":
            destination = os.path.join(self.output_folder, f"{character_id}_reference.png")
        else:
            destination = os.path.join(self.output_folder, f"{character_id}_{image_type}.png")
        
        # Копируем или перемещаем файл
        shutil.copy2(image_path, destination)
        
        return destination