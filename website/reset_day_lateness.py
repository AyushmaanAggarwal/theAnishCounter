from .models import Lateness
from . import db
from .lateness import dates
import datetime

pst_tz = datetime.timezone(offset=-datetime.timedelta(hours=8))
curr_time = datetime.datetime.now(pst_tz)
if (curr_time.date() in dates and curr_time.hour == 9):
    for tracker in Lateness.query.all():
        if not tracker.arrived:
            tracker.lateTotal = tracker.lateTotal + 50
        tracker.arrived = False
        tracker.lastTime = None

    db.session.commit()
