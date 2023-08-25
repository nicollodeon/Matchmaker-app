from flask_wtf import FlaskForm
from app.models import User
from flask_login import current_user

# for registration
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

#for pfp, file form and validators
from flask_wtf.file import FileField, FileAllowed



#Flaskform is the base class, data required is to make sure not empty
# defining the fields of a web form as class variables
class LoginForm(FlaskForm):
    # StringField etc are classes defined in wtf packages, created in our Flaskfrom class
    # these field/classes know how to render themselves in html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    gender = RadioField('I am ', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Edit Image', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)]) # set to the space allocate to the DB
    gender = StringField('Gender', validators=[Length(min=0, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            if (username.data != current_user.username):
                raise ValidationError('Please use a different username.')
