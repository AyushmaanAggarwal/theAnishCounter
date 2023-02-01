import requests

def search_book_name(name, count=15):
    book_name = name.replace(" ", "+")
    req = requests.get(f"http://openlibrary.org/search.json?q={book_name}")
    numFound = req.json()["numFound"]
    titles = [book['title'] for book in req.json()["docs"][0:count]]
    authors = [book.get('author_name', "") for book in req.json()["docs"][0:count]]
    year = [book.get('first_publish_year', 0) for book in req.json()["docs"][0:count]]
    ISBN = [book.get('isbn', [""])[0] for book in req.json()["docs"][0:count]]
    Cover_ID = [book.get('cover_i', "") for book in req.json()["docs"][0:count]]
    OLID = [book.get('edition_key', "")[0] for book in req.json()["docs"][0:count]]
    output = list(map(list, zip(titles, authors, year, ISBN, Cover_ID, OLID)))
    return numFound, output

def get_book_cover(cover_id, size='M'):
    return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"

if __name__ == '__main__':
    print(get_book_cover(240727))
