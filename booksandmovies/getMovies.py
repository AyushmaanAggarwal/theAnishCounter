import requests

def search_movies_name(name, count=15):
    movie_name = name.replace(" ", "+")
    with open("instance/movie_api", 'r') as file:
        api_key = file.read()
    req = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&s={movie_name}")
    numFound = req.json()["totalResults"]
    titles = [movie['Title'] for movie in req.json()["Search"][0:count]]
    year = [movie['Year'] for movie in req.json()["Search"][0:count]]
    imdbID = [movie['imdbID'] for movie in req.json()["Search"][0:count]]
    Poster = [movie['Poster'] for movie in req.json()["Search"][0:count]]

    output = list(map(list, zip(titles, year, imdbID, Poster)))
    return numFound, output

def get_movie_by_imdbid(id):
    with open("instance/movie_api", 'r') as file:
        api_key = file.read()
    req = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&i={id}")
    title = req.json()["Title"]
    year = req.json().get("Year", '')
    runtime = req.json().get("Runtime", '')
    director = req.json().get("Director", '')
    actors = req.json().get("Actors", '')
    plot = req.json().get("Plot", '')
    ratings = [item["Value"] for item in req.json().get("Ratings", '') if item["Source"]==("Rotten Tomatoes")]
    boxOffice = req.json().get("BoxOffice", '')
    poster = req.json().get("Poster", '')

    return [title, year, runtime, director, actors, plot, ratings, boxOffice, poster]

if __name__ == '__main__':
    print(search_movies_name("Dune"))
    print(get_movie_by_imdbid("tt1160419"))