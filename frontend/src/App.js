import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Импортируем компоненты
import DependencyStatus from './components/DependencyStatus';
import CharacterGenerator from './components/CharacterGenerator';
import SceneGenerator from './components/SceneGenerator';
import CharacterList from './components/CharacterList';

// Базовый URL API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [status, setStatus] = useState({
    dependencies: {
      stable_diffusion: { installed: false, progress: 0, message: "Not installed" },
      control_net: { installed: false, progress: 0, message: "Not installed" },
      face_id: { installed: false, progress: 0, message: "Not installed" }
    },
    models: {
      anime_model: { installed: false, progress: 0, message: "Not installed" },
      real_dream_pony: { installed: false, progress: 0, message: "Not installed" },
      controlnet_openpose: { installed: false, progress: 0, message: "Not installed" }
    },
    overall_status: { ready: false, progress: 0, message: "Loading..." }
  });
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Получение статуса зависимостей и моделей
  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/status`);
      setStatus(response.data);
      setIsReady(response.data.overall_status.ready);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching status:', error);
      setIsLoading(false);
    }
  };

  // Установка зависимостей и моделей
  const installDependencies = async (type = 'all') => {
    try {
      await axios.post(`${API_BASE_URL}/dependencies/install`, { type });
      // После запуска установки, начинаем периодический опрос статуса
      const intervalId = setInterval(async () => {
        const response = await axios.get(`${API_BASE_URL}/status`);
        setStatus(response.data);
        setIsReady(response.data.overall_status.ready);
        
        // Если установка завершена, останавливаем опрос
        if (response.data.overall_status.ready) {
          clearInterval(intervalId);
        }
      }, 2000);
      
      // Очистка интервала при размонтировании компонента
      return () => clearInterval(intervalId);
    } catch (error) {
      console.error('Error installing dependencies:', error);
    }
  };

  // Загрузка статуса при первой загрузке компонента
  useEffect(() => {
    fetchStatus();
    
    // Периодический опрос статуса каждые 5 секунд
    const intervalId = setInterval(() => {
      fetchStatus();
    }, 5000);
    
    // Очистка интервала при размонтировании компонента
    return () => clearInterval(intervalId);
  }, []);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Генератор аниме-изображений</h1>
          <nav>
            <ul className="nav-links">
              <li>
                <Link to="/">Статус</Link>
              </li>
              <li>
                <Link to="/characters" className={!isReady ? 'disabled-link' : ''}>
                  Создать персонажа
                </Link>
              </li>
              <li>
                <Link to="/scenes" className={!isReady ? 'disabled-link' : ''}>
                  Создать сцену
                </Link>
              </li>
            </ul>
          </nav>
        </header>

        <main className="App-main">
          {isLoading ? (
            <div className="loading">
              <p>Загрузка...</p>
            </div>
          ) : (
            <Routes>
              <Route 
                path="/" 
                element={
                  <DependencyStatus 
                    status={status} 
                    onInstall={installDependencies} 
                  />
                } 
              />
              <Route 
                path="/characters" 
                element={
                  isReady ? (
                    <CharacterGenerator apiBaseUrl={API_BASE_URL} />
                  ) : (
                    <div className="not-ready">
                      <p>Для создания персонажей необходимо установить зависимости.</p>
                      <button onClick={() => installDependencies()}>
                        Установить зависимости
                      </button>
                    </div>
                  )
                } 
              />
              <Route 
                path="/scenes" 
                element={
                  isReady ? (
                    <SceneGenerator apiBaseUrl={API_BASE_URL} />
                  ) : (
                    <div className="not-ready">
                      <p>Для создания сцен необходимо установить зависимости.</p>
                      <button onClick={() => installDependencies()}>
                        Установить зависимости
                      </button>
                    </div>
                  )
                } 
              />
            </Routes>
          )}
        </main>

        <footer className="App-footer">
          <p>Генеративное создание изображений в аниме-стиле © 2025</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;