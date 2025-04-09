#!/bin/bash

echo "==================================================="
echo "=== Автоматический запуск приложения для генерации" 
echo "=== аниме-изображений с сохранением персонажей"
echo "==================================================="
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python не установлен. Пожалуйста, установите Python 3.8 или выше."
    echo "Для Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "Для Mac: brew install python3"
    exit 1
fi

# Проверка наличия Node.js
if ! command -v node &> /dev/null; then
    echo "[ОШИБКА] Node.js не установлен. Пожалуйста, установите Node.js 14 или выше."
    echo "Для Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "Для Mac: brew install node"
    exit 1
fi

# Проверка наличия папок проекта
if [ ! -d "backend" ]; then
    echo "[ОШИБКА] Папка backend не найдена."
    echo "Убедитесь, что вы запускаете скрипт из корневой папки проекта."
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "[ОШИБКА] Папка frontend не найдена."
    echo "Убедитесь, что вы запускаете скрипт из корневой папки проекта."
    exit 1
fi

echo "[INFO] Настройка бэкенда..."

# Создание виртуального окружения Python, если его нет
if [ ! -d "backend/venv" ]; then
    echo "[INFO] Создание виртуального окружения Python..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Активация виртуального окружения и установка зависимостей
echo "[INFO] Установка Python-зависимостей..."
cd backend
source venv/bin/activate
pip install flask flask-cors Pillow requests
echo "[INFO] Python-зависимости установлены"

# Создание необходимых папок
mkdir -p uploads/characters
mkdir -p uploads/scenes
mkdir -p uploads/temp

# Запуск бэкенда в фоновом режиме
echo "[INFO] Запуск бэкенда..."
(source venv/bin/activate && python app.py) &
BACKEND_PID=$!

# Переход к настройке фронтенда
cd ..
echo ""
echo "[INFO] Настройка фронтенда..."

# Установка зависимостей для фронтенда
cd frontend
if [ ! -d "node_modules" ]; then
    echo "[INFO] Установка Node.js зависимостей..."
    npm install
    echo "[INFO] Node.js зависимости установлены"
else
    echo "[INFO] Node.js зависимости уже установлены"
fi

# Запуск фронтенда
echo "[INFO] Запуск фронтенда..."
npm start &
FRONTEND_PID=$!

cd ..
echo ""
echo "==================================================="
echo "Приложение запущено!"
echo "Бэкенд доступен по адресу: http://localhost:5000"
echo "Фронтенд доступен по адресу: http://localhost:3000"
echo ""
echo "Для остановки приложения нажмите Ctrl+C"
echo "==================================================="
echo ""

# Обработка сигнала завершения
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

# Ожидаем завершения процессов
wait