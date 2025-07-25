import uuid
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    applications = db.relationship('Application', backref='applicant', lazy=True)
    jobs_posted = db.relationship('Job', backref='poster', lazy=True)  # NEW

class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    company = db.Column(db.String(100))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    job = db.relationship('Job', backref='applications')

    __table_args__ = (
        db.UniqueConstraint('job_id', 'user_id', name='unique_application'),
    )
