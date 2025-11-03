# Инструкция по деплою на GitHub

## Быстрый старт

### 1. Инициализация Git (если еще не сделано)

```bash
git init
```

### 2. Добавление remote репозитория

```bash
git remote add origin https://github.com/jfsagro-glitch/AIC.git
```

### 3. Добавление всех файлов

```bash
git add .
```

### 4. Создание первого коммита

```bash
git commit -m "Initial commit: AI Залоговик - система оценки недвижимости"
```

### 5. Переименование ветки в main (если нужно)

```bash
git branch -M main
```

### 6. Загрузка на GitHub

```bash
git push -u origin main
```

## Если возникают конфликты

Если репозиторий не пустой, нужно сначала сделать pull:

```bash
git pull origin main --allow-unrelated-histories
```

Затем push:

```bash
git push -u origin main
```

## Структура проекта на GitHub

После загрузки структура будет следующей:

```
AIC/
├── .github/
│   └── workflows/          # GitHub Actions для CI/CD
├── frontend/               # React приложение
├── backend/                # FastAPI сервер
├── ai_core/                # Расчетные модули
├── docker-compose.yml      # Docker конфигурация
├── README.md               # Документация
└── .gitignore             # Игнорируемые файлы
```

## GitHub Actions

В проекте настроены автоматические workflow:
- `deploy.yml` - тестирование и сборка при изменении кода
- `docker-build.yml` - сборка Docker образов

Они автоматически запустятся при push в main/master ветку.

