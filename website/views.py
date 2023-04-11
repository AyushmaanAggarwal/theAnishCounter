from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import date, datetime, time, timedelta, timezone
from .models import Counter, Movie, Book, Event, Announcement
from booksandmovies.getBooks import *
from booksandmovies.getMovies import *
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/counter')
@login_required
def counter():
    counters = Counter.query.order_by(Counter.counts.desc()).all()
    return render_template("counter.html", user=current_user, counters=counters)

@views.route('/new-counter', methods=['POST', 'GET'])
@login_required
def new_counter():
    if request.method == 'POST':
        counterName = request.form.get('counterName')
        description = request.form.get('description')

        counter = Counter.query.filter_by(counterName=counterName).first()
        if counter:
            flash("Counter already exists with that name.", category='error')
        elif len(counterName) == 0:
            flash("Please add a name.", category='error')
        elif len(description) == 0:
            flash("Please add a description.", category='error')
        else:
            new_counter = Counter(counterName=counterName, description=description, counts=0)
            db.session.add(new_counter)
            db.session.commit()
            flash("Counter created!", category='success')
            return redirect(url_for('views.counter'))
    return render_template("new_counter.html", user=current_user)

@views.route('/increase-counter', methods=['POST'])
def increase_counter():
    counter = json.loads(request.data)
    counterId = counter['counterId']
    increase = counter['increase']
    counter = Counter.query.get(counterId)
    if counter:
        if increase:
            counter.counts = counter.counts + 1
        else:
            counter.counts = counter.counts - 1
        db.session.commit()
        return jsonify({})

@views.route('/delete-counter', methods=['POST'])
def delete_counter():
    counter = json.loads(request.data)
    counterId = counter['counterId']
    counter = Counter.query.get(counterId)
    if counter:
        counter.counterName = "." + counter.counterName
        db.session.commit()
        return jsonify({})

@views.route('/movies')
@login_required
def movies():
    movies = Movie.query.order_by(Movie.likes.desc()).all()
    pastMovies = any([movie.title[0]=='.' for movie in movies])

    return render_template("movies.html", user=current_user, movies=movies, pastMovies=pastMovies)

@views.route('/search-movie', methods=['POST', 'GET'])
@login_required
def search_movie():
    output = False
    if request.method == 'POST':
        amount, output = search_movies_name(request.form.get('movieName'))

    return render_template("search_movie.html", user=current_user, search_result=output, str=str)

@views.route('/add-movie', methods=['POST'])
@login_required
def add_movie():
    movie_dict = json.loads(request.data)
    movie_list = movie_dict['movie']
    print(movie_list)
    movie_data = get_movie_by_imdbid(movie_list[2])
    print(movie_data)
    new_movie = Movie(title=movie_list[0], year=movie_list[1], runtime=movie_data[2], posterUrl=movie_list[3], plot=movie_data[5], rating=str(movie_data[6]), imdb_id=movie_list[2], likes=0, creator_id=current_user.id)
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({})

@views.route('/like-movie', methods=['POST'])
def like_movie():
    movie = json.loads(request.data)
    movieId = movie['movieId']
    increase = movie['increase']
    movie = Movie.query.get(movieId)
    if movie:
        if increase:
            movie.likes = movie.likes + 1
            movie.likedUsers.append(current_user)
        else:
            movie.likes = movie.likes - 1
            movie.likedUsers.remove(current_user)  
        db.session.commit()
        return jsonify({})


@views.route('/books')
@login_required
def books():
    books = Book.query.order_by(Book.likes.desc()).all()
    pastBooks = any([book.bookTitle[0]=='.' for book in books])
    currentBooks = any([book.bookTitle[0]=='_' for book in books])
    bookClubAnnouncement = Announcement.query.filter_by(type="book club").order_by(Announcement.post_date.desc()).first().description
    dateAnnouncement = Announcement.query.filter_by(type="book club").order_by(Announcement.post_date.desc()).first().post_date.strftime("%b %d, %Y")
    return render_template("books.html", user=current_user, books=books, get_book_cover=get_book_cover, load=json.loads, pastBooks=pastBooks, currentBooks=currentBooks, announcement=bookClubAnnouncement, date=dateAnnouncement)

@views.route('/search-book', methods=['POST', 'GET'])
@login_required
def search_book():
    output = False
    if request.method == 'POST':
        amount, output = search_book_name(request.form.get('bookName'))
    return render_template("search_book.html", user=current_user, search_result=output, str=str)


@views.route('/add-book', methods=['POST'])
@login_required
def add_book():
    book_dict = json.loads(request.data)
    book_list = book_dict['book']
    print(book_list)
    new_book = Book(bookTitle=book_list[0], author=json.dumps(book_list[1]), publishYear=book_list[2],
                    isbn=book_list[3], cover_id=book_list[4], olid=book_list[5], likes=0, creator_id=current_user.id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({})


@views.route('/like-book', methods=['POST'])
def like_book():
    book = json.loads(request.data)
    bookId = book['bookId']
    increase = book['increase']
    book = Book.query.get(bookId)
    if book:
        if increase:
            book.likes = book.likes + 1
            book.likedUsers.append(current_user)
        else:
            book.likes = book.likes - 1
            book.likedUsers.remove(current_user)
        db.session.commit()
        return jsonify({})


def delete_old_events(app):
    with app.app_context():
        pst_tz = timezone(offset=-timedelta(hours=8))
        curr_time = datetime.now(pst_tz)
        for event in Event.query.all():
            if event.date < curr_time.date():
                db.session.delete(event)
                db.session.commit()


def sort_by_datetime(object_to_compare):
    date_ = object_to_compare.date
    time_ = object_to_compare.time
    return datetime(date_.year, date_.month, date_.day, hour=time_.hour, minute=time_.minute)


@views.route('/events', methods=['GET', 'POST'])
def events():
    events_ = sorted(Event.query.all(), key=sort_by_datetime)
    today_events = sorted(Event.query.filter_by(date=date.today()).all(), key=sort_by_datetime)
    # Both lists have the same first items, so we can just pop a certain number of times to avoid repeats
    for i in range(len(today_events)):
        events_.pop(0)
    return render_template("events.html", user=current_user, today_events=today_events, events=events_, fmttime=datetime.strptime)


@views.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form.get('eventTitle')
        date_ = date.fromisoformat(request.form.get('eventDate'))
        as_datetime = datetime.strptime(request.form.get('eventTime'), "%H:%M")
        time_ = time(hour=as_datetime.hour, minute=as_datetime.minute)
        location = request.form.get('eventLocation')
        description = request.form.get('description')
        new_event = Event(title=title, date=date_, time=time_, location=location, description=description)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('views.events'))
    return render_template("new_event.html", user=current_user)
