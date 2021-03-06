from flask_wtf import FlaskForm
from wtforms import (BooleanField, TextField, HiddenField, PasswordField, 
   DateTimeField, validators, IntegerField, SubmitField)
import user_constants


class LoginForm(FlaskForm):
    login = TextField('user_name', [validators.Required()])
    password  = TextField('password',  [validators.Required()])
    remember_me = BooleanField('remember_me', default = False)


class SignupForm(FlaskForm):
    user_name = TextField('user_name',   [
      validators.Length(
         min=user_constants.MIN_USERNAME_LEN,
         max=user_constants.MAX_USERNAME_LEN
      ),
      validators.Regexp(
         "^[a-zA-Z0-9]*$",
         message="Username can only contain letters and numbers"
      )
    ])
    first_name = TextField('first_name', [validators.Required()])
    last_name  = TextField('last_name', [validators.Required()])
    email      = TextField('email', [validators.Required(), validators.Email()])
    password   = PasswordField(
      'New Password', 
      [validators.Length(
         min=user_constants.MIN_PASSWORD_LEN,
         max=user_constants.MAX_PASSWORD_LEN)]
    )
    confirm = PasswordField('Repeat Password', [
      validators.Required(),
      validators.EqualTo('password', message='Passwords must match')
    ])
