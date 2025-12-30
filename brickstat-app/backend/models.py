from datetime import datetime
from extensions import db


class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)

    # LEGO identity
    set_num = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)

    # Cached static metadata
    piece_count = db.Column(db.Integer)
    release_year = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    reviews = db.relationship(
        "Review",
        back_populates="set",
        cascade="all, delete-orphan"
    )


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    # FK to sets (string FK on set_num — intentional)
    set_num = db.Column(
        db.String(50),
        db.ForeignKey("sets.set_num"),
        nullable=False,
        index=True
    )

    # Relationship
    set = db.relationship("Set", back_populates="reviews")

    # User-provided / subjective data
    build_time_minutes = db.Column(db.Integer)
    distraction_level = db.Column(db.Integer)
    organization_level = db.Column(db.Integer)
    build_speed = db.Column(db.Integer)

    review_text = db.Column(db.String(250))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "set_num": self.set_num,
            "build_time_minutes": self.build_time_minutes,
            "distraction_level": self.distraction_level,
            "organization_level": self.organization_level,
            "build_speed": self.build_speed,
            "review_text": self.review_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
