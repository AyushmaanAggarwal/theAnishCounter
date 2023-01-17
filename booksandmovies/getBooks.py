import requests

def search_book_name(name, count=15):
    book_name = name.replace(" ", "+")
    req = requests.get(f"http://openlibrary.org/search.json?title={name}")
    numFound = req.json()["numFound"]
    titles = [book['title'] for book in req.json()["docs"][0:count]]
    authors = [book['author_name'] for book in req.json()["docs"][0:count]]
    year = [book['first_publish_year'] for book in req.json()["docs"][0:count]]
    ISBN = [book['isbn'][0] for book in req.json()["docs"][0:count]]
    Cover_ID = [book['cover_i'] for book in req.json()["docs"][0:count]]
    OLID = [book['edition_key'][0] for book in req.json()["docs"][0:count]]
    output = list(zip(titles, authors, year, ISBN, Cover_ID, OLID))
    return numFound, output

def get_book_cover(cover_id, size='L'):
    return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"

if __name__ == '__main__':
    print(get_cover(240727))
