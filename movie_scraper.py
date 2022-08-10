from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin

IMDB_ROOT_URL = 'http://www.imdb.com'


def get_movie_tags():
    imdb_top_url = urljoin(IMDB_ROOT_URL, '/chart/top')
    response = requests.get(imdb_top_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    get_tbody = soup.find('tbody', attrs={'class': 'lister-list'})
    rows = get_tbody.find_all('tr')
    return rows


def parse_movie_row(row):
    movie = row.find('td', {'class': 'titleColumn'})
    image_url = row.find('td', {'class': 'posterColumn'}).a.img.get('src')
    rating = row.find('td', {'class': 'ratingColumn imdbRating'}).strong.text
    title, movie_url, year, position = get_movie_table_rows(movie)
    return title, movie_url, year, image_url, position,  rating


def get_movie_table_rows(movie):
    title = movie.a.text
    year = movie.text.split()[-1].replace('(', '').replace(')', '')
    movie_url = urljoin(IMDB_ROOT_URL, movie.a['href'])
    position = movie.text.split()[0].replace('.', '')
    return title, movie_url, year, position


def extract_movie_props(row):
    title, movie_url, year, image_url, position,  rating = parse_movie_row(row)
    return {'Title': title, 'Film url': movie_url, 'Year': year, 'Image url': image_url,
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
