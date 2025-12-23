from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length, URL


class ContactForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    phone = StringField("phone", validators=[DataRequired()])
    message = TextAreaField("message", validators=[DataRequired()])
