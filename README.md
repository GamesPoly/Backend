## start app

```
python manage.py migrate
python manage.py runserver
```


## 📘 API Эндпоинты

### 🎮 Игры
- `GET    /api/games/` — список игр (поиск, фильтрация, сортировка)
- `POST   /api/games/` — создание новой игры
- `GET    /api/games/<id>/` — получить игру по ID
- `PUT    /api/games/<id>/` — полное обновление игры
- `PATCH  /api/games/<id>/` — частичное обновление игры
- `DELETE /api/games/<id>/` — удалить игру

### 🏷 Теги
- `GET /api/games/tags/` — список всех тегов

### 💻 Платформы
- `GET /api/games/platforms/` — список всех платформ