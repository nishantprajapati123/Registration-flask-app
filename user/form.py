from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, SubmitField)
from wtforms.validators import InputRequired, Length, DataRequired, Email, NumberRange


class RegistrationForm(FlaskForm):
    name  = StringField("Full Name", id="name_field" ,validators=[DataRequired()])
    email = StringField("Email Id", id="email_field", validators=[DataRequired(), Email()])
    phone = IntegerField("Phone number", id="phone_field", validators=[DataRequired()])
    submit = SubmitField('Submit')