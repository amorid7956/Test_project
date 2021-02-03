# Test_project
### 1) Клонирум файлы ветки master данного репозитория в папку своего локального компьютера
`git clone git@github.com:amorid7956/Test_project.git`
### 2) Заходим в папку проекта:
`cd Test_project`
### 3) Создаём виртуальное окружение:
`virtualenv venv`
### 4) Активируем виртуальное окружение:
`venv/Scripts/activate`
### 5) Теперь, устанавливаем зависимости в ВО:
`pip install -r requirements.txt`
### 6) Так как уже есть сформированная миграция, то просто выполняем:
`manage.py migrate`
### 7) Запускаем отладочный сервер:
`manage.py runserver`
