from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    keyword_taxon = StringField('Taxon', validators=[DataRequired()])
    keyword_traits = StringField('Traits', validators=[DataRequired()])
    submit = SubmitField('Search')
