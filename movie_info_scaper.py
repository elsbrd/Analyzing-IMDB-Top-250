import requests
import json
import asyncio
from bs4 import BeautifulSoup


def get_data_from_file():
    movie_url = list()
    with open('movies.json') as f:
        data = json.load(f)
        for row in data:
            movie_url.append(row['movie_url'])
    return movie_url


async def create_schedule():
    for i in get_data_from_file():
        await extract_movie_props(i)


def get_movie_tags(row):
    response = requests.get(row)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_tags = soup.find('section', attrs={
        'class': 'ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs '
                 'sc-2a827f80-1 gvCXlM'})
    return movie_tags


def parse_data(row):
    movie_tags = get_movie_tags(row)
    title = movie_tags.find('div', class_='sc-80d4314-1 fbQftq').h1.text
    year = movie_tags.find('div', class_='sc-80d4314-1 fbQftq').a.text
    hours = list(map(lambda x: x.text, movie_tags.find_all('li', class_="ipc-inline-list__item")))[5]
    rating = movie_tags.find('div', class_='sc-db8c1937-1 kVSEMR').span.text
    popularity = movie_tags.find('div', class_="sc-edc76a2-1 gopMqI").text
    info_film_type = list(
        map(lambda x: x.span.text, movie_tags.find_all('a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')))
    summary = movie_tags.find('span', class_='sc-16ede01-0 fMPjMP').text
    get_movie_info = movie_tags.find_all('ul',
                                         class_='ipc-inline-list ipc-inline-list--show-dividers '
                                                'ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')
    director = list(map(lambda x: x.a.text, get_movie_info[0]))
    writers = list(map(lambda x: x.a.text, get_movie_info[1]))
    stars = list(map(lambda x: x.a.text, get_movie_info[2]))
    return title, year, hours, rating, popularity, info_film_type, summary, director, writers, stars


async def extract_movie_props(row):
    title, year, hours, rating, popularity, info_film_type, summary, director, writers, stars = parse_data(row)
    return {title: {
        'year': year,
        'hours': hours,
        'rating': rating,
        'popularity': popularity,
        'info_film_type': info_film_type,
        'summary': summary,
        'director': director,
        'writers': writers,
        'stars': stars
    }}


if __name__ == '__main__':
    asyncio.run(create_schedule())
