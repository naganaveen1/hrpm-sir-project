from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class EnquiryForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Please enter your full name."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Please enter your email address."),
        Email(message="Please enter a valid email address.")
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message="Please enter your phone number."),
        Length(min=10, max=15, message="Please enter a valid 10 to 15 digit phone number.")
    ])
    business_name = StringField('Business / Enterprise Name', validators=[
        Optional(),
        Length(max=150)
    ])
    service_id = SelectField('Required Service', coerce=int, validators=[Optional()])
    message = TextAreaField('Message / Requirements', validators=[
        DataRequired(message="Please describe your requirements or inquiry."),
        Length(min=10, max=2000, message="Message should be at least 10 characters long.")
    ])
    submit = SubmitField('Submit Inquiry')

class ConsultationForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Please enter your full name."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Please enter your email address."),
        Email(message="Please enter a valid email address.")
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message="Please enter your phone number."),
        Length(min=10, max=15, message="Please enter a valid 10 to 15 digit phone number.")
    ])
    business_name = StringField('Business / Enterprise Name', validators=[
        Optional(),
        Length(max=150)
    ])
    service_id = SelectField('Select Service for Consultation', coerce=int, validators=[Optional()])
    preferred_date = StringField('Preferred Date', validators=[
        DataRequired(message="Please select a preferred date for consultation.")
    ])
    preferred_time = SelectField('Preferred Slot', choices=[
        ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM (Morning)'),
        ('11:30 AM - 12:30 PM', '11:30 AM - 12:30 PM (Morning)'),
        ('02:00 PM - 03:00 PM', '02:00 PM - 03:00 PM (Afternoon)'),
        ('04:00 PM - 05:00 PM', '04:00 PM - 05:00 PM (Evening)'),
        ('06:00 PM - 07:00 PM', '06:00 PM - 07:00 PM (Evening)')
    ], validators=[DataRequired(message="Please select a preferred time slot.")])
    message = TextAreaField('Consultation Topic Details', validators=[
        Optional(),
        Length(max=1000)
    ])
    submit = SubmitField('Book Consultation Appointment')

class AdminLoginForm(FlaskForm):
    email = StringField('Admin Email Address', validators=[
        DataRequired(message="Please enter your admin email address."),
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter your password.")
    ])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Authenticate & Login')

