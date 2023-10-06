from flask import Flask, render_template, request, redirect, url_for, flash, session
from .forms import LoginForm
import os
from .forms import SearchForm
from .text_search import TaxonTraitTextSearch


def init_app(app):

    # @app.route("/")
    # def home():
    #     return render_template("home.html")

    @app.route("/", methods=["GET", "POST"])
    def home():
        form = SearchForm()
        results = {}  # Initialize results to an empty dictionary
        form_submitted = False  # Initialize form_submitted to False
        if form.validate_on_submit():
            form_submitted = True  # Set form_submitted to True since the form has been submitted
            keyword_taxon = [keyword.strip() for keyword in form.keyword_taxon.data.split(',')]
            keyword_traits = [keyword.strip() for keyword in form.keyword_traits.data.split(',')]
            searcher = TaxonTraitTextSearch(keyword_taxon, keyword_traits)
            results = searcher.search_through_txt()
            # pass 'results' to a template
        return render_template("home.html", form=form, results=results, form_submitted=form_submitted)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            password = form.password.data  # Use form field data
            # if password == os.environ.get('PASSWORD'):
            if password == 'lacrymaria':
                session['logged_in'] = True  # Set session variable
                flash('Successfully logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Try again.', 'danger')
        return render_template('login.html',
                               form=form)  # form instance to template

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/database')
    def database():
        return render_template('database.html')
