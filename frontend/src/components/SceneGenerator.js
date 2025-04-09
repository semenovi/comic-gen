import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SceneGenerator.css';

function SceneGenerator({ apiBaseUrl }) {
  const [characters, setCharacters] = useState([]);
  const [selectedCharacterId, setSelectedCharacterId] = useState('');
  const [plotDescription, setPlotDescription] = useState('');
  const [generatedScenes, setGeneratedScenes] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  // Загрузка списка персонажей при монтировании компонента
  useEffect(() => {
    fetchCharacters();
    fetchScenes();
  }, []);

  // Функция для загрузки списка персонажей
  const fetchCharacters = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/characters`);
      setCharacters(response.data);
      
      // Если персонажи есть, выбираем первого по умолчанию
      if (response.data.length > 0) {
        setSelectedCharacterId(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching characters:', error);
      setError('Ошибка при загрузке персонажей');
    }
  };

  // Функция для загрузки списка сгенерированных сцен
  const fetchScenes = async () => {
    try {
      // В реальном приложении здесь был бы запрос к API
      // Для демонстрации используем заглушку
      setGeneratedScenes([]);
    } catch (error) {
      console.error('Error fetching scenes:', error);
      setError('Ошибка при загрузке сцен');
    }
  };

  // Обработчик изменения выбранного персонажа
  const handleCharacterChange = (e) => {
    setSelectedCharacterId(e.target.value);
  };

  // Обработчик изменения описания сюжета
  const handlePlotDescriptionChange = (e) => {
    setPlotDescription(e.target.value);
  };

  // Обработчик нажатия на кнопку генерации сцены
  const handleGenerateScene = async () => {
    if (!selectedCharacterId) {
      setError('Выберите персонажа');
      return;
    }

    if (!plotDescription.trim()) {
      setError('Введите описание сюжета');
      return;
    }

    setError('');
    setIsGenerating(true);

    try {
      const response = await axios.post(`${apiBaseUrl}/scenes`, {
        character_id: selectedCharacterId,
        plot_description: plotDescription
      });

      // Добавляем новую сцену в начало списка
      setGeneratedScenes([response.data, ...generatedScenes]);
      
      // Очищаем поле описания сюжета
      setPlotDescription('');
    } catch (error) {
      console.error('Error generating scene:', error);
      setError('Ошибка при генерации сцены');
    } finally {
      setIsGenerating(false);
    }
  };

  // Функция для определения, какого персонажа выбрали
  const getSelectedCharacter = () => {
    return characters.find(character => character.id === selectedCharacterId);
  };

  return (
    <div className="scene-generator">
      <div className="generator-container">
        <h2>Генерация сюжетной сцены</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="character-select">Выберите персонажа:</label>
          <select
            id="character-select"
            value={selectedCharacterId}
            onChange={handleCharacterChange}
            disabled={isGenerating || characters.length === 0}
          >
            {characters.length === 0 ? (
              <option value="">Нет доступных персонажей</option>
            ) : (
              characters.map(character => (
                <option key={character.id} value={character.id}>
                  {character.description.substring(0, 50)}
                  {character.description.length > 50 ? '...' : ''}
                </option>
              ))
            )}
          </select>
        </div>
        
        {selectedCharacterId && getSelectedCharacter() && (
          <div className="selected-character-preview">
            <img 
              src={`http://localhost:5000${getSelectedCharacter().image_url}`} 
              alt={getSelectedCharacter().description}
              onError={(e) => {
                e.target.onerror = null; 
                e.target.src = '/placeholder-character.png';
              }}
            />
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="plot-description">Описание сюжета:</label>
          <textarea
            id="plot-description"
            value={plotDescription}
            onChange={handlePlotDescriptionChange}
            placeholder="Опишите сюжетную сцену с участием персонажа (например: персонаж гуляет в парке осенью, падающие листья, солнечный свет)"
            rows={4}
            disabled={isGenerating || !selectedCharacterId}
          />
        </div>
        
        <div className="action-buttons">
          <button 
            className="generate-button"
            onClick={handleGenerateScene}
            disabled={isGenerating || !selectedCharacterId || !plotDescription.trim()}
          >
            {isGenerating ? 'Генерация...' : 'Сгенерировать сцену'}
          </button>
        </div>
      </div>
      
      <div className="generated-scenes">
        <h2>Сгенерированные сцены</h2>
        
        {generatedScenes.length === 0 ? (
          <div className="no-scenes">
            <p>У вас пока нет сгенерированных сцен</p>
          </div>
        ) : (
          <div className="scenes-grid">
            {generatedScenes.map((scene) => {
              // Находим персонажа для этой сцены
              const character = characters.find(c => c.id === scene.character_id);
              
              return (
                <div key={scene.id} className="scene-card">
                  <div className="scene-image-container">
                    <img
                      src={`http://localhost:5000${scene.image_url}`}
                      alt={scene.plot_description}
                      className="scene-image"
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = '/placeholder-scene.png';
                      }}
                    />
                  </div>
                  
                  <div className="scene-info">
                    <div className="scene-description">
                      {scene.plot_description}
                    </div>
                    
                    {character && (
                      <div className="scene-character">
                        Персонаж: {character.description.substring(0, 50)}
                        {character.description.length > 50 ? '...' : ''}
                      </div>
                    )}
                    
                    <div className="scene-date">
                      Создана: {new Date(scene.created_at).toLocaleString()}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default SceneGenerator;