# FocusFlow — To-Do List App

A simple, clean task management web app built with **Flask** and **SQLite**. Create an account, manage your daily tasks, and track your progress — with a separate admin dashboard for managing users, tasks, and site settings.

## Features

**User side**
- Register and log in with a username/email and password (hashed with Werkzeug)
- Add, edit, complete, and delete personal tasks
- Dashboard summary showing total, completed, and pending task counts
- Each user only sees their own tasks

**Admin side**
- Separate admin login (`/admin/login`)
- Admin dashboard listing all users and all tasks across the app
- Database view for a raw look at stored records
- Editable site header/subtitle text, stored in the database and shown site-wide

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite via Flask-SQLAlchemy
- **Auth:** Session-based, with hashed passwords (Werkzeug security)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Testing:** `unittest` with Flask's test client

## Project Structure

```
TO-DO-LIST/
├── run.py                     # App entry point — creates the app, initializes and seeds the DB
├── app/
│   ├── __init__.py            # App factory, DB setup, blueprint registration
│   ├── models.py              # User, Task, and AppSetting models
│   ├── routes/
│   │   ├── auth.py            # Register, login, logout, admin login, admin dashboard/settings
│   │   └── tasks.py           # Task dashboard and CRUD operations
│   ├── templates/             # Jinja2 templates (base, login, register, task, admin dashboard)
│   └── static/
│       ├── css/style.css
│       └── js/script.js
├── instance/
│   └── todo.db                # SQLite database (created automatically on first run)
└── tests/
    └── test_auth_flow.py      # Register → login → dashboard → admin flow tests
```

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Vishalkaushik001/TO-DO-LIST.git
cd TO-DO-LIST

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy
```

> **Note:** This project doesn't yet include a `requirements.txt`. If you add one, running `pip install -r requirements.txt` will cover the above.

### Running the app

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000/`. On first run, it automatically creates the database and seeds:
- A default admin account (`admin` / `admin123`)
- Default header text ("FocusFlow" / "Calm plans for a clearer day")

**Change the default admin password before using this anywhere beyond your own machine.**

### Running tests

```bash
python -m unittest tests/test_auth_flow.py
```

## Usage

1. Go to `/register` to create a user account.
2. Log in at `/login`.
3. Add tasks from your dashboard at `/tasks` — mark them complete, edit, or delete them.
4. To access admin features, log in separately at `/admin/login` with the admin account.

## Roadmap / Ideas for Improvement

- [ ] Move `SECRET_KEY` and database URI into environment variables instead of hardcoding them
- [ ] Add a `requirements.txt` / `pyproject.toml`
- [ ] Add CSRF protection on forms
- [ ] Add due dates, priorities, or tags to tasks
- [ ] Password reset flow
- [ ] Remove the committed `instance/todo.db` from version control and add it to `.gitignore`

## License

No license specified yet. Consider adding one (e.g., MIT) if you plan to share or accept contributions.
