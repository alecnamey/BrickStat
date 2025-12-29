from backend import create_app
from extensions import db
import models  # registers models with SQLAlchemy


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Tables created (if not existing)")


if __name__ == "__main__":
    main()
