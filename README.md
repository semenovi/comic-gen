# Генератор аниме-изображений

Приложение для генеративного создания изображений в аниме-стиле с сохранением узнаваемости персонажей.

## Особенности

- Сохранение узнаваемости персонажа при генерации разных сцен
- Генерация персонажей на нейтральном фоне
- Генерация сюжетных картинок с выбранным персонажем
- Модульная архитектура для легкого добавления новых функций
- Веб-интерфейс для удобного использования

## Структура проекта

```
project
├── backend               # Бэкенд на Flask
│   ├── app.py             # Основное приложение Flask
│   ├── modules           # Модули для генерации изображений
│   ├── utils             # Вспомогательные утилиты
│   └── requirements.txt   # Python-зависимости
├── frontend              # Фронтенд на React
│   ├── public            # Статические файлы
│   ├── src               # Исходный код React
│   └── package.json       # Node.js зависимости
└── README.md              # Эта инструкция
```

## Требования

- Python 3.8 или выше
- Node.js 14 или выше
- NVIDIA GPU (рекомендуется) для ускорения генерации
- 10+ ГБ свободного места на диске для моделей

## Установка и запуск

### Бэкенд

1. Создайте виртуальное окружение Python
   ```bash
   cd backend
   python -m venv venv
   ```

2. Активируйте виртуальное окружение
   - Windows `venvScriptsactivate`
   - LinuxMac `source venvbinactivate`

3. Установите зависимости
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите сервер
   ```bash
   python app.py
   ```

Бэкенд будет доступен по адресу httplocalhost5000

### Фронтенд

1. Установите зависимости
   ```bash
   cd frontend
   npm install
   ```

2. Запустите сервер разработки
   ```bash
   npm start
   ```

Фронтенд будет доступен по адресу httplocalhost3000

## Использование

1. После запуска перейдите в браузере по адресу httplocalhost3000
2. На первом экране вы увидите статус зависимостей и моделей. Нажмите кнопку Установить все, чтобы загрузить необходимые модели.
3. После установки вы можете
   - Перейти на вкладку Создать персонажа для генерации персонажей
   - Перейти на вкладку Создать сцену для генерации сюжетных изображений с существующими персонажами

## Технические детали

Проект использует следующие ключевые технологии

- Бэкенд
  - Flask для веб-сервера
  - Stable Diffusion для генерации изображений
  - ControlNet для сохранения узнаваемости персонажей
  - IP-Adapter для работы с референсами персонажей

- Фронтенд
  - React для пользовательского интерфейса
  - React Router для навигации
  - Axios для HTTP-запросов

## Расширение функциональности

Благодаря модульной архитектуре, вы можете легко добавить новые функции

1. Для добавления модуля предобработки или постобработки, создайте новый класс в папке `backendmodules`
2. Реализуйте интерфейс базового модуля с методами `process` и `save`
3. Подключите новый модуль в основном приложении `app.py`

## Лицензия

Этот проект распространяется под лицензией MIT.