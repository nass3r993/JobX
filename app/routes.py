from flask import request
from sqlalchemy import text
from flask import request, jsonify
from sqlalchemy import or_
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from flask import jsonify
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask import render_template_string
from .models import User, Job, Application
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .utils import generate_cv_pdf
from flask_wtf.csrf import validate_csrf
from flask import abort
from flask_wtf import FlaskForm
from . import csrf
import re



def is_valid_phone(phone):
    # Regex: starts with '05' and then 8 digits (total 10 digits)
    return bool(re.fullmatch(r'05\d{8}', phone))
def is_valid_email(email):
    # Basic email regex: something@something.something
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))


bp = Blueprint('main', __name__)

class EmptyForm(FlaskForm):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'main.home'

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You must be logged in to view that page.", "warning")
    return redirect(url_for('main.home'))

@bp.route('/')
def home():
    return render_template('home.html', user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        csrf_token = request.form.get('csrf_token')

        # If using Flask-WTF CSRF protection globally
        from flask_wtf.csrf import validate_csrf
        try:
            validate_csrf(csrf_token)
        except Exception:
            flash("Invalid CSRF token", "danger")
            return render_template('register.html')

        if not all([name, email, phone, address, password, confirm_password]):
            flash("All fields are required.", "danger")
            return render_template('register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')
        
        if not is_valid_phone(phone):
            flash("Phone number must be in the format 05xxxxxxxx (10 digits, starting with 05).", "danger")
            return render_template('register.html')

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
            return render_template('register.html')

        try:
            hashed_pw = generate_password_hash(password)
            user = User(
                name=name,
                email=email,
                phone=phone,
                address=address,
                password=hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('main.login'))  # make sure this route exists
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists.", "danger")
            return render_template('register.html')

    return render_template('register.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.profile'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    # Get form data directly from POST
    first_name = request.form.get('firstName', '').strip()
    phone = request.form.get('phone', '').strip()
    location = request.form.get('location', '').strip()
    bio = request.form.get('bio', '').strip()
    experience = request.form.get('experience', '').strip()
    skills = request.form.get('skills', '').strip()
    if not is_valid_phone(phone):
        flash("Phone number must be in the format 05xxxxxxxx (10 digits, starting with 05).", "danger")
        return render_template('profile.html')

    # Update user fields
    current_user.name = first_name
    current_user.phone = phone
    current_user.address = location
    current_user.bio = bio
    current_user.experience = experience
    current_user.skills = skills

    try:
        db.session.commit()
        flash('Your profile has been updated.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating your profile.', 'error')
        # Optionally log the error here

    return redirect(url_for('main.profile'))


@bp.route('/profile/export')
@login_required
def export_pdf():
    pdf_path = generate_cv_pdf(current_user)
    return send_file(pdf_path, as_attachment=True)


@bp.route('/jobs')
@login_required
def jobs():
    return render_template('jobs.html')




@bp.route('/api/v1/jobs')
@login_required
def api_jobs():
    search = request.args.get('search', '', type=str).strip()
    job_type = request.args.get('type', '', type=str).strip()
    location = request.args.get('location', '', type=str).strip()

    query = Job.query

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term)
            )
        )

    if job_type:
        query = query.filter(Job.job_type == job_type)


    if location:
        unsafe_condition = f"LOWER(location) LIKE '%%{location.lower()}%%'"
        query = query.filter(text(unsafe_condition))

    jobs = query.all()

    if not jobs:
        return jsonify([]), 200

    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'salary': job.salary,
            'job_type': job.job_type,
            'location': job.location,
            'posted_date': job.posted_date.isoformat() if job.posted_date else None,
            'application_deadline': job.application_deadline.isoformat() if job.application_deadline else None
        })

    return jsonify(jobs_data)






@bp.route('/jobs/<string:job_id>')
@login_required
def job_detail(job_id):
    return render_template('job_detail.html', job_id=job_id)

@bp.route('/api/v1/jobs/<string:job_id>', methods=['GET', 'PATCH'])
@login_required
@csrf.exempt
def api_job_detail(job_id):
    job = Job.query.get_or_404(job_id)

    # GET: return job data
    if request.method == 'GET':
        poster = job.poster
        return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "company": job.company,
        "salary": job.salary,
        "job_type": job.job_type,
        "location": job.location,
        "posted_date": job.posted_date.isoformat(),
        "application_deadline": job.application_deadline.isoformat(),
        'posted_by': job.posted_by,
        'poster_email': poster.email if poster else "N/A",
        'poster_phone': poster.phone if poster else "N/A",
        'poster_address': poster.address if poster else "N/A"
    })

    # PATCH: update fields except id
    if request.method == 'PATCH':


        data = request.get_json()

        # Apply all updates except 'id'
        for key, value in data.items():
            if key == 'id':
                continue
            if hasattr(job, key):
                setattr(job, key, value)

        db.session.commit()
        return jsonify({'message': 'Job updated successfully'})



from sqlalchemy.exc import IntegrityError  # Already imported earlier

@bp.route('/jobs/<string:job_id>/apply')
@login_required
def apply(job_id):
    existing_application = Application.query.filter_by(
        user_id=current_user.id, job_id=job_id
    ).first()

    if existing_application:
        flash('You have already applied to this job.', 'warning')
    else:
        application = Application(user_id=current_user.id, job_id=job_id)
        db.session.add(application)
        try:
            db.session.commit()
            flash('Application submitted successfully.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('You have already applied to this job.', 'danger')

    return redirect(url_for('main.my_applications'))


@bp.route('/applications')
@login_required
def my_applications():
    status_filter = request.args.get('status')

    # Filter by user and optionally by status
    query = Application.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    applications = query.all()
    form = EmptyForm()
    return render_template('applications.html', applications=applications, form=form)



@bp.route('/applications/<int:app_id>/remove', methods=['POST'])
@login_required
def remove_application(app_id):
    app = Application.query.get_or_404(app_id) 
    db.session.delete(app)
    db.session.commit()
    flash('Application removed successfully.', 'success')
    return redirect(url_for('main.my_applications'))
