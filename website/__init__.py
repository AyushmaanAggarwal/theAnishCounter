from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user, AnonymousUserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

DB_NAME = "database.db"

scheduler = BackgroundScheduler(timezone="America/Los_Angeles", daemon=True)

class MyView(ModelView):
    def is_accessible(self):
        return not isinstance(current_user._get_current_object(), AnonymousUserMixin) and current_user.testlevel == 'admin'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'spring'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    admin = Admin(app)

    from .views import views
    from .auth import auth
    from .lateness import late

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(late, url_prefix='/')

    from .models import User, Counter, Movie, Book, Lateness, Event, Announcement

    admin.add_view(MyView(User, db.session))
    admin.add_view(MyView(Counter, db.session))
    admin.add_view(MyView(Movie, db.session))
    admin.add_view(MyView(Book, db.session))
    admin.add_view(MyView(Lateness, db.session))
    admin.add_view(MyView(Event, db.session))
    admin.add_view(MyView(Announcement, db.session))
    # migrate = Migrate(app, db, render_as_batch=True)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .lateness import reset_day_lateness
    from .views import delete_old_events
    scheduler.add_job(func=lambda: reset_day_lateness(app), trigger='cron', month='1-5', day_of_week='mon, wed, fri', hour=9, minute=0, second=0)
    scheduler.add_job(func=lambda: delete_old_events(app), trigger='cron', month='1-5', day_of_week='mon, tue, wed, thu, fri, sat, sun', hour=0, minute=1, second=0)
    scheduler.start()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')