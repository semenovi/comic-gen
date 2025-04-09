@echo off
echo ===================================================
echo === Автоматический запуск приложения для генерации 
echo === аниме-изображений с сохранением персонажей
echo ===================================================
echo.

REM Проверка наличия Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Python не установлен. Пожалуйста, установите Python 3.8 или выше.
    echo Скачать Python можно с сайта: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Проверка наличия Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Node.js не установлен. Пожалуйста, установите Node.js 14 или выше.
    echo Скачать Node.js можно с сайта: https://nodejs.org/
    pause
    exit /b 1
)

REM Проверка наличия папок проекта
if not exist backend (
    echo [ОШИБКА] Папка backend не найдена.
    echo Убедитесь, что вы запускаете скрипт из корневой папки проекта.
    pause
    exit /b 1
)

if not exist frontend (
    echo [ОШИБКА] Папка frontend не найдена.
    echo Убедитесь, что вы запускаете скрипт из корневой папки проекта.
    pause
    exit /b 1
)

echo [INFO] Настройка бэкенда...

REM Создание виртуального окружения Python, если его нет
if not exist backend\venv (
    echo [INFO] Создание виртуального окружения Python...
    cd backend
    python -m venv venv
    cd ..
)

REM Активация виртуального окружения и установка зависимостей
echo [INFO] Установка Python-зависимостей...
cd backend
call venv\Scripts\activate.bat
pip install flask flask-cors Pillow requests
echo [INFO] Python-зависимости установлены

REM Создание необходимых папок
if not exist uploads mkdir uploads
if not exist uploads\characters mkdir uploads\characters
if not exist uploads\scenes mkdir uploads\scenes
if not exist uploads\temp mkdir uploads\temp

REM Запуск бэкенда в фоновом режиме
echo [INFO] Запуск бэкенда...
start cmd /k "venv\Scripts\activate.bat && python app.py"

REM Переход к настройке фронтенда
cd ..
echo.
echo [INFO] Настройка фронтенда...

REM Установка зависимостей для фронтенда
cd frontend
if not exist node_modules (
    echo [INFO] Установка Node.js зависимостей...
    npm install
    echo [INFO] Node.js зависимости установлены
) else (
    echo [INFO] Node.js зависимости уже установлены
)

REM Запуск фронтенда
echo [INFO] Запуск фронтенда...
start cmd /k "npm start"

cd ..
echo.
echo ===================================================
echo Приложение запущено!
echo Бэкенд доступен по адресу: http://localhost:5000
echo Фронтенд доступен по адресу: http://localhost:3000
echo.
echo Для остановки приложения закройте окна командной строки
echo ===================================================
echo.
echo Нажмите любую клавишу для выхода из этого окна...
pause >nul