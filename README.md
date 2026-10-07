# Task Tracker API

REST API для таск-трекера на Django REST Framework. Є дошки (Board), задачі на них (Task) і коментарі до задач (Comment).
Читати дані може будь-хто, створювати задачі й коментарі — лише залогінені користувачі, а змінювати чи видаляти запис — тільки його власник.
Списки підтримують фільтрацію, пошук, сортування і пагінацію.

## Запуск локально

```
python -m venv .venv
.venv\Scripts\activate          # macOS / Linux: source .venv/bin/activate
cd task_api
pip install -r requirements.txt
copy .env.example .env          # macOS / Linux: cp .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
```

У файлі `.env` вкажіть власний `SECRET_KEY` і `DEBUG=True` для локальної роботи.

Команда `seed` створює 3 дошки, 8 задач, 4 коментарі та двох користувачів: `anna` і `bohdan` (пароль в обох `pass12345`).
Повторний запуск нічого не дублює.

Корінь API: http://127.0.0.1:8000/api/ . Увійти в Browsable API: http://127.0.0.1:8000/api-auth/login/

## Ендпоінти

| Метод | Адреса | Що робить | Хто може |
|-------|--------|-----------|----------|
| GET | /api/boards/ | список дошок, пошук | усі (read-only) |
| GET | /api/boards/<id>/ | одна дошка | усі (read-only) |
| GET | /api/tasks/ | список задач, фільтри | усі |
| POST | /api/tasks/ | створити задачу | залогінені |
| GET | /api/tasks/<id>/ | одна задача | усі |
| PUT / PATCH | /api/tasks/<id>/ | змінити задачу | тільки власник |
| DELETE | /api/tasks/<id>/ | видалити задачу | тільки власник |
| GET | /api/tasks/overdue/ | прострочені невиконані задачі | усі |
| GET | /api/comments/ | список коментарів, фільтри | усі |
| POST | /api/comments/ | створити коментар | залогінені |
| GET | /api/comments/<id>/ | один коментар | усі |
| PUT / PATCH | /api/comments/<id>/ | змінити коментар | тільки власник |
| DELETE | /api/comments/<id>/ | видалити коментар | тільки власник |

## Фільтри, пошук, сортування

| Запит | Результат |
|-------|-----------|
| /api/tasks/?status=done | задачі з певним статусом (`todo`, `in_progress`, `done`) |
| /api/tasks/?board=1 | задачі однієї дошки |
| /api/tasks/?owner=1 | задачі одного користувача |
| /api/tasks/?search=звіт | пошук за назвою задачі та назвою дошки |
| /api/tasks/?ordering=-deadline | сортування за `deadline` або `start_date`, мінус — за спаданням |
| /api/tasks/?board=1&ordering=deadline&page=2 | параметри комбінуються |
| /api/comments/?task=1 | коментарі до однієї задачі |
| /api/comments/?search=рейси | пошук за текстом коментаря |
| /api/boards/?search=work | пошук дошки за назвою |

Списки приходять сторінками по 10 записів у форматі `count / next / previous / results`.

## Перевірки даних

- Назва задачі — щонайменше 3 символи.
- Дедлайн задачі не може бути раніше дати початку.
- Коментар не може бути порожнім.

## Тести

```
python manage.py test tasks
```