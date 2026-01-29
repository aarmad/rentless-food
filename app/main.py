from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, timedelta
import io
import csv

from . import models, schemas, crud, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rentless Meal Planner")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Dependency to get DB session
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/planner")

# --- RECIPES ---

@app.get("/recipes", response_class=HTMLResponse)
async def list_recipes(request: Request, db: Session = Depends(get_db)):
    recipes = crud.get_recipes(db)
    return templates.TemplateResponse("recipes.html", {"request": request, "recipes": recipes})

@app.get("/recipes/add", response_class=HTMLResponse)
async def add_recipe_form(request: Request):
    return templates.TemplateResponse("recipe_form.html", {"request": request})

@app.post("/recipes/add")
async def create_recipe(
    request: Request,
    title: str = Form(...),
    instructions: str = Form(...),
    total_time: int = Form(...),
    category: str = Form(...),
    # Ingredients will be handled as a JSON string or multiple fields in a real app
    # For simplicity here, we'll parse a text area or use a dynamic JS form
    ingredients_raw: str = Form(...), 
    db: Session = Depends(get_db)
):
    # Parse ingredients_raw (format: "quantité:nom" per line)
    ingredients_list = []
    for line in ingredients_raw.strip().split('\n'):
        if ':' in line:
            q, n = line.split(':', 1)
            ingredients_list.append({"name": n.strip(), "quantity": q.strip()})
    
    recipe_data = schemas.RecipeCreate(
        title=title,
        instructions=instructions,
        total_time=total_time,
        category=category,
        ingredients=ingredients_list
    )
    crud.create_recipe(db, recipe_data)
    return RedirectResponse(url="/recipes", status_code=303)

@app.get("/recipes/delete/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    crud.delete_recipe(db, recipe_id)
    return RedirectResponse(url="/recipes", status_code=303)

# --- PLANNER ---

@app.get("/planner", response_class=HTMLResponse)
async def view_planner(request: Request, db: Session = Depends(get_db)):
    # Calculate current week (Monday to Sunday)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    days = [start_of_week + timedelta(days=i) for i in range(7)]
    
    meal_plans = crud.get_meal_plans(db, days[0], days[-1])
    recipes = crud.get_recipes(db)
    
    # Organize meal plans for the template
    # structure: {date: {meal_type: recipe}}
    plan_data = {d: {"Matin": None, "Midi": None, "Soir": None} for d in days}
    for p in meal_plans:
        plan_data[p.date][p.meal_type] = p.recipe

    return templates.TemplateResponse("planner.html", {
        "request": request, 
        "days": days, 
        "plan_data": plan_data,
        "recipes": recipes
    })

@app.post("/planner/assign")
async def assign_meal(
    date_str: str = Form(...),
    meal_type: str = Form(...),
    recipe_id: int = Form(...),
    db: Session = Depends(get_db)
):
    meal_date = date.fromisoformat(date_str)
    meal_plan = schemas.MealPlanCreate(date=meal_date, meal_type=meal_type, recipe_id=recipe_id)
    crud.create_meal_plan(db, meal_plan)
    return RedirectResponse(url="/planner", status_code=303)

# --- SHOPPING LIST ---

@app.get("/shopping-list", response_class=HTMLResponse)
async def view_shopping_list(request: Request, db: Session = Depends(get_db)):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    meal_plans = crud.get_meal_plans(db, start_of_week, end_of_week)
    shopping_list = utils.generate_shopping_list_data(meal_plans)
    
    return templates.TemplateResponse("shopping_list.html", {
        "request": request, 
        "shopping_list": shopping_list,
        "start": start_of_week,
        "end": end_of_week
    })

@app.get("/shopping-list/csv")
async def export_shopping_list_csv(db: Session = Depends(get_db)):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    meal_plans = crud.get_meal_plans(db, start_of_week, end_of_week)
    shopping_list = utils.generate_shopping_list_data(meal_plans)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Ingrédient", "Quantité"])
    for item in shopping_list:
        writer.writerow([item["name"], item["quantities"]])
    
    return HTMLResponse(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=courses_{start_of_week}.csv"}
    )

@app.get("/shopping-list/pdf")
async def export_shopping_list_pdf(db: Session = Depends(get_db)):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    meal_plans = crud.get_meal_plans(db, start_of_week, end_of_week)
    shopping_list = utils.generate_shopping_list_data(meal_plans)
    
    pdf_buffer = utils.generate_shopping_list_pdf(
        shopping_list, 
        start_of_week.strftime('%d/%m/%Y'), 
        end_of_week.strftime('%d/%m/%Y')
    )
    
    return HTMLResponse(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=courses_{start_of_week}.pdf"}
    )
