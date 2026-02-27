from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    claimed = db.Column(db.Boolean, default=False)
    claimed_at = db.Column(db.DateTime)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_code = db.Column(db.String(8), nullable=False)
    clip_name = db.Column(db.String(100), nullable=False)
    rt_ms = db.Column(db.Float, nullable=False)
    verdict = db.Column(db.String(20), nullable=False)
    stimulus_frame = db.Column(db.Integer)
    color_mode = db.Column(db.String(20))
    game = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)