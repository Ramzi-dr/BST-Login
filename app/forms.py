from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User
import re


def password_check(form,field):
    password = form.password.data
    if len(password)< 7:
        raise ValidationError('Das Passwort muss mindestens 7 Buchstaben lang sein')
    elif re.search('[0-9]',password) is None:
        raise ValidationError('Das Passwort muss eine Zahl enthalten')
    elif re.search('[A-Z]',password) is None:
        raise ValidationError('Das Passwort muss einen Großbuchstaben enthalten')
    elif re.search('[@_,\-+"\]\[!#.\\\;$%^\'&*()<>?/\|}{~:]', password) is None:
        raise ValidationError('Das Passwort muss einen Sonderzeichen enthalten')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    vorname = StringField('Vorname', validators=[DataRequired(), Length(min=2, max=20)])
    firmaname = StringField('Firmaname')
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired(),password_check],
                             render_kw={"placeholder": "Mindestens: 7 Buchstaben, eine Zahl, "
                                                       "und muss einen Großbuchstaben enthalten "})
    confirm_password = PasswordField('Passwort Wiederholen',  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('einreichen')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Diese E-email existiert bereits in der Datenbank!\n'
                                  '. Bitte wählen Sie ein anderes aus')


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Length(min=3, max=20), Email()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=7, max=20)])
    remember = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')


    def validate_email(self, email):
        email = User.query.filter_by(email=email.data.upper()).first()
        if email is None:
             raise ValidationError('Es gibt kein Konto mit dieser E-Mail. Sie müssen sich zuerst registrieren!')


class LoginAdmin(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Length(min=3, max=20), Email()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=7, max=20)])
    submit = SubmitField('Anmelden')


    def validate_admin_email(self, email):
        email = User.query.filter_by(email=email.data.upper()).first()
        if email is None:
             raise ValidationError('Es gibt kein Konto mit dieser E-Mail. Sie müssen sich zuerst registrieren!')


class RequestResetForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Fordere Passwort-Reset an')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Passwort', validators=[DataRequired(),password_check],
                             render_kw={"placeholder": "Mindestens: 7 Buchstaben, eine Zahl, "
                                                       "und muss einen Großbuchstaben enthalten "})
    confirm_password = PasswordField('Passwort Wiederholen',  
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Passwort zurücksetzen')



