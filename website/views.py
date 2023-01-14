from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Counter
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
    counters = Counter.query.all()
    return render_template("counter.html", user=current_user, counters=counters)

@views.route('/new-counter', methods=['POST', 'GET'])
@login_required
def new_counter():
    if request.method == 'POST':
        counterName = request.form.get('counterName')
        description = request.form.get('description')

        counter = Counter.query.filter_by(counterName=counterName).first()
        if counter:
            flash("Counter already existed with that name.", category='error')
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
    counter = Counter.query.get(counterId)
    if counter:
        counter.counts = counter.counts + 1
        db.session.commit()
        return jsonify({})