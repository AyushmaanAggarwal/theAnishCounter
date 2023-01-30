import requests

def search_movies_name(name, count=15):
    movie_name = name.replace(" ", "+")
    with open("../instance/movie_api", 'r') as file:
        api_key = file.read()
    req = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&s={movie_name}")
    numFound = req.json()["totalResults"]
    titles = [book['Title'] for book in req.json()["Search"][0:count]]
    year = [book['year'] for book in req.json()["Search"][0:count]]
    imdbID = [book['imdbID'] for book in req.json()["Search"][0:count]]
    Poster = [book['Poster'] for book in req.json()["Search"][0:count]]

    output = list(map(list, zip(titles, year, imdbID, Poster)))
    return numFound, output

def get_movie_by_imdbid(id):
    with open("../instance/movie_api", 'r') as file:
        api_key = file.read()
    req = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&i={id}")
    title = req.json()["Title"]
    year = req.json()["Year"]
    runtime = req.json()["Runtime"]
    director = req.json()["Director"]
    actors = req.json()["Actors"]
    plot = req.json()["Plot"]
    ratings = [item["Value"] for item in req.json()["Ratings"] if item["Source"].equals("Rotten Tomatoes")]
    boxOffice = req.json()["BoxOffice"]
    poster = req.json()["Poster"]

    return list(map(list, zip(title, year, runtime, director, actors, plot, ratings, boxOffice, poster)))

if __name__ == '__main__':
    print("")