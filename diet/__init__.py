from flask import Flask, render_template

from .routers import ingredients, recipes
from .db import engine




app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'dev'

app.register_blueprint(ingredients.bp)
app.register_blueprint(recipes.bp)

@app.route('/', methods=('GET', 'POST'))
def get_home():

    return render_template('home.html')
