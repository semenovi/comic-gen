import React from 'react';
import { useNavigate } from 'react-router-dom';
import './DependencyStatus.css';

function DependencyStatus({ status, onInstall }) {
  const navigate = useNavigate();
  
  // Функция для обработки нажатия на кнопку установки
  const handleInstall = (type) => {
    onInstall(type);
  };
  
  // Функция для перехода на страницу создания персонажа, если система готова
  const handleStart = () => {
    navigate('/characters');
  };
  
  return (
    <div className="dependency-status">
      <h2>Статус системы</h2>
      
      <div className="status-overview">
        <div className="status-card overall">
          <h3>Общий статус</h3>
          <div className="progress-bar">
            <div 
              className="progress-bar-fill" 
              style={{ width: `${status.overall_status.progress}%` }}
            />
          </div>
          <div className="status-info">
            <p>{status.overall_status.message}</p>
            <p className="progress-percent">{status.overall_status.progress}%</p>
          </div>
          {status.overall_status.ready ? (
            <button className="button start-button" onClick={handleStart}>
              Начать работу
            </button>
          ) : (
            <button className="button install-button" onClick={() => handleInstall('all')}>
              Установить все
            </button>
          )}
        </div>
      </div>
      
      <div className="status-sections">
        <div className="status-section">
          <h3>Зависимости</h3>
          <div className="status-cards">
            {Object.entries(status.dependencies).map(([key, dependency]) => (
              <div key={key} className="status-card">
                <h4>{formatDependencyName(key)}</h4>
                <div className="progress-bar">
                  <div 
                    className="progress-bar-fill" 
                    style={{ width: `${dependency.progress}%` }}
                  />
                </div>
                <div className="status-info">
                  <p>{dependency.message}</p>
                  <p className="progress-percent">{dependency.progress}%</p>
                </div>
              </div>
            ))}
          </div>
          <button className="button install-button" onClick={() => handleInstall('dependencies')}>
            Установить зависимости
          </button>
        </div>
        
        <div className="status-section">
          <h3>Модели</h3>
          <div className="status-cards">
            {Object.entries(status.models).map(([key, model]) => (
              <div key={key} className="status-card">
                <h4>{formatModelName(key)}</h4>
                <div className="progress-bar">
                  <div 
                    className="progress-bar-fill" 
                    style={{ width: `${model.progress}%` }}
                  />
                </div>
                <div className="status-info">
                  <p>{model.message}</p>
                  <p className="progress-percent">{model.progress}%</p>
                </div>
              </div>
            ))}
          </div>
          <button className="button install-button" onClick={() => handleInstall('models')}>
            Установить модели
          </button>
        </div>
      </div>
      
      <div className="instructions">
        <h3>Инструкции</h3>
        <p>
          Для работы с приложением необходимо установить все зависимости и модели. 
          Процесс установки может занять некоторое время в зависимости от скорости вашего интернет-соединения.
        </p>
        <p>
          После установки вы сможете создавать персонажей и генерировать сюжетные картинки с ними.
        </p>
      </div>
    </div>
  );
}

// Функция для форматирования названий зависимостей
function formatDependencyName(name) {
  const nameMap = {
    'stable_diffusion': 'Stable Diffusion',
    'control_net': 'ControlNet',
    'face_id': 'Face ID'
  };
  return nameMap[name] || name;
}

// Функция для форматирования названий моделей
function formatModelName(name) {
  const nameMap = {
    'anime_model': 'Аниме модель',
    'real_dream_pony': 'Real Dream Pony V9',
    'controlnet_openpose': 'ControlNet OpenPose'
  };
  return nameMap[name] || name;
}

export default DependencyStatus;