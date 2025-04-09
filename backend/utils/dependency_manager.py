import os
import sys
import subprocess
import threading
import logging
import json
import time
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class DependencyManager:
    def __init__(self):
        self.status = {
            "dependencies": {
                "stable_diffusion": {"installed": False, "progress": 0, "message": "Not installed"},
                "control_net": {"installed": False, "progress": 0, "message": "Not installed"},
                "face_id": {"installed": False, "progress": 0, "message": "Not installed"}
            },
            "models": {
                "anime_model": {"installed": False, "progress": 0, "message": "Not installed"},
                "real_dream_pony": {"installed": False, "progress": 0, "message": "Not installed"},
                "controlnet_openpose": {"installed": False, "progress": 0, "message": "Not installed"}
            },
            "overall_status": {"ready": False, "progress": 0, "message": "Installation required"}
        }
        
        # Путь к директории с моделями
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Проверяем, какие модели уже установлены
        self._check_installed_dependencies()
    
    def _check_installed_dependencies(self):
        """
        Проверяет, какие зависимости и модели уже установлены
        """
        # Проверяем библиотеки Python
        try:
            import torch
            import diffusers
            self.status["dependencies"]["stable_diffusion"]["installed"] = True
            self.status["dependencies"]["stable_diffusion"]["progress"] = 100
            self.status["dependencies"]["stable_diffusion"]["message"] = "Installed"
        except ImportError:
            pass
        
        try:
            from diffusers import ControlNetModel
            self.status["dependencies"]["control_net"]["installed"] = True
            self.status["dependencies"]["control_net"]["progress"] = 100
            self.status["dependencies"]["control_net"]["message"] = "Installed"
        except ImportError:
            pass
        
        try:
            import insightface
            self.status["dependencies"]["face_id"]["installed"] = True
            self.status["dependencies"]["face_id"]["progress"] = 100
            self.status["dependencies"]["face_id"]["message"] = "Installed"
        except ImportError:
            pass
        
        # Проверяем наличие моделей
        anime_model_path = os.path.join(self.models_dir, 'anime_model')
        if os.path.exists(anime_model_path) and os.path.isdir(anime_model_path):
            self.status["models"]["anime_model"]["installed"] = True
            self.status["models"]["anime_model"]["progress"] = 100
            self.status["models"]["anime_model"]["message"] = "Installed"
        
        real_dream_path = os.path.join(self.models_dir, 'real_dream_pony')
        if os.path.exists(real_dream_path) and os.path.isdir(real_dream_path):
            self.status["models"]["real_dream_pony"]["installed"] = True
            self.status["models"]["real_dream_pony"]["progress"] = 100
            self.status["models"]["real_dream_pony"]["message"] = "Installed"
        
        controlnet_path = os.path.join(self.models_dir, 'controlnet_openpose')
        if os.path.exists(controlnet_path) and os.path.isdir(controlnet_path):
            self.status["models"]["controlnet_openpose"]["installed"] = True
            self.status["models"]["controlnet_openpose"]["progress"] = 100
            self.status["models"]["controlnet_openpose"]["message"] = "Installed"
        
        # Обновляем общий статус
        self._update_overall_status()
    
    def _update_overall_status(self):
        """
        Обновляет общий статус установки
        """
        total_deps = len(self.status["dependencies"]) + len(self.status["models"])
        installed_deps = 0
        total_progress = 0
        
        for dep in self.status["dependencies"].values():
            if dep["installed"]:
                installed_deps += 1
            total_progress += dep["progress"]
        
        for model in self.status["models"].values():
            if model["installed"]:
                installed_deps += 1
            total_progress += model["progress"]
        
        overall_progress = total_progress / total_deps if total_deps > 0 else 0
        
        self.status["overall_status"]["progress"] = round(overall_progress)
        
        if installed_deps == total_deps:
            self.status["overall_status"]["ready"] = True
            self.status["overall_status"]["message"] = "Ready to use"
        else:
            self.status["overall_status"]["ready"] = False
            if overall_progress > 0:
                self.status["overall_status"]["message"] = "Installation in progress"
            else:
                self.status["overall_status"]["message"] = "Installation required"
    
    def get_status(self):
        """
        Возвращает текущий статус установки зависимостей и моделей
        """
        self._check_installed_dependencies()
        return self.status
    
    def install_dependencies(self, dep_type="all"):
        """
        Устанавливает необходимые зависимости и модели
        dep_type может быть 'all', 'dependencies' или 'models'
        """
        if dep_type == "all" or dep_type == "dependencies":
            self._install_python_dependencies()
        
        if dep_type == "all" or dep_type == "models":
            self._download_models()
        
        return {"success": True, "message": "Installation started"}
    
    def _install_python_dependencies(self):
        """
        Устанавливает необходимые Python-библиотеки
        """
        def install_thread():
            try:
                # Обновляем статус
                for dep in self.status["dependencies"].values():
                    dep["progress"] = 10
                    dep["message"] = "Installation started"
                self._update_overall_status()
                
                # Устанавливаем Stable Diffusion и связанные библиотеки
                packages = [
                    "torch",
                    "diffusers",
                    "transformers",
                    "accelerate"
                ]
                
                for i, package in enumerate(packages):
                    progress = (i + 1) / len(packages) * 90
                    self.status["dependencies"]["stable_diffusion"]["progress"] = 10 + int(progress)
                    self.status["dependencies"]["stable_diffusion"]["message"] = f"Installing {package}"
                    self._update_overall_status()
                    
                    # В реальном проекте здесь будет реальная установка пакетов
                    # subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    time.sleep(1)  # Имитация установки
                
                self.status["dependencies"]["stable_diffusion"]["installed"] = True
                self.status["dependencies"]["stable_diffusion"]["progress"] = 100
                self.status["dependencies"]["stable_diffusion"]["message"] = "Installed"
                
                # Устанавливаем ControlNet
                self.status["dependencies"]["control_net"]["progress"] = 50
                self.status["dependencies"]["control_net"]["message"] = "Installing"
                self._update_overall_status()
                
                # В реальном проекте здесь будет реальная установка
                # subprocess.check_call([sys.executable, "-m", "pip", "install", "controlnet"])
                time.sleep(1)  # Имитация установки
                
                self.status["dependencies"]["control_net"]["installed"] = True
                self.status["dependencies"]["control_net"]["progress"] = 100
                self.status["dependencies"]["control_net"]["message"] = "Installed"
                
                # Устанавливаем Face ID
                self.status["dependencies"]["face_id"]["progress"] = 50
                self.status["dependencies"]["face_id"]["message"] = "Installing"
                self._update_overall_status()
                
                # В реальном проекте здесь будет реальная установка
                # subprocess.check_call([sys.executable, "-m", "pip", "install", "insightface", "onnxruntime-gpu"])
                time.sleep(1)  # Имитация установки
                
                self.status["dependencies"]["face_id"]["installed"] = True
                self.status["dependencies"]["face_id"]["progress"] = 100
                self.status["dependencies"]["face_id"]["message"] = "Installed"
                
                self._update_overall_status()
                
            except Exception as e:
                logger.error(f"Error installing dependencies: {e}")
                for dep in self.status["dependencies"].values():
                    if not dep["installed"]:
                        dep["message"] = f"Installation failed: {str(e)}"
                self._update_overall_status()
        
        # Запускаем установку в отдельном потоке
        threading.Thread(target=install_thread).start()
        
        return True
    
    def _download_models(self):
        """
        Скачивает необходимые модели
        """
        def download_thread():
            try:
                # Обновляем статус
                for model in self.status["models"].values():
                    model["progress"] = 10
                    model["message"] = "Download started"
                self._update_overall_status()
                
                # Скачиваем модель для аниме
                anime_model_path = os.path.join(self.models_dir, 'anime_model')
                if not os.path.exists(anime_model_path):
                    os.makedirs(anime_model_path, exist_ok=True)
                
                self.status["models"]["anime_model"]["progress"] = 30
                self.status["models"]["anime_model"]["message"] = "Downloading model files"
                self._update_overall_status()
                
                # В реальном проекте здесь будет реальная загрузка модели
                # from huggingface_hub import snapshot_download
                # snapshot_download("AstraliteHeart/pony-diffusion-v4", local_dir=anime_model_path)
                time.sleep(2)  # Имитация загрузки
                
                self.status["models"]["anime_model"]["installed"] = True
                self.status["models"]["anime_model"]["progress"] = 100
                self.status["models"]["anime_model"]["message"] = "Installed"
                self._update_overall_status()
                
                # Скачиваем Real Dream Pony V9
                real_dream_path = os.path.join(self.models_dir, 'real_dream_pony')
                if not os.path.exists(real_dream_path):
                    os.makedirs(real_dream_path, exist_ok=True)
                
                self.status["models"]["real_dream_pony"]["progress"] = 30
                self.status["models"]["real_dream_pony"]["message"] = "Downloading model files"
                self._update_overall_status()
                
                # В реальном проекте здесь будет реальная загрузка модели
                # Например, из CivitAI или из другого источника
                time.sleep(3)  # Имитация загрузки
                
                # Создаем пустой файл для имитации загруженной модели
                with open(os.path.join(real_dream_path, 'model.safetensors'), 'w') as f:
                    f.write('')
                
                self.status["models"]["real_dream_pony"]["installed"] = True
                self.status["models"]["real_dream_pony"]["progress"] = 100
                self.status["models"]["real_dream_pony"]["message"] = "Installed"
                self._update_overall_status()
                
                # Скачиваем ControlNet OpenPose
                controlnet_path = os.path.join(self.models_dir, 'controlnet_openpose')
                if not os.path.exists(controlnet_path):
                    os.makedirs(controlnet_path, exist_ok=True)
                
                self.status["models"]["controlnet_openpose"]["progress"] = 30
                self.status["models"]["controlnet_openpose"]["message"] = "Downloading model files"
                self._update_overall_status()
                
                # В реальном проекте здесь будет реальная загрузка модели
                # from huggingface_hub import snapshot_download
                # snapshot_download("lllyasviel/sd-controlnet-openpose", local_dir=controlnet_path)
                time.sleep(2)  # Имитация загрузки
                
                self.status["models"]["controlnet_openpose"]["installed"] = True
                self.status["models"]["controlnet_openpose"]["progress"] = 100
                self.status["models"]["controlnet_openpose"]["message"] = "Installed"
                self._update_overall_status()
                
            except Exception as e:
                logger.error(f"Error downloading models: {e}")
                for model in self.status["models"].values():
                    if not model["installed"]:
                        model["message"] = f"Download failed: {str(e)}"
                self._update_overall_status()
        
        # Запускаем загрузку в отдельном потоке
        threading.Thread(target=download_thread).start()
        
        return True