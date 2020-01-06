from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from app.models import Company, Contact


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CreateUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class CreateContact(FlaskForm):
    last_name = StringField('last_name', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    job_position = StringField('job_position', validators=[DataRequired()])
    contact_status = SelectField('contact_status', choices=[("Client", 'Client'), ("Prospect", "Prospect"),
                                                            ("Churner", "Churner"), ("Prestataire", "Prestataire"),
                                                            ("Reperage", "Reperage")])
    company_name = StringField('company_name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField('Créer')


class CreateNote(FlaskForm):
    """
    company = SelectField('company',
                          choices=[[str(i), x.company_name.title()] for i, x in enumerate(Company.query.all())])

    contact = SelectField(
        'contact',
        choices=[[str(i), f'{x.last_name.title()} {x.first_name.title()}'] for i, x in enumerate(Contact.query.all())]
    )
    """
    note = TextAreaField('note', validators=[DataRequired()])
    submit = SubmitField('Créer la note')




