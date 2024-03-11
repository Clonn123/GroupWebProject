import requests
from bs4 import BeautifulSoup
import sqlite3


def writheBD(title_en, title_ru, url_img, descriptionEpisod, descriptionData, anime_list_id):
    conn = sqlite3.connect('/Users/andrejsmirnov/PycharmProjects/GroupWebProject/backend/db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO animes (anime_list_id, title_en, title_ru, url_img, descriptionEpisod, descriptionData) VALUES ("
        "?, ?, ?, ?, ?, ?)",
        (anime_list_id, title_en, title_ru, url_img,
         descriptionEpisod, descriptionData))

    conn.commit()
    conn.close()


def update_rank(anime_id, rank):
    connection = sqlite3.connect('/Users/andrejsmirnov/PycharmProjects/GroupWebProject/backend/db.sqlite3')
    cursor = connection.cursor()

    sql_query = f"UPDATE animes SET score = ? WHERE anime_list_id = ?"
    cursor.execute(sql_query, (rank, anime_id))

    connection.commit()
    connection.close()


def scrape_rating():
    url = 'https://myanimelist.net/topanime.php?limit=50'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Найдем все элементы с классом 'ranking-list'
        ranking_lists = soup.find_all(class_='ranking-list')
        for ranking_list in ranking_lists:
            anime_rank = ranking_list.find(class_='js-top-ranking-score-col di-ib al').span.text.strip()
            anime_list_id = ranking_list.find(class_='hoverinfo_trigger fl-l ml12 mr8')['id'][5:]

            update_rank(anime_list_id, anime_rank)


def scrape_top_anime():
    url = 'https://shikimori.one/animes/page/5'

    headers = {
        'User-Agent': 'AnimeRecommended'
    }

    response = requests.get(url, headers=headers)
    ss = BeautifulSoup(response.text, 'html.parser')

    titles = []

    articles = ss.select('article[class*="c-column b-catalog_entry c-anime"]')

    for article in articles:
        title_data = {}

        # Получаем название
        title_element = article.find('span', class_='name-en')
        if title_element:
            title_data['name_en'] = title_element.text.strip()

        # Получаем русское название
        title_ru_element = article.find('span', class_='name-ru')
        if title_ru_element:
            title_data['name_ru'] = title_ru_element.text.strip()

        # Получаем тип (TV Сериал, Фильм и т.д.)
        misc_elements = article.find_all('span', class_='misc')
        if misc_elements:
            type_element = misc_elements[0].find('span')
            if type_element:
                title_data['type'] = type_element.text.strip()

        # Получаем ссылку на изображение
        img_element = article.find('img')
        if img_element:
            title_data['image_url'] = img_element['src']

        year = article.find('meta', itemprop='dateCreated')['content'].split('-')[0]
        if year:
            title_data['year'] = year

        # Получаем ссылку на страницу
        a_element = article.find('a', class_='cover')
        if a_element:
            title_data['url'] = a_element['href']

        # Получаем ID
        if 'id' in article.attrs:
            title_data['id'] = article['id']

        titles.append(title_data)

    for title in titles:
        writheBD(title['name_en'], title['name_ru'], title['image_url']
                 , title['type'], title['year'], title['id'])
        print(title)
    print(len(titles))


if __name__ == '__main__':
    scrape_rating()
