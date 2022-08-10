import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

IMDB_ROOT_URL = 'http://www.imdb.com'


def get_movie_tags():
    imdb_top_url = urljoin(IMDB_ROOT_URL, '/chart/top')
    response = requests.get(imdb_top_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_tags = soup.find('tbody', attrs={'class': 'lister-list'}).find_all('tr')
    return movie_tags


def parse_movie_row(row):
    title = row.find('td', class_='titleColumn')
    image_url = row.find('td', class_='posterColumn').a.img.get('src')
    rating = row.find('td', class_='ratingColumn imdbRating').strong.text
    movie_title, movie_url, year, position = parse_movie_title(title)
    return movie_title, movie_url, year, image_url, position, rating


def parse_movie_title(movie):
    movie_title = movie.a.text
    year = movie.text.split()[-1].strip('()')
    movie_url = urljoin(IMDB_ROOT_URL, movie.a['href'])
    position = movie.text.split()[0].replace('.', '')
    return movie_title, movie_url, year, position


def extract_movie_props(row):
    movie_title, movie_url, year, image_url, position,  rating = parse_movie_row(row)
    return {'Title': movie_title, 'Film url': movie_url, 'Year': year, 'Image url': image_url,
            'Position': position, 'Rating': rating}


def main():
    movies_data = list()

    with open("movies.json", "w", encoding='utf8') as f:
        rows = get_movie_tags()
        for row in rows:
            movie_props = extract_movie_props(row)
            if int(movie_props['Year']) > 2000:
                movies_data.append(movie_props)
        json.dump(movies_data, f, indent=2)


if __name__ == '__main__':
    main()
