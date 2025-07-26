import uuid
from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)  # store comma-separated skills
    password = db.Column(db.String(200), nullable=False)

    applications = db.relationship('Application', backref='applicant', lazy=True)
    jobs_posted = db.relationship('Job', backref='poster', lazy=True)


class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    company = db.Column(db.String(100))
    salary = db.Column(db.String(50))  
    job_type = db.Column(db.String(20))  
    location = db.Column(db.String(100))
    posted_date = db.Column(db.Date, default=datetime.utcnow)
    application_deadline = db.Column(db.Date, default=lambda: datetime.utcnow() + timedelta(days=30))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)  # NEW
    status = db.Column(db.String(50), default='Pending')  # NEW

    job = db.relationship('Job', backref='applications')

    __table_args__ = (
        db.UniqueConstraint('job_id', 'user_id', name='unique_application'),
    )

