# -*- coding: utf-8 -*-
"""
Created on Sun May 16 03:05:37 2021

@author: garvi
"""
# Files
from ip_app.models import User

# Packages
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class Login(FlaskForm):
    '''
    Login form, driven by base_page.html
    
    Note to self: Dont remove the flaskform the validators come from there
    '''
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class Register(FlaskForm):
    '''
    Registeration form, driven by base_page.html
    '''
    # Taken from the flask docs
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    
    # Email() validates this field for me
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired(), Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Sign In')
    
    def validate_username(self, username):
        '''
        validate_X is a flask wtforms thing, allows for additional checking (autoinvoked).
        '''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''
        validate_X is a flask wtforms thing, allows for additional checking (autoinvoked).
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
            
class NewProjectForm(FlaskForm):
    project_name = StringField('Project Name', [validators.DataRequired()])
    project_desc = TextAreaField('Project Description', [validators.DataRequired()])
    
    submit = SubmitField('Create Project')



class NewTaskForm(FlaskForm):
    task_name = StringField("Task: ", [validators.DataRequired()])
    assigned_member = StringField("Assigned To: ", [validators.DataRequired()])
    
    eta = IntegerField('Eta: ', [validators.DataRequired()])
    submit = SubmitField('Create Task in this Project')
    
    
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

    