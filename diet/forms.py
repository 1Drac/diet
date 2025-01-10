from wtforms import Form, StringField, DecimalField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from sqlalchemy import select

from .db import Session
from .models import Base

def validate_existence_in_db(table, id: int | None = None):
    message = f'{table.__name__} already exist'
    
    def _validate_existence_in_db(form, field):
        with Session.begin() as session:

            if id is None:
                if session.scalars(select(table).where(table.name == field.data)).first():
                    raise ValidationError(message)
            else:
                if session.scalars(select(table).where((table.name == field.data) & (table.id != id ))).first():
                    raise ValidationError(message)
        
    return _validate_existence_in_db

class CustomDataRequired(DataRequired):
    def __call__(self, form, field):
        self.message = self.message or f"{field.label.text} is required."
        super().__call__(form, field)

class CustomInputRequired(InputRequired):
    def __call__(self, form, field):
        self.message = self.message or f"{field.label.text} is required."
        super().__call__(form, field)

class IngredientForm(Form):

    name =  StringField('Ingredient name', [CustomDataRequired()])
    carbohydrate = DecimalField('Carbohydrate', [CustomInputRequired()])
    protein = DecimalField('Protein', [CustomInputRequired()])
    fat = DecimalField('Fat', [CustomInputRequired()])
    portion = DecimalField('Portion', [CustomInputRequired()])

class RecipeForm(Form):

    name =  StringField('Recipe name', [CustomDataRequired()])
    description =  StringField('Recipe name', [CustomDataRequired()])
