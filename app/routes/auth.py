from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import AppSetting, Task, User

auth_bp = Blueprint('auth', __name__)


def _is_admin_session():
    return session.get('role') == 'admin'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'error')
            return render_template('register.html')

        new_user = User(username=username, email=email, password_hash=generate_password_hash(password), role='user')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username, role='user').first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful.', 'success')
            return redirect(url_for('tasks.dashboard'))

        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin_user = User.query.filter_by(username=username, role='admin').first()
        if admin_user and check_password_hash(admin_user.password_hash, password):
            session['user_id'] = admin_user.id
            session['username'] = admin_user.username
            session['role'] = admin_user.role
            flash('Admin login successful.', 'success')
            return redirect(url_for('auth.admin_dashboard'))

        flash('Invalid admin credentials.', 'error')

    return render_template('login.html', admin_mode=True)


@auth_bp.route('/admin/dashboard')
def admin_dashboard():
    if not _is_admin_session():
        flash('Please log in as an admin.', 'error')
        return redirect(url_for('auth.admin_login'))

    users = User.query.order_by(User.id).all()
    tasks = Task.query.order_by(Task.id).all()
    return render_template('admin_dashboard.html', users=users, tasks=tasks)


@auth_bp.route('/admin/settings', methods=['POST'])
def admin_settings():
    if not _is_admin_session():
        flash('Please log in as an admin.', 'error')
        return redirect(url_for('auth.admin_login'))

    header_title = request.form.get('header_title', '').strip() or 'FocusFlow'
    header_subtitle = request.form.get('header_subtitle', '').strip() or 'Calm plans for a clearer day'

    AppSetting.set_value('header_title', header_title)
    AppSetting.set_value('header_subtitle', header_subtitle)
    flash('Header settings updated.', 'success')
    return redirect(url_for('auth.admin_dashboard'))


@auth_bp.route('/admin/database')
def admin_database():
    if not _is_admin_session():
        flash('Please log in as an admin.', 'error')
        return redirect(url_for('auth.admin_login'))

    users = User.query.order_by(User.id).all()
    tasks = Task.query.order_by(Task.id).all()
    return render_template('admin_dashboard.html', users=users, tasks=tasks, show_database=True)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

