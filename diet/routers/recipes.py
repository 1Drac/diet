from flask import Blueprint, render_template, request, flash, url_for, redirect
from sqlalchemy import select
from ..models import Recipe
from ..db import Session, get_items, delete_item, get_item
from ..forms import RecipeForm, validate_existence_in_db


bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/post', methods=('GET', 'POST'))
def post_recipe():

    form = RecipeForm(request.form)
    
    if request.method == 'POST' and form.validate(extra_validators={'name' : [validate_existence_in_db(Recipe)]}):
        
        recipe = Recipe(
                name = form.name.data,
                description = form.description.data,
            )
        with Session.begin() as session:
            session.add(recipe)
            session.commit()

        flash("Recipe created successfully", "success")
        return redirect(url_for('recipes.get_recipes'))
        
    return render_template('recipes/post.html', form=form)

@bp.route('/', methods=('GET', 'POST'))
def get_recipes():

    recipes = get_items(select(Recipe))

    return render_template('recipes/get.html', recipes=recipes)

@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete_recipe(id):

    delete_item(Recipe, id)
    flash("Recipe deleted successfully", "success")
    return redirect(url_for('recipes.get_recipes'))

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
def update_recipe(id):

    recipe = get_items(select(Recipe).where(Recipe.id == id))[0]
    form = RecipeForm(request.form)
    
    if request.method == 'POST' and form.validate(extra_validators={'name' : [validate_existence_in_db(Recipe, id)]}):

        with Session.begin() as session:
            
            recipe = session.get(Recipe, id)
            recipe.name = form.name.data
            recipe.description = form.description.data
            
            session.commit()

        flash("recipe updated successfully", "success")
        return redirect(url_for('recipes.get_recipes'))
        
    return render_template('recipes/update.html', form=form, recipe=recipe)


