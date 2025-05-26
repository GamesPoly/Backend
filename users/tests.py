import pytest
from rest_framework.test import APIClient
from users.models import User

# Фикстура, возвращающая клиент для API-запросов
@pytest.fixture
def api():
    return APIClient()



# ✅ Тест успешной регистрации пользователя
# Проверяет, что при валидных данных возвращается статус 201 и токен
@pytest.mark.django_db
def test_register_user_success(api):
    response = api.post('/api/users/register/', {
        "username": "pytestuser",
        "email": "pytest@example.com",
        "password": "pytestpass123"
    }, format='json')
    assert response.status_code == 201
    assert 'token' in response.data



# ❌ Тест невалидного email при регистрации
# Проверяет, что при некорректном email возвращается 400 и сообщение об ошибке
@pytest.mark.django_db
def test_register_user_invalid_email(api):
    response = api.post('/api/users/register/', {
        "username": "pytestuser",
        "email": "not-an-email",
        "password": "pytestpass123"
    }, format='json')
    assert response.status_code == 400
    assert 'email' in response.data



# ❌ Тест короткого пароля при регистрации
# Убеждается, что короткий пароль вызывает ошибку валидации
@pytest.mark.django_db
def test_register_user_short_password(api):
    response = api.post('/api/users/register/', {
        "username": "pytestuser",
        "email": "short@example.com",
        "password": "123"
    }, format='json')
    assert response.status_code == 400
    assert 'password' in response.data



# ✅ Тест успешного логина
# Проверяет, что корректный email и пароль дают токен доступа
@pytest.mark.django_db
def test_login_success(api):
    User.objects.create_user(username="loginuser", email="login@example.com", password="correctpass123")
    response = api.post('/api/users/login/', {
        "email": "login@example.com",
        "password": "correctpass123"
    }, format='json')
    assert response.status_code == 200
    assert 'token' in response.data



# ❌ Тест логина с неверным паролем
# Убеждается, что неправильный пароль вызывает ошибку авторизации
@pytest.mark.django_db
def test_login_wrong_password(api):
    User.objects.create_user(username="loginuser", email="login@example.com", password="correctpass123")
    response = api.post('/api/users/login/', {
        "email": "login@example.com",
        "password": "wrongpass"
    }, format='json')
    assert response.status_code == 401
    assert 'error' in response.data



# 🔐 Тест доступа к защищённому эндпоинту
# Проверяет, что доступ без токена запрещён, а с токеном — разрешён
@pytest.mark.django_db
def test_protected_endpoint_requires_auth(api):
    user = User.objects.create_user(username="secureuser", email="secure@example.com", password="pass123secure")
    response = api.post('/api/users/login/', {
        "email": "secure@example.com",
        "password": "pass123secure"
    }, format='json')
    token = response.data['token']

    # Без токена — должен отказать
    unauthorized = api.get('/api/users/protected/')
    assert unauthorized.status_code == 401

    # С токеном — должен пустить
    api.credentials(HTTP_AUTHORIZATION='Token ' + token)
    authorized = api.get('/api/users/protected/')
    assert authorized.status_code == 200
    assert 'Привет' in authorized.data['message']



# 🚪 Тест выхода пользователя (logout)
# Проверяет, что при logout токен удаляется и доступ становится невозможен
@pytest.mark.django_db
def test_logout_removes_token(api):
    user = User.objects.create_user(username="logoutuser", email="logout@example.com", password="logoutpass123")
    login = api.post('/api/users/login/', {
        "email": "logout@example.com",
        "password": "logoutpass123"
    }, format='json')
    token = login.data['token']

    # Авторизуемся
    api.credentials(HTTP_AUTHORIZATION='Token ' + token)

    # Вызываем logout
    response = api.post('/api/users/logout/')
    assert response.status_code == 200
    assert response.data['message'] == 'Вы вышли из системы'

    # Проверим, что токен действительно удалён
    response2 = api.get('/api/users/protected/')
    assert response2.status_code == 401
