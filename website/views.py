from flask import Flask, render_template, request, redirect, url_for, flash, session
from .forms import LoginForm
import os
from .forms import SearchForm


def init_app(app):

    # @app.route("/")
    # def home():
    #     return render_template("home.html")

    @app.route("/", methods=["GET", "POST"])
    def home():
        form = SearchForm()
        if form.validate_on_submit():
            # Handle your search logic here
            pass
        return render_template("home.html", form=form)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            password = form.password.data  # Use form field data
            if password == os.environ.get('PASSWORD'):
                session['logged_in'] = True  # Set session variable
                flash('Successfully logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Try again.', 'danger')
        return render_template('login.html',
                               form=form)  # form instance to template
