from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class IngredientBase(BaseModel):
    name: str
    quantity: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    title: str
    instructions: str
    total_time: int
    category: str

class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate]

class Recipe(RecipeBase):
    id: int
    ingredients: List[Ingredient]

    class Config:
        orm_mode = True

class MealPlanBase(BaseModel):
    date: date
    meal_type: str
    recipe_id: int

class MealPlanCreate(MealPlanBase):
    pass

class MealPlan(MealPlanBase):
    id: int
    recipe: Recipe

    class Config:
        orm_mode = True
