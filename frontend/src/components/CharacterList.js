import React from 'react';
import './CharacterList.css';

function CharacterList({ characters, onEdit, onDelete }) {
  const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  // Сортируем персонажей по дате создания (от новых к старым)
  const sortedCharacters = [...characters].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  });

  return (
    <div className="character-list">
      <h2>Список персонажей</h2>
      
      {sortedCharacters.length === 0 ? (
        <div className="no-characters">
          <p>У вас пока нет созданных персонажей</p>
        </div>
      ) : (
        <div className="characters-grid">
          {sortedCharacters.map((character) => (
            <div key={character.id} className="character-card">
              <div className="character-image-container">
                <img 
                  src={`http://localhost:5000${character.image_url}`} 
                  alt={character.description} 
                  className="character-image"
                  onError={(e) => {
                    e.target.onerror = null; 
                    e.target.src = '/placeholder-character.png';
                  }}
                />
              </div>
              
              <div className="character-info">
                <div className="character-description">
                  {character.description.length > 100 
                    ? `${character.description.substring(0, 100)}...` 
                    : character.description}
                </div>
                
                <div className="character-meta">
                  <div className="character-date">
                    Создан: {formatDate(character.created_at)}
                  </div>
                  {character.updated_at !== character.created_at && (
                    <div className="character-date">
                      Обновлен: {formatDate(character.updated_at)}
                    </div>
                  )}
                </div>
                
                <div className="character-actions">
                  <button 
                    className="edit-button"
                    onClick={() => onEdit(character)}
                  >
                    Редактировать
                  </button>
                  <button 
                    className="delete-button"
                    onClick={() => {
                      if (window.confirm(`Вы уверены, что хотите удалить персонажа "${character.description}"?`)) {
                        onDelete(character.id);
                      }
                    }}
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CharacterList;