from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


def seed_default_data(app=None):
    from app.models import AppSetting, User

    if app is not None:
        with app.app_context():
            seed_default_data()
        return

    db.create_all()

    admin = User.query.filter_by(username='admin').first()
    if admin is None:
        admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)

    if AppSetting.query.filter_by(key='header_title').first() is None:
        AppSetting.set_value('header_title', 'FocusFlow')
    if AppSetting.query.filter_by(key='header_subtitle').first() is None:
        AppSetting.set_value('header_subtitle', 'Calm plans for a clearer day')

    db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.context_processor
    def inject_site_settings():
        from app.models import AppSetting

        return {
            'header_title': AppSetting.get_value('header_title', 'FocusFlow'),
            'header_subtitle': AppSetting.get_value('header_subtitle', 'Calm plans for a clearer day'),
        }

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app

