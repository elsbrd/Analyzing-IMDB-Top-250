import os
import json
import asyncio

import aiohttp
from bs4 import BeautifulSoup

CURRENT_DIR = os.path.dirname(__file__)

MOVIES_DATA_PATH = os.path.join(CURRENT_DIR, "movies.json")
MOVIES_DESCRIPTION_PATH = os.path.join(CURRENT_DIR, "movies_description.json")


def get_urls() -> {}:
    """
    Reads the json file with the data of films

    return:
        Movie urls
    """

    with open(MOVIES_DATA_PATH) as f:
        return {movie["movie_url"] for movie in json.load(f)}


async def get_data_from_url(url: str, session) -> dict:
    """
    Gets the movie info asynchronously from the url

    param url:
        Gets the url from the website
    param session:
        Aiohttp ClientSession sample

    return:
        A dictionary with all the details of a film
    """

    async with session.get(url) as response:
        return parse_data_from_response(await response.text())


def parse_data_from_response(response_text: str) -> dict:
    """
    Parses the data from the response

    param response_text:
        A str response of a specific movie

    return:
         A dictionary with all the details of a film
    """

    soup = BeautifulSoup(response_text, "html.parser")

    section_tags = soup.find("section", attrs={"class": "ipc-page-section--baseAlt"})

    title = section_tags.h1.text
    year = [year.span.text for year in section_tags][1]
    hours = section_tags.find_all("li", class_="ipc-inline-list__item")[5].text
    rating = section_tags.find("div", class_="sc-80d4314-3").span.text
    popularity = section_tags.find("div", class_="sc-edc76a2-1 gopMqI").text
    genres = [
        genre.span.text
        for genre in section_tags.find_all(
            "a", class_="sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt"
        )
    ]
    summary = section_tags.find("span", class_="gXUyNh").text
    get_movie_info = section_tags.find_all(
        "ul",
        class_="ipc-inline-list ipc-inline-list--show-dividers "
        "ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt",
    )
    directors = [director.a.text for director in get_movie_info[0]]
    writers = [writer.a.text for writer in get_movie_info[1]]
    stars = [star.a.text for star in get_movie_info[2]]
    return {
        title: {
            "year": year,
            "hours": hours,
            "rating": rating,
            "popularity": popularity,
            "genres": genres,
            "summary": summary,
            "director": directors,
            "writers": writers,
            "stars": stars,
        }
    }


async def main():
    """
    Runs the method asynchronously
    """

    async with aiohttp.ClientSession() as session:
        tasks = list()
        for url in get_urls():
            tasks.append(asyncio.ensure_future(get_data_from_url(url, session)))

        movies_data = await asyncio.gather(*tasks)

        with open(MOVIES_DESCRIPTION_PATH, "w", encoding="utf8") as f:
            json.dump(movies_data, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
