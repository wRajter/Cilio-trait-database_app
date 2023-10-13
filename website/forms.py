from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    keyword_taxon = StringField('Taxon', validators=[DataRequired()])
    keyword_traits = StringField('Traits', validators=[DataRequired()])
    submit = SubmitField('Search')

class LiteratureForm(FlaskForm):
    file = FileField('Upload PDF', validators=[DataRequired()])
    article_name = StringField('Article Name')
    article_link = StringField('Article Link')
    year = IntegerField('Year')
    authors = StringField('Authors')
    journal = StringField('Journal')
    submit = SubmitField('Upload')
