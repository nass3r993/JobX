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


bp = Blueprint('main', __name__)

class EmptyForm(FlaskForm):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def home():
    return render_template('home.html', user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(
                email=form.email.data,
                name=form.name.data,
                phone=form.phone.data,
                address=form.address.data,
                password=hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('main.login'))

        except IntegrityError:
            db.session.rollback()
            flash("Email already exists. Please choose a different one.", "danger")
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)



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

@bp.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('update_profile.html', form=form)

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
    jobs = Job.query.all()
    jobs_data = []
    for job in jobs:
        poster = job.poster
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company
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
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'description': job.description,
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
    apps = Application.query.filter_by(user_id=current_user.id).all()
    form = EmptyForm()
    return render_template('applications.html', apps=apps, form=form)


@bp.route('/applications/<int:app_id>/remove', methods=['POST'])
@login_required
def remove_application(app_id):
    app = Application.query.get_or_404(app_id) 
    db.session.delete(app)
    db.session.commit()
    flash('Application removed successfully.', 'success')
    return redirect(url_for('main.my_applications'))
