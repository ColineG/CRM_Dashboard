from flask import render_template, flash, redirect, url_for
from werkzeug.urls import url_parse

from app import db
from app.forms import LoginForm, CreateContact, CreateNote
from flask import request, render_template, make_response, render_template_string
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contact, Company, Email, Phone, FollowUp
from flask_user import login_required

from plot.altair_plot import html_contrat_signed_vs_refused_count, html_contrat_signed_vs_refused_amount, concat, \
    html_ca_entreprise, html_demande_type_presta, html_detail_company


# The Home page is accessible to anyone
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

""" 
@app.route('/home', methods=['GET'])
def create_user():
    #Create a user.
    new_user = User(username='coco',
                    password_hash='mysecret',
                    email='coline@gmail.com')  # Create an instance of the User class
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Commits all changes
    return render_template('blahome.html', title='Home', new_user=new_user)
"""

""" 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    app.logger.info(form.username)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        app.logger.info(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('index.html', title='Sign In', form=form)
"""


@app.route('/create_contact', methods=['GET', 'POST'])
def create_contact():
    form = CreateContact()
    if form.validate_on_submit():
        company = Company.query.filter_by(company_name=form.company_name.data)
        email = Email.query.filter_by(email=form.email.data)
        phone = Phone.query.filter_by(phone=form.phone.data)
        if email.count() == 1:
            flash('Email already exist')
            return redirect(url_for('create_contact'))
        if phone.count() == 1:
            flash('Phone already exist')
            return redirect(url_for('create_contact'))
        if company.count() == 1:
            contact = Contact(last_name=form.last_name.data, first_name=form.first_name.data,
                              job_position=form.job_position.data, contact_status=form.contact_status.data)
            company = company.first()
            company.contacts.append(contact)

        else:
            contact = Contact(last_name=form.last_name.data, first_name=form.first_name.data,
                              job_position=form.job_position.data, contact_status=form.contact_status.data)
            company = Company(company_name=form.company_name.data)
            company.contacts.append(contact)
        db.session.add_all([company, contact])
        db.session.commit()
        flash('Congratulations, you have create a new contact !')

    return render_template('create_contact.html', title='Create contact', form=form)


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    form = CreateNote()
    if form.validate_on_submit():
        company = Company.query.filter_by(company_name=form.company.data).first()
        contact = Contact.query.filter_by()
        follow_up = FollowUp(note=form.note.data, company=company, contact=contact)
        db.session.add(follow_up)
        db.session.commit()
        flash('Congratulations, you have well create your note !')

    return render_template('create_note.html', form=form)


@app.route('/dash', methods=['GET'])
def dash():
    kwargs = {
    }
    plot_1 = html_contrat_signed_vs_refused_count()
    plot_2 = html_contrat_signed_vs_refused_amount()
    concat(plot_1, plot_2, 'contrat_signed_vs_refused')
    return render_template('dash.html', **kwargs)


@app.route('/dash2', methods=['GET'])
def dash2():
    kwargs = {
    }
    plot_1 = html_ca_entreprise()
    plot_2 = html_demande_type_presta()
    concat(plot_1, plot_2, 'ca_et_type_presta')
    return render_template('dash2.html', **kwargs)


@app.route('/dash3', methods=['GET'])
def dash3():
    kwargs = {
    }
    html_detail_company()
    return render_template('dash3.html', **kwargs)

""" 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

"""