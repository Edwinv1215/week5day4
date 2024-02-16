from os import name
from tkinter.tix import Form
from flask import  request, render_template, redirect, url_for,flash
import requests

from  app  import app
from .forms import SignupForm
from .forms import LoginForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user



@app.route("/")
def home():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'wellcome {queried_user.username}!', 'info')
            login_user(queried_user)
            return redirect(url_for('home'))
        else: 
            flash('incorrect username, email or password....please try again', 'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user =User(username, email, password)
        new_user.save()
        flash('success thank you for signing up', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)


        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))    



def get_pokemon_data(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "hp": data["stats"][0]["base_stat"],
            "defense": data["stats"][3]["base_stat"],
            "attack": data["stats"][1]["base_stat"],
            "sprite": data["sprites"]["front_shiny"],
            "ability": data["abilities"][0]["ability"]["name"]
        }
    else:
        return {"error": "Pokemon not found or API error"}
pokemon_names = ['charizard', 'pikachu', 'squirtle', 'bulbasaur', 'charmander', 'raichu']

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = Pokemon=Form()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_identifier = form.name_or_id.data
        pokemons = get_pokemon_data(pokemon_identifier)
        return render_template('pokemon.html', form=form, pokemons=pokemons)
    else:
        return render_template('pokemon.html', form=form)
