import time

import requests
from bs4 import BeautifulSoup
import sqlite3


def writheInfo(anime_id, Episodes, Genres, Themes):
    connection = sqlite3.connect('/Users/andrejsmirnov/PycharmProjects/GroupWebProject/backend/db.sqlite3')
    cursor = connection.cursor()

    sql_query = "INSERT INTO anime_info (anime_id, Episodes, Genres, Themes) " \
                "VALUES (?, ?, ?, ?)"
    cursor.execute(sql_query, (anime_id, Episodes, Genres, Themes))

    connection.commit()
    connection.close()


def get_anime_ids():
    connection = sqlite3.connect('/Users/andrejsmirnov/PycharmProjects/GroupWebProject/backend/db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT anime_id FROM anime_info')
    anime_info_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT anime_list_id FROM animes')
    anime_ids = [row[0] for row in cursor.fetchall()]

    connection.close()

    # Фильтруем уникальные anime_list_id, которых нет в таблице animes
    anime_ids_not_in_animes = [anime_id for anime_id in anime_ids if anime_id not in anime_info_ids]

    return anime_ids_not_in_animes


def get_info(anime_id):
    url = f'https://shikimori.one/animes/z{anime_id}'

    headers = {
        'User-Agent': 'AnimeRecommended'
    }
    response = requests.get(url, headers=headers)
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        entry_info = soup.findAll('div', class_='line-container')

        episodes_container, genres_container, themes_container = None, None, None
        for container in entry_info:
            key_element = container.find('div', class_='key')
            key_text = key_element.text.strip()
            if key_text == 'Эпизоды:':
                episodes_container = container.find('div', class_='value')
            if key_text == 'Жанры:' or key_text == 'Жанр:':
                genres_container = container.find('div', class_='value')
            if key_text == 'Темы:' or key_text == 'Тема:':
                themes_container = container.find('div', class_='value')

        print(anime_id)

        try:
            episodes = episodes_container.text.strip().split("/")[-1].strip()
        except:
            episodes = 1
        print("Количество эпизодов:", episodes)

        genre_elements = genres_container.find_all('span', class_='genre-ru')
        genres = ', '.join([genre.text.strip() for genre in genre_elements])
        print("Жанры:", genres)

        try:
            themes_elements = themes_container.find_all('span', class_='genre-ru')
            themes = ', '.join([themes.text.strip() for themes in themes_elements])
        except:
            themes = None
        print("Темы:", themes)
        writheInfo(anime_id, episodes, genres, themes)
        print("--------")


if __name__ == '__main__':
    print(get_anime_ids())
    '''for i in get_anime_ids():
        get_info(i)
        time.sleep(10)
'''