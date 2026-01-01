from flask import Flask, jsonify, request, abort
import os
import requests
from dotenv import load_dotenv
from sqlalchemy import text
from extensions import db

load_dotenv()

API_KEY = os.getenv("REBRICKABLE_API_KEY")
if not API_KEY:
    raise RuntimeError("REBRICKABLE_API_KEY not set")

BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"


def fetch_set(set_num):
    headers = {"Authorization": f"key {API_KEY}"}
    url = f"{BASE_URL}{set_num}/"
    r = requests.get(url, headers=headers, timeout=5)

    if r.status_code == 404:
        return None

    r.raise_for_status()
    return r.json()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://brickstatuser:brickstatpass@db:3306/brickstat",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize extensions
    db.init_app(app)
    # migrations
    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    # import models to register them with SQLAlchemy
    import models  # noqa: F401


    @app.route("/reviews", methods=["POST"])
    def create_review():
        data = request.get_json() or {}

        # REQUIRED
        set_num = data.get("set_num")
        if not set_num:
            return jsonify({"error": "set_num is required"}), 400

        # Optional set metadata (used only if set does not exist)
        set_name = data.get("set_name")
        piece_count = data.get("piece_count")
        release_year = data.get("release_year")


        # Validate numeric fields
        def ivalue(key, minv=None, maxv=None):
            v = data.get(key)
            if v is None:
                return None
            try:
                vi = int(v)
            except Exception:
                abort(400, description=f"{key} must be an integer")
            if minv is not None and vi < minv:
                abort(400, description=f"{key} must be >= {minv}")
            if maxv is not None and vi > maxv:
                abort(400, description=f"{key} must be <= {maxv}")
            return vi

        build_time_minutes = ivalue("build_time_minutes")
        distraction_level = ivalue("distraction_level", 1, 10)
        organization_level = ivalue("organization_level", 1, 10)
        build_speed = ivalue("build_speed", 1, 3)
        user_id = ivalue("user_id")

        review_text = data.get("review_text")
        if review_text and len(review_text) > 250:
            return jsonify({"error": "review_text must be <= 250 characters"}), 400

        # Find or create Set
        set_obj = models.Set.query.filter_by(set_num=set_num).first()
        if set_obj is None:
            if not set_name:
                return jsonify({"error": "set_name required when creating a new set"}), 400

            set_obj = models.Set(
                set_num=set_num,
                name=set_name,
                piece_count=piece_count,
                release_year=release_year,
            )
            db.session.add(set_obj)

        # Create Review (ONLY review fields)
        review = models.Review(
            set_num=set_num,
            build_time_minutes=build_time_minutes,
            distraction_level=distraction_level,
            organization_level=organization_level,
            build_speed=build_speed,
            review_text=review_text,
            user_id=user_id,
        )

        db.session.add(review)
        db.session.commit()

        return jsonify(review.to_dict()), 201


    @app.route("/reviews", methods=["GET"])
    def list_reviews():
        set_num = request.args.get("set_num")
        q = models.Review.query
        if set_num:
            q = q.filter_by(set_num=set_num)
        items = q.order_by(models.Review.created_at.desc()).limit(100).all()
        return jsonify([i.to_dict() for i in items])

    # useful to get all the reviews for a given set, 
    # for example for the page showing set details
    @app.route("/sets/<set_num>/reviews", methods=["GET"])
    def list_reviews_for_set(set_num):
        s = models.Set.query.filter_by(set_num=set_num).first()
        if s is None:
            return jsonify({
                "set_num": set_num,
                "review_count": 0,
                "reviews": []
            })

        items = (
            models.Review.query
            .filter_by(set_num=set_num)
            .order_by(models.Review.created_at.desc())
            .all()
        )

        return jsonify({
            "set_num": s.set_num,
            "set_name": s.name,
            "piece_count": s.piece_count,
            "release_year": s.release_year,
            "review_count": len(items),
            "reviews": [r.to_dict() for r in items],
        })
    # lists all the reviews for a given set by a specific user
    # USEFUL for to show on account dashboard page
    @app.route("/sets/reviews/<user_id>", methods=["GET"])
    def list_reviews_for_user(user_id):
        items = (
            models.Review.query
            .filter_by(user_id=user_id)
            .order_by(models.Review.created_at.desc())
            .all()
        )

        return jsonify({
            "user_id": user_id,
            "review_count": len(items),
            "reviews": [r.to_dict() for r in items],
        })
    @app.route("/sets/<set_num>/reviews/<user_id>", methods=["DELETE"])
    def delete_review(set_num, user_id):
        review = models.Review.query.filter_by(set_num=set_num, user_id=user_id).first()
        if review is None:
            return jsonify({"error": "Review not found"}), 404

        db.session.delete(review)
        db.session.commit()

        return jsonify({"message": "Review deleted successfully"}), 200

    @app.route("/db_health")
    def db_health():
        try:
            # simple lightweight check
            result = db.session.execute(text("SELECT 1")).fetchone()
            if result is None:
                raise RuntimeError("no result")
            return jsonify({"db": "ok"}), 200
        except Exception as e:
            return jsonify({"db": "error", "detail": str(e)}), 500

    # routes to rebrickable api, Might move to the frontend later
    @app.route("/sets/<set_num>")
    def get_set(set_num):
        s = fetch_set(set_num)
        if not s:
            return jsonify({"error": "Invalid set number"}), 404

        return jsonify({
            "set_name": s["name"],
            "set_num": s["set_num"],
            "year": s["year"],
            "pieces": s["num_parts"],
            "image": s["set_img_url"]
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
