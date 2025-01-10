from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from .db import engine


class Base(DeclarativeBase):
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Ingredient(Base):
    __tablename__ = 'ingredient'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    carbohydrate: Mapped[float]
    protein: Mapped[float]
    fat: Mapped[float]
    portion: Mapped[float]
    create_date: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    create_date: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    id_recipe: Mapped[int] = mapped_column(primary_key=True)
    id_ingredient: Mapped[int] = mapped_column(ForeignKey('recipe.id'))
    quantity : Mapped[float]
    unit: Mapped[str]
    create_date: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

Base.metadata.create_all(engine)