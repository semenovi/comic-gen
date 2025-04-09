import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import CharacterList from './CharacterList';
import './CharacterGenerator.css';

function CharacterGenerator({ apiBaseUrl }) {
  const [description, setDescription] = useState('');
  const [referenceImage, setReferenceImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [characters, setCharacters] = useState([]);
  const [error, setError] = useState('');
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const fileInputRef = useRef(null);

  // Загрузка списка персонажей при монтировании компонента
  useEffect(() => {
    fetchCharacters();
  }, []);

  // Функция для загрузки списка персонажей
  const fetchCharacters = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/characters`);
      setCharacters(response.data);
    } catch (error) {
      console.error('Error fetching characters:', error);
      setError('Ошибка при загрузке персонажей');
    }
  };

  // Обработчик изменения текстового описания
  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  // Обработчик выбора файла изображения
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setReferenceImage(file);
      
      // Создаем URL для превью изображения
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Обработчик нажатия на кнопку очистки изображения
  const handleClearImage = () => {
    setReferenceImage(null);
    setPreviewImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Обработчик нажатия на кнопку генерации персонажа
  const handleGenerateCharacter = async () => {
    if (!description.trim()) {
      setError('Введите описание персонажа');
      return;
    }
    
    setError('');
    setIsGenerating(true);
    
    try {
      // Создаем объект FormData для отправки файла
      const formData = new FormData();
      formData.append('description', description);
      if (referenceImage) {
        formData.append('reference_image', referenceImage);
      }
      
      const response = await axios.post(`${apiBaseUrl}/characters`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Обновляем список персонажей
      await fetchCharacters();
      
      // Очищаем форму
      setDescription('');
      setReferenceImage(null);
      setPreviewImage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Error generating character:', error);
      setError('Ошибка при генерации персонажа');
    } finally {
      setIsGenerating(false);
    }
  };

  // Обработчик выбора персонажа для редактирования
  const handleEditCharacter = (character) => {
    setSelectedCharacter(character);
    setDescription(character.description);
    setEditMode(true);
    
    // Если у персонажа есть референсное изображение, загружаем его
    if (character.references && character.references.length > 0) {
      // Здесь нужно будет загрузить изображение с сервера
      // Для демонстрации просто устанавливаем URL
      setPreviewImage(`http://localhost:5000${character.references[0]}`);
    }
  };

  // Обработчик сохранения изменений персонажа
  const handleSaveChanges = async () => {
    if (!selectedCharacter || !description.trim()) {
      setError('Введите описание персонажа');
      return;
    }
    
    setError('');
    setIsGenerating(true);
    
    try {
      // Создаем объект FormData для отправки файла
      const formData = new FormData();
      formData.append('description', description);
      if (referenceImage) {
        formData.append('new_image', referenceImage);
      }
      
      const response = await axios.put(`${apiBaseUrl}/characters/${selectedCharacter.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Обновляем список персонажей
      await fetchCharacters();
      
      // Выходим из режима редактирования
      setSelectedCharacter(null);
      setDescription('');
      setReferenceImage(null);
      setPreviewImage(null);
      setEditMode(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Error updating character:', error);
      setError('Ошибка при обновлении персонажа');
    } finally {
      setIsGenerating(false);
    }
  };

  // Обработчик отмены редактирования
  const handleCancelEdit = () => {
    setSelectedCharacter(null);
    setDescription('');
    setReferenceImage(null);
    setPreviewImage(null);
    setEditMode(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Обработчик удаления персонажа
  const handleDeleteCharacter = async (characterId) => {
    try {
      await axios.delete(`${apiBaseUrl}/characters/${characterId}`);
      
      // Обновляем список персонажей
      await fetchCharacters();
      
      // Если удаляем персонажа, которого редактируем, то выходим из режима редактирования
      if (selectedCharacter && selectedCharacter.id === characterId) {
        handleCancelEdit();
      }
    } catch (error) {
      console.error('Error deleting character:', error);
      setError('Ошибка при удалении персонажа');
    }
  };

  return (
    <div className="character-generator">
      <div className="generator-container">
        <h2>{editMode ? 'Редактирование персонажа' : 'Создание персонажа'}</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="description">Описание персонажа:</label>
          <textarea
            id="description"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Опишите вашего персонажа (например: девушка с длинными рыжими волосами, зеленые глаза, веснушки, одета в школьную форму)"
            rows={4}
            disabled={isGenerating}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="reference-image">Референсное изображение (опционально):</label>
          <div className="file-input-container">
            <input
              type="file"
              id="reference-image"
              accept="image/*"
              onChange={handleFileChange}
              disabled={isGenerating}
              ref={fileInputRef}
            />
            {previewImage && (
              <div className="image-preview-container">
                <img src={previewImage} alt="Preview" className="image-preview" />
                <button 
                  className="clear-image-button"
                  onClick={handleClearImage}
                  disabled={isGenerating}
                >
                  ✕
                </button>
              </div>
            )}
          </div>
        </div>
        
        <div className="action-buttons">
          {editMode ? (
            <>
              <button 
                className="save-button"
                onClick={handleSaveChanges}
                disabled={isGenerating}
              >
                {isGenerating ? 'Сохранение...' : 'Сохранить изменения'}
              </button>
              <button 
                className="cancel-button"
                onClick={handleCancelEdit}
                disabled={isGenerating}
              >
                Отмена
              </button>
            </>
          ) : (
            <button 
              className="generate-button"
              onClick={handleGenerateCharacter}
              disabled={isGenerating}
            >
              {isGenerating ? 'Генерация...' : 'Сгенерировать персонажа'}
            </button>
          )}
        </div>
      </div>
      
      <CharacterList 
        characters={characters} 
        onEdit={handleEditCharacter}
        onDelete={handleDeleteCharacter}
      />
    </div>
  );
}

export default CharacterGenerator;