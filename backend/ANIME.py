import requests
import time
from urllib.parse import urlparse, parse_qs

# Функция для получения id пользователя
def get_user_id(access_token):
    headers = {
        'User-Agent': 'MangaRecommendation',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://shikimori.one/api/users/whoami', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']
    else:
        print(f'Failed to get user ID. Status code: {response.status_code}')
        return None

# Функция для получения списка оцененных аниме пользователя с нормальными названиями
def get_user_anime_ratings(access_token):
    user_id = get_user_id(access_token)
    if user_id is not None:
        headers = {
            'User-Agent': 'MangaRecommendation',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(f'https://shikimori.one/api/v2/user_rates?user_id={user_id}', headers=headers)
        if response.status_code == 200:
            anime_ratings = response.json()
            anime_titles = []
            for rating in anime_ratings:
                anime_id = rating['target_id']
                anime_title = get_anime_title(anime_id, headers)
                anime_info = {
                    'title': anime_title,
                    'status': rating['status'],
                    'score': rating['score']
                }
                anime_titles.append(anime_info)
            return anime_titles
        else:
            print(f'Failed to get anime ratings. Status code: {response.status_code}')
            return None
    else:
        return None

# Функция для получения названия аниме по его id
def get_anime_title(anime_id, headers):
    response = requests.get(f'https://shikimori.one/api/animes/{anime_id}', headers=headers)
    if response.status_code == 200:
        anime_data = response.json()
        return anime_data['russian']  # Здесь можно выбрать русское или английское название
    elif response.status_code == 429:
        print('Слишком много запросов. Ждем 15 секунд...')
        time.sleep(15)  # Добавляем задержку в 15 секунд
        return get_anime_title(anime_id, headers)  # Повторяем запрос
    else:
        print(f'Не удалось получить аниме. Код статуса: {response.status_code}')
        return None

# Функция для получения access_token через процедуру аутентификации OAuth2
def get_access_token(client_id, client_secret, code, redirect_uri):
    headers = {
        'User-Agent': 'MangaRecommendation',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post('https://shikimori.one/oauth/token', headers=headers, data=data)
    if response.status_code == 200:
        access_token_data = response.json()
        return access_token_data.get('access_token')
    else:
        print(f'Failed to get access token. Status code: {response.status_code}')
        return None

# # Ссылка для аутентификации OAuth2
# auth_url = 'https://shikimori.one/oauth/authorize?client_id=krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F&response_type=code&scope=user_rates+topics'

# # Отправка запроса для аутентификации
# response_auth = requests.get(auth_url)
# Добавить хедер при запросе???
# print("response_auth: "+str(response_auth))
# # Получение URL-адреса, на который произойдет перенаправление
# redirect_url = response_auth.url

# # Извлечение параметров запроса из URL-адреса
# parsed_url = urlparse(redirect_url)
# query_params = parse_qs(parsed_url.query)

#Ошибка здесь "response_auth = requests.get(auth_url)", поэтому берет просто данную ссылку и ее парсит. То есть не переходит дальше

# Запрашиваем данные для аутентификации
client_id = "krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI"
client_secret = "JesmUCRQb2bBJY8cx-DMJcZych6NIJ2kv3jHbTXWBLg"
redirect_uri = "http://localhost:3000/profile"
code = input('Введите ваш код авторизации: ')
# # Извлечение кода авторизации из параметров запроса
# print("query_params: "+str(query_params))
# code = query_params.get('code')[0] if 'code' in query_params else None

# if code:
#     print(f'Код авторизации: {code}\n')
# else:
#     print('Не удалось получить код авторизации')

# Получаем access_token
access_token = get_access_token(client_id, client_secret, code, redirect_uri)

# access_token = 'ot9GN4FrRkYIeN5AaCo1T23P2-5ifJWcQbhYajTslFk'

# Получение списка оцененных аниме пользователя с нормальными названиями
anime_titles = get_user_anime_ratings(access_token)
if anime_titles is not None:
    print(anime_titles)

#Короче, поясняю. Нужно как-то получить код авторизации, который пишется при переходе по ссылке "https://shikimori.one/oauth/authorize?client_id=krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F&response_type=code&scope=user_rates+topics"
#Который ?code= Вот он. Парсить не получается у меня, нужно думать. Вариант выше в комментах не работает. Так что нужно пока вручную вводить перейдя
