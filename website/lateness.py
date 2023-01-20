from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Lateness
from . import db
import json
import datetime

late = Blueprint('late', __name__)

dates = [datetime.date(2023, 1, 18), datetime.date(2023, 1, 20), datetime.date(2023, 1, 23),
            datetime.date(2023, 1, 25), datetime.date(2023, 1, 27), datetime.date(2023, 1, 30),
            datetime.date(2023, 2, 1), datetime.date(2023, 2, 3), datetime.date(2023, 2, 6),
            datetime.date(2023, 2, 8), datetime.date(2023, 2, 10), datetime.date(2023, 2, 13),
            datetime.date(2023, 2, 15), datetime.date(2023, 2, 17), datetime.date(2023, 2, 22),
            datetime.date(2023, 2, 24), datetime.date(2023, 2, 27), datetime.date(2023, 3, 1),
            datetime.date(2023, 3, 3), datetime.date(2023, 3, 6), datetime.date(2023, 3, 8),
            datetime.date(2023, 3, 10), datetime.date(2023, 3, 13), datetime.date(2023, 3, 15),
            datetime.date(2023, 3, 17), datetime.date(2023, 3, 20), datetime.date(2023, 3, 22),
            datetime.date(2023, 3, 24), datetime.date(2023, 4, 3), datetime.date(2023, 4, 5),
            datetime.date(2023, 4, 7), datetime.date(2023, 4, 10), datetime.date(2023, 4, 12),
            datetime.date(2023, 4, 14), datetime.date(2023, 4, 17), datetime.date(2023, 4, 19),
            datetime.date(2023, 4, 21), datetime.date(2023, 4, 24), datetime.date(2023, 4, 26),
            datetime.date(2023, 4, 28)]

def reset_day_lateness(app):
    with app.app_context():
        pst_tz = datetime.timezone(offset=-datetime.timedelta(hours=8))
        curr_time = datetime.datetime.now(pst_tz)
        if (curr_time.date() in dates and curr_time.hour == 9 and curr_time.minute == 0):
            for tracker in Lateness.query.all():
                if (tracker.lastTime == None or tracker.lastTime != curr_time.date()):                    
                    tracker.lateTotal = tracker.lateTotal + 50
                    tracker.lastTime = curr_time.date()

                db.session.commit()

@late.route('/lateness-tracker', methods=['GET', 'POST'])
@login_required
def lateness_home():
    tracking = Lateness.query.order_by("name").all()
    ordered_tracking = Lateness.query.order_by(Lateness.lateTotal.desc()).all()

    pst_tz = datetime.timezone(offset=-datetime.timedelta(hours=8))
    curr_time = datetime.datetime.now(pst_tz)

    return render_template('lateness_tracker.html', user=current_user, tracking=tracking, 
                            ordered_tracking=ordered_tracking, curr_time=curr_time, dates=dates)

@late.route('/mark-here', methods=['POST'])
@login_required
def mark_here():
    lateness = json.loads(request.data)
    latenessId = lateness['latenessId']
    here = lateness['here']
    tracker = Lateness.query.get(latenessId)

    if tracker:
        pst_tz = datetime.timezone(offset=-datetime.timedelta(hours=8))
        if here:
            tracker.lateTotal = tracker.lateTotal + max(datetime.datetime.now(pst_tz).minute - 10, 0)
            tracker.lastTime = datetime.datetime.now(pst_tz)
        elif not here:
            tracker.lateTotal = tracker.lateTotal - max(tracker.lastTime.minute - 10, 0)
            tracker.lastTime = None
        db.session.commit()
        return jsonify({})
