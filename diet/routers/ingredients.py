from flask import Blueprint, render_template, request, flash, url_for, redirect
from sqlalchemy import select
from ..models import Ingredient
from ..db import Session, get_items, delete_item, get_item
from ..forms import IngredientForm, validate_existence_in_db
bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

@bp.route('/post', methods=('GET', 'POST'))
def post_ingredient():

    form = IngredientForm(request.form)
    
    if request.method == 'POST' and form.validate(extra_validators={'name' : [validate_existence_in_db(Ingredient)]}):
        ingredient = Ingredient(
                name = form.name.data,
                carbohydrate = form.carbohydrate.data,
                protein = form.protein.data,
                fat = form.fat.data,
                portion = form.portion.data,
            )
        with Session.begin() as session:
            session.add(ingredient)
            session.commit()
        flash("Ingredient created successfully", "success")
        return redirect(url_for('ingredients.get_ingredients'))
        
    return render_template('ingredients/post.html', form=form)

@bp.route('/', methods=('GET', 'POST'))
def get_ingredients():

    ingredients = get_items(select(Ingredient))

    return render_template('ingredients/get.html', ingredients=ingredients)

@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete_ingredient(id):

    delete_item(Ingredient, id)
    flash("Ingredient deleted successfully", "success")
    return redirect(url_for('ingredients.get_ingredients'))

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
def update_ingredient(id):

    ingredient = get_items(select(Ingredient).where(Ingredient.id == id))[0]
    form = IngredientForm(request.form)
    
    if request.method == 'POST' and form.validate(extra_validators={'name' : [validate_existence_in_db(Ingredient, id)]}):

        with Session.begin() as session:
            
            ingredient = session.get(Ingredient, id)
            ingredient.name = form.name.data
            ingredient.carbohydrate = form.carbohydrate.data
            ingredient.protein = form.protein.data
            ingredient.fat = form.fat.data
            ingredient.portion = form.portion.data

            session.commit()

        flash("Ingredient updated successfully", "success")
        return redirect(url_for('ingredients.get_ingredients'))
        
    return render_template('ingredients/update.html', form=form, ingredient=ingredient)


