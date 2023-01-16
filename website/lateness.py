from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Counter, Movie, User
from . import db
import json
import datetime

lateness = Blueprint('lateness', __name__)


@lateness.route('/lateness_tracker', methods=['GET', 'POST'])
@login_required
def lateness_home():
    all_users = User.query.all()

    if request.method == 'POST':
        minutes_late = datetime.datetime.now().minute - 10

    return render_template('lateness_tracker.html', all_users=all_users)
