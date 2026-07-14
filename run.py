from app import create_app, db, seed_default_data

app = create_app()

with app.app_context():
    db.create_all()
    seed_default_data()


if __name__ == '__main__':
    app.run(debug=True)


