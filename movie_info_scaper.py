import json
import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

start_time = time.time()


async def get_data_from_file():
    movie_url = set()
    async with aiohttp.ClientSession() as session:
        with open('movies.json') as f:
            data = json.load(f)
            for url in data:
                movie_url.add(asyncio.ensure_future(get_movie_section_tag(session, url['movie_url'])))
            get_section_tags = await asyncio.gather(*movie_url)
            for section_tags in get_section_tags:
                print(parse_data(section_tags))


async def get_movie_section_tag(session, url):
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        movie_tags = soup.find('section', attrs={
            'class': 'ipc-page-section--baseAlt'})
        return movie_tags


def parse_data(section_tags):
    title = section_tags.h1.text
    year = [year.span.text for year in section_tags][1]
    hours = section_tags.find_all('li', class_="ipc-inline-list__item")[5].text
    rating = section_tags.find('div', class_='sc-80d4314-3').span.text
    popularity = section_tags.find('div', class_="sc-edc76a2-1 gopMqI").text
    genres = [genre.span.text for genre in
              section_tags.find_all('a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')]
    summary = section_tags.find('span', class_='gXUyNh').text
    get_movie_info = section_tags.find_all('ul',
                                           class_='ipc-inline-list ipc-inline-list--show-dividers '
                                                  'ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')
    directors = [director.a.text for director in get_movie_info[0]]
    writers = [writer.a.text for writer in get_movie_info[1]]
    stars = [star.a.text for star in get_movie_info[2]]
    return {title: {
        'year': year,
        'hours': hours,
        'rating': rating,
        'popularity': popularity,
        'genres': genres,
        'summary': summary,
        'director': directors,
        'writers': writers,
        'stars': stars
    }}


if __name__ == '__main__':
    asyncio.run(get_data_from_file())
    print("--- %s seconds ---" % (time.time() - start_time))
