from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from .forms import LoginForm, SearchForm, LiteratureForm
from .text_search import TaxonTraitTextSearch
from .database import Database

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

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        form = LiteratureForm()
        print(f"Form Data: {form.data}")  # Print form data
        print(f"Form Errors: {form.errors}")  # Print form errors
        if form.validate_on_submit():
            article_name = form.article_name.data or 'NA'
            article_link = form.article_link.data or 'NA'
            year = form.year.data or 'NA'
            authors = form.authors.data or 'NA'
            journal = form.journal.data or 'NA'
            f = form.file.data # retrieves the uploaded file from the form.
            # upload file to the disk
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure directory exists
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            print(file_path)
            f.save(file_path)

            # Now you can create a Database object and call its methods
            db = Database(file_path)
            paragraphs = db.extract_paragraphs_from_pdf()
            db.save_to_txt(paragraphs)
            data_row = [db.file_name, article_name, article_link, year, authors, journal]
            db.add_to_tsv(data_row)

            # After processing, you might want to redirect to a success page or the like
            return redirect(url_for('success'))

        return render_template('upload.html', form=form)

    @app.route('/success')
    def success():
        return "File uploaded successfully!"
