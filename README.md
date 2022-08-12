# Analyzing-IMDB-Top-250


There is a link of the top 250 films according to IMDB https://www.imdb.com/chart/top

## Task 1
- Collect movies released after 2000 into a `movies.json` file. For each movie collect the following data (look on the screenshot).
![photo_2022-08-09_16-39-00](https://user-images.githubusercontent.com/56909624/183663607-857ce17d-1646-478c-8c8e-7af486a7e94e.jpg)
- Save the data as list of dictionaries (1 dictionary == 1 movie).
- The list of the dictionaries in the file has to look like
```python
[{'a': 1, 'c': 3}, {'b': 2, 'd': 4}]
```
should become
```javascript
[
    {
        "a": 1,
        "c": 3
    },
    {
        "b": 2
        "d": 4
    }
]
```

## Task 2
- Read the json file and collect links of the movies into a list.
- Send a request to the link and parse the data of each movie the following figures (look on the screenshot).
![image](https://user-images.githubusercontent.com/56909624/184365294-908e0916-6c2f-429d-b483-c0d97029de71.png)
- Save the data in the dictionary in the format
```python
{'<movie_title>': {'year': ..., 'director': ... etc }}
```
