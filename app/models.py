from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.title}>'


class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(250), nullable=False)

    @staticmethod
    def get_value(key, default=None):
        setting = AppSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_value(key, value):
        setting = AppSetting.query.filter_by(key=key).first()
        if setting is None:
            setting = AppSetting(key=key, value=value)
            db.session.add(setting)
        else:
            setting.value = value
        db.session.commit()