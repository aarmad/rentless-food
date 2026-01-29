from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

# Recipes
def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        title=recipe.title,
        instructions=recipe.instructions,
        total_time=recipe.total_time,
        category=recipe.category
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    for ing in recipe.ingredients:
        db_ing = models.Ingredient(**ing.dict(), recipe_id=db_recipe.id)
        db.add(db_ing)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
    return db_recipe

# Meal Plans
def get_meal_plans(db: Session, start_date: date, end_date: date):
    return db.query(models.MealPlan).filter(models.MealPlan.date >= start_date, models.MealPlan.date <= end_date).all()

def create_meal_plan(db: Session, meal_plan: schemas.MealPlanCreate):
    # Remove existing meal plan for that day and meal type if exists
    db.query(models.MealPlan).filter(
        models.MealPlan.date == meal_plan.date,
        models.MealPlan.meal_type == meal_plan.meal_type
    ).delete()
    
    db_meal_plan = models.MealPlan(**meal_plan.dict())
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

def get_weekly_summary(db: Session, start_date: date, end_date: date):
    return db.query(models.MealPlan).filter(
        models.MealPlan.date >= start_date,
        models.MealPlan.date <= end_date
    ).all()
