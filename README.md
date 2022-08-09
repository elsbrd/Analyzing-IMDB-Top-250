# Analyzing-IMDB-Top-250
There is a link from the top 250 films according to IMDB https://www.imdb.com/chart/top
The task:
1. Collect movies released after 2000 into a `movies.json` file. For each movie collect the following data (look on the screenshot).
2. Save the ![photo_2022-08-09_16-39-00](https://user-images.githubusercontent.com/56909624/183663607-857ce17d-1646-478c-8c8e-7af486a7e94e.jpg)
data as list of dictionaries (1 dictionary == 1 movie)
3. The list of dictionaries in the file has to look like:
[{'a': 1, 'c': 3}, {'b': 2, 'd': 4}]
should become
[
    {
        "a": 1,
        c: 3
    },
    {
        "b": 2
        "d": 4
    }
]
