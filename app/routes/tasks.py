from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('tasks.dashboard'))
    return redirect(url_for('auth.login'))


@tasks_bp.route('/tasks', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if title:
            new_task = Task(title=title, description=description or None, user_id=session['user_id'])
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully.', 'success')
        else:
            flash('Task title is required.', 'error')

    tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.id.desc()).all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks

    return render_template(
        'task.html',
        username=session.get('username'),
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
    )


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'success')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        task.completed = not task.completed
        db.session.commit()
        flash('Task updated.', 'success')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if title:
            task.title = title
            task.description = description or None
            db.session.commit()
            flash('Task updated.', 'success')
        else:
            flash('Task title is required.', 'error')
    return redirect(url_for('tasks.dashboard'))
