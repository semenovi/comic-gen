from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import json
from werkzeug.utils import secure_filename
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем модули
from modules.character_generator import CharacterGenerator
from modules.scene_generator import SceneGenerator
from utils.dependency_manager import DependencyManager

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Папки для хранения изображений и данных
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
CHARACTERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'characters')
SCENES_FOLDER = os.path.join(UPLOAD_FOLDER, 'scenes')
TEMP_FOLDER = os.path.join(UPLOAD_FOLDER, 'temp')

# Создаем папки, если они не существуют
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHARACTERS_FOLDER, exist_ok=True)
os.makedirs(SCENES_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Инициализация менеджера зависимостей
dependency_manager = DependencyManager()

# Инициализация генераторов
character_generator = CharacterGenerator(CHARACTERS_FOLDER)
scene_generator = SceneGenerator(SCENES_FOLDER)

# Роуты для статуса зависимостей
@app.route('/api/status', methods=['GET'])
def get_status():
    status = dependency_manager.get_status()
    return jsonify(status)

@app.route('/api/dependencies/install', methods=['POST'])
def install_dependencies():
    dependency_type = request.json.get('type', 'all')
    result = dependency_manager.install_dependencies(dependency_type)
    return jsonify(result)

# Роуты для работы с персонажами
@app.route('/api/characters', methods=['GET'])
def get_characters():
    characters = character_generator.get_all_characters()
    return jsonify(characters)

@app.route('/api/characters', methods=['POST'])
def create_character():
    # Получаем текстовое описание из запроса
    data = request.form.to_dict()
    description = data.get('description', '')
    
    # Проверяем, есть ли загруженное изображение
    reference_image = None
    if 'reference_image' in request.files:
        file = request.files['reference_image']
        if file.filename:
            # Сохраняем изображение во временной папке
            filename = secure_filename(file.filename)
            filepath = os.path.join(TEMP_FOLDER, filename)
            file.save(filepath)
            reference_image = filepath
    
    # Генерируем персонажа
    character = character_generator.generate(description, reference_image)
    return jsonify(character)

@app.route('/api/characters/<character_id>', methods=['PUT'])
def update_character(character_id):
    data = request.form.to_dict()
    
    # Проверяем, есть ли загруженное изображение для замены
    new_image = None
    if 'new_image' in request.files:
        file = request.files['new_image']
        if file.filename:
            # Сохраняем изображение во временной папке
            filename = secure_filename(file.filename)
            filepath = os.path.join(TEMP_FOLDER, filename)
            file.save(filepath)
            new_image = filepath
    
    # Обновляем персонажа
    character = character_generator.update(character_id, data, new_image)
    if character:
        return jsonify(character)
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/api/characters/<character_id>', methods=['DELETE'])
def delete_character(character_id):
    result = character_generator.delete(character_id)
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Character not found"}), 404

# Роуты для генерации сюжетных изображений
@app.route('/api/scenes', methods=['POST'])
def create_scene():
    data = request.json
    character_id = data.get('character_id')
    plot_description = data.get('plot_description', '')
    
    scene = scene_generator.generate(character_id, plot_description)
    if scene:
        return jsonify(scene)
    else:
        return jsonify({"error": "Failed to generate scene"}), 400

# Роуты для получения изображений
@app.route('/uploads/characters/<path:filename>')
def character_image(filename):
    return send_from_directory(CHARACTERS_FOLDER, filename)

@app.route('/uploads/scenes/<path:filename>')
def scene_image(filename):
    return send_from_directory(SCENES_FOLDER, filename)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)