from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Counter, Movie
from . import db
import json
from website.auth import verification_required

views = Blueprint('views', __name__)

@views.route('/')
@login_required
@verification_required(current_user)
def home():
    return render_template("home.html", user=current_user)

@views.route('/counter')
@login_required
@verification_required(current_user)
def counter():
    counters = Counter.query.all()
    return render_template("counter.html", user=current_user, counters=counters)

@views.route('/new-counter', methods=['POST', 'GET'])
@login_required
@verification_required(current_user)
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
        db.session.delete(counter)
        db.session.commit()
        return jsonify({})

@views.route('/movies')
@login_required
@verification_required(current_user)
def movies():
    movies = Movie.query.all()
    return render_template("movies.html", user=current_user, movies=movies)

@views.route('/add-movie', methods=['POST', 'GET'])
@login_required
@verification_required(current_user)
def add_movie():
    if request.method == 'POST':
        movieName = request.form.get('movieName')
        releaseYear = request.form.get('releaseYear')

        movie = Movie.query.filter_by(movieName=movieName, releaseYear=releaseYear).first()
        if movie:
            flash("Movie has already been suggested.", category='error')
        elif len(movieName) == 0:
            flash("Please add a name.", category='error')
        elif releaseYear == 0:
            flash("Please add a year of release.", category='error')
        else:
            new_movie = Movie(movieName=movieName, releaseYear=releaseYear, description="", 
                              runtime="", likes=0)
            db.session.add(new_movie)
            db.session.commit()
            flash("Movie added!", category='success')
            return redirect(url_for('views.movies'))
    return render_template("add_movie.html", user=current_user)

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