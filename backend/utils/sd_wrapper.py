import os
import sys
import logging
import io
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class StableDiffusionWrapper:
    def __init__(self, mock_mode=True):
        self.api_url = os.environ.get('SD_API_URL', 'http://localhost:7860/api/v1')
        self.is_initialized = False
        self.mock_mode = mock_mode
        
        # В реальном режиме будут проверки наличия GPU и т.д.
        if not mock_mode:
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Using device: {self.device}")
            except ImportError:
                logger.warning("PyTorch not available, forcing mock mode")
                self.mock_mode = True
                self.device = "cpu"
    
    def initialize(self):
        """
        Инициализирует модели Stable Diffusion.
        В реальном проекте здесь будет загрузка моделей в память.
        """
        if self.mock_mode:
            logger.info("Running in mock mode, no actual models will be loaded")
            self.is_initialized = True
            return True
            
        try:
            # Импортируем необходимые библиотеки для работы с моделями
            import torch
            from diffusers import StableDiffusionPipeline, ControlNetModel, StableDiffusionControlNetPipeline
            
            # Загружаем основную модель
            logger.info("Loading Stable Diffusion model...")
            self.model = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            # Загружаем модель для аниме
            logger.info("Loading anime model...")
            self.anime_model = StableDiffusionPipeline.from_pretrained(
                "AstraliteHeart/pony-diffusion-v4",  # Пример, в реальности - другая модель
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            # Загружаем ControlNet
            logger.info("Loading ControlNet model...")
            self.controlnet = ControlNetModel.from_pretrained(
                "lllyasviel/sd-controlnet-openpose",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            self.is_initialized = True
            logger.info("All models loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Stable Diffusion models: {e}")
            return False
    
    def check_initialized(self):
        """
        Проверяет, инициализированы ли модели, и инициализирует их при необходимости
        """
        if not self.is_initialized:
            return self.initialize()
        return True
    
    def generate(self, prompt, output_path, negative_prompt="", width=512, height=768):
        """
        Генерирует изображение на основе текстового описания
        """
        if self.mock_mode:
            return self._create_mock_image(prompt, output_path, width, height)
            
        if not self.check_initialized():
            return self._create_mock_image(prompt, output_path, width, height)
        
        try:
            # В реальном проекте здесь будет вызов модели для генерации изображения
            image = self.anime_model(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
            ).images[0]
            
            # Сохраняем изображение
            image.save(output_path)
            
            return True
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_mock_image(prompt, output_path, width, height)
    
    def generate_with_reference(self, prompt, reference_image, output_path, negative_prompt=""):
        """
        Генерирует изображение на основе текстового описания и референсного изображения
        """
        if self.mock_mode:
            return self._create_mock_image(prompt, output_path, ref_image=reference_image)
            
        if not self.check_initialized():
            return self._create_mock_image(prompt, output_path, ref_image=reference_image)
        
        try:
            # Загружаем референсное изображение
            if isinstance(reference_image, str):
                reference_img = Image.open(reference_image)
            else:
                reference_img = reference_image
            
            # Ресайзим изображение если нужно
            reference_img = reference_img.resize((512, 512))
            
            # В реальном проекте здесь будет вызов IP-Adapter или другого метода для сохранения персонажа
            
            # Для демонстрации просто копируем референсное изображение
            reference_img.save(output_path)
            
            return True
        except Exception as e:
            logger.error(f"Error generating image with reference: {e}")
            return self._create_mock_image(prompt, output_path, ref_image=reference_image)
    
    def generate_scene(self, prompt, character_image, output_path, negative_prompt=""):
        """
        Генерирует сюжетную сцену с персонажем
        """
        if self.mock_mode:
            return self._create_mock_image(prompt, output_path, width=768, height=512, scene=True)
            
        if not self.check_initialized():
            return self._create_mock_image(prompt, output_path, width=768, height=512, scene=True)
        
        try:
            # Загружаем изображение персонажа
            if isinstance(character_image, str):
                char_img = Image.open(character_image)
            else:
                char_img = character_image
            
            # В реальном проекте здесь будет использование ControlNet для сохранения персонажа
            
            # Для демонстрации создаем тестовое изображение
            image = self._create_dummy_image(768, 512)
            
            # Сохраняем изображение
            image.save(output_path)
            
            return True
        except Exception as e:
            logger.error(f"Error generating scene: {e}")
            return self._create_mock_image(prompt, output_path, width=768, height=512, scene=True)
    
    def _create_mock_image(self, prompt, output_path, width=512, height=768, ref_image=None, scene=False):
        """
        Создает мок-изображение для тестирования без реальных моделей
        """
        try:
            # Создаем базовое изображение
            image = Image.new('RGB', (width, height), color=(240, 240, 240))
            draw = ImageDraw.Draw(image)
            
            # Пытаемся использовать стандартный шрифт или создаем без текста, если не найден
            try:
                # Пытаемся найти шрифт в системе
                font_path = None
                
                # Windows пути к шрифтам
                windows_font_paths = [
                    'C:\\Windows\\Fonts\\Arial.ttf',
                    'C:\\Windows\\Fonts\\Consolas.ttf',
                    'C:\\Windows\\Fonts\\Verdana.ttf'
                ]
                
                # Linux пути к шрифтам
                linux_font_paths = [
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    '/usr/share/fonts/TTF/DejaVuSans.ttf',
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
                ]
                
                # Проверяем доступные шрифты
                for path in windows_font_paths + linux_font_paths:
                    if os.path.exists(path):
                        font_path = path
                        break
                
                if font_path:
                    font = ImageFont.truetype(font_path, 18)
                    
                    # Добавляем текст с промптом
                    draw.rectangle([(10, 10), (width-10, 120)], fill=(255, 255, 255), outline=(200, 200, 200))
                    
                    # Обрезаем текст, если он слишком длинный
                    display_prompt = prompt
                    if len(prompt) > 100:
                        display_prompt = prompt[:97] + "..."
                    
                    # Помещаем текст в рамку
                    draw.text((20, 20), f"Prompt: {display_prompt}", fill=(0, 0, 0), font=font)
                    draw.text((20, 50), "Mock Image - No real AI generation", fill=(255, 0, 0), font=font)
                    
                    if scene:
                        draw.text((20, 80), "Scene Generation Mode", fill=(0, 0, 255), font=font)
                    else:
                        draw.text((20, 80), "Character Generation Mode", fill=(0, 128, 0), font=font)
            except Exception as font_error:
                logger.warning(f"Could not load font, skipping text: {font_error}")
            
            # Если это генерация с референсом, и референс есть - добавляем его уменьшенную версию в угол
            if ref_image and os.path.exists(ref_image):
                try:
                    ref = Image.open(ref_image)
                    # Ресайзим референс до маленького размера
                    ref_size = 150
                    ref.thumbnail((ref_size, ref_size))
                    
                    # Помещаем его в правый верхний угол
                    image.paste(ref, (width - ref_size - 10, 10))
                    
                    # Добавляем рамку
                    draw.rectangle(
                        [(width - ref_size - 11, 9), (width - 9, ref_size + 11)], 
                        outline=(200, 200, 200), width=1
                    )
                except Exception as e:
                    logger.warning(f"Could not add reference thumbnail: {e}")
            
            # Добавляем сетку для наглядности
            grid_size = 50
            light_color = (230, 230, 230)
            
            for x in range(0, width, grid_size):
                draw.line([(x, 0), (x, height)], fill=light_color)
            
            for y in range(0, height, grid_size):
                draw.line([(0, y), (width, y)], fill=light_color)
                
            # Сохраняем изображение
            image.save(output_path)
            
            return True
        except Exception as e:
            logger.error(f"Error creating mock image: {e}")
            # В крайнем случае создаем совсем простое изображение
            self._create_dummy_image(width, height).save(output_path)
            return True
    
    def _create_dummy_image(self, width, height):
        """
        Создает простое пустое изображение заданного размера
        """
        image = Image.new('RGB', (width, height), color=(240, 240, 240))
        return image