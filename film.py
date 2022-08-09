from bs4 import BeautifulSoup
import requests
import json
# title, picture url, position in top 250, year released, rating, url inside the title


def get_movie_soup():
    url = 'http://www.imdb.com/chart/top'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('tbody', attrs={'class': 'lister-list'})
    rows = table.find_all('tr')
    return rows

def get_imd_movies(i):
    movie = i.find_all('td', class_='titleColumn')[0]
    image_url = i.find_all('td', class_='posterColumn')[0].a.img.get('src')
    rating = i.find_all_next('td', class_='ratingColumn imdbRating')[0].strong.text
    return movie, image_url, rating


def get_imd_movie_info(movie):
    movie_title = movie.a.text
    movie_year = movie.text.split()[-1].replace('(', '').replace(')', '')
    movie_url = 'http://www.imdb.com' + movie.a['href']
    movie_position = movie.text.split()[0].replace('.', '')
    return movie_title, movie_year, movie_url, movie_position


def writing_data(movie_title, movie_url, movie_year, image_url, movie_position, rating):
    my_dict = {'Title': movie_title, 'Film url': movie_url, 'Year': movie_year, 'Image url': image_url,
               'Position': movie_position, 'Rating': rating}

    json_object = json.dumps(my_dict, indent=4) # encoding problems

    # example
    #string = json.loads(b'"\\u041a\\u0435\\u0439\\u0442\\u043b\\u0438\\u043d\\u043f\\u0440\\u043e"'.decode('utf8'))
    #print(string)

    with open("movies.json", "w") as outfile:
        outfile.write(json_object)


def imd_movie_picker():
    rows = get_movie_soup()
    for i in rows:
        movie, image_url, rating = get_imd_movies(i)
        movie_title, movie_year, movie_url, movie_position = get_imd_movie_info(movie)
        if movie_year > '2000':
            writing_data(movie_title, movie_url, movie_year, image_url, movie_position, rating)


if __name__ == '__main__':
    imd_movie_picker()
