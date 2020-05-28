import json
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SelectForm, LoginForm

@app.route('/')
# def content():
#     filepath = url_for('static', filename='select_form_values.json')
#     with open(filepath, 'r') as file:
#         select_form_values = json.load(file)
@app.route('/index')
def index():
    user = {'username': 'Jon-Marshall'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SelectForm()
    results = None
    return render_template('search.html', title='Search', form=form, results=results)