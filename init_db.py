from app import app
from models import db

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    print("Database tables created successfully!") 