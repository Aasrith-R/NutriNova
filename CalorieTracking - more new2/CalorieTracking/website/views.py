from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user, logout_user
from . import db
from .models import Note, User, Calorie, Calo, Cal, Cars, Food, Log, Calor, Form, Recs, Snacks, Dkey, Cali, Message
from datetime import datetime
import sys
import json
from pyzbar.pyzbar import decode
from PIL import Image
import requests

from functools import wraps
import random
global TARGETCALORIES3
global NUMLOGIN
views = Blueprint('views', __name__)
global DUP2_NOTE
global OUTPUT
OUTPUT = None
DUP2_NOTE = None
global EDISORDEER
EDISORDEER = None
global TCALORIES
TCALORIES = None
global TARGET_CALORIES_29
TARGET_CALORIES_29 = None
global SNACK
SNACK = None
global M
M = 0
from datetime import datetime 

def form_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        existing_note = Form.query.filter_by(user_id=current_user.id).first()
        if not existing_note:
            flash("Please fill out the form", category='warning')
            return redirect(url_for('views.home'))

        return f(*args, **kwargs)
    return decorated_function

graph = {
  'Anorexia' : ['Grilled Chicken and Quinoa Salad (400 cal)', 'Salmon and Sweet Potato Bowl (450 cal)', 'Greek Yogurt Parfait with Berries and Nuts (500 cal)'],
  'Grilled Chicken and Quinoa Salad (400 cal)' : [400],
   400 : [],
  'Salmon and Sweet Potato Bowl (450 cal)' : [450],
  450 : [],
  'Greek Yogurt Parfait with Berries and Nuts (500 cal)' : [500],
  500 : [],
  
  'Bulimia' : ['Vegetable Stir-Fry with Tofu and Brown Rice (400 cal)', 'Turkey and Avocado Wrap (450 cal)', 'Chickpea and Vegetable Curry(400)'],
  'Vegetable Stir-Fry with Tofu and Brown Rice (400 cal)' : [400],
   400 : [],
  'Turkey and Avocado Wrap (450 cal)' : [450],
  450 : [],
  'Chickpea and Vegetable Curry(400)' : [500],
  500 : []
}

graph2 = {
    'Anorexia': ['Grilled Chicken and Quinoa Salad (400 cal)', 'Salmon and Sweet Potato Bowl (450 cal)', 'Greek Yogurt Parfait with Berries and Nuts (500 cal)'],
    'Grilled Chicken and Quinoa Salad (400 cal)': ['8:00 AM'],
    'Salmon and Sweet Potato Bowl (450 cal)': ['1:00 PM'],
    'Greek Yogurt Parfait with Berries and Nuts (500 cal)': ['6:00 PM'],
    
    'Bulimia': ['Vegetable Stir-Fry with Tofu and Brown Rice (400 cal)', 'Turkey and Avocado Wrap (450 cal)', 'Chickpea and Vegetable Curry (400 cal)'],
    'Vegetable Stir-Fry with Tofu and Brown Rice (400 cal)': ['8:00 AM'],
    'Turkey and Avocado Wrap (450 cal)': ['1:00 PM'],
    'Chickpea and Vegetable Curry (400 cal)': ['6:00 PM']
}


visited = [] # List for visited nodes.
queue = []     #Initialize a queue



def get_food_recommendations(eating_disorder):
    food_recommendations = {
        'Anorexia': ['Avocado', 'Nuts', 'Olive Oil'],
        'Bulimia': ['Bananas', 'Sweet Potatoes', 'Lean Protein'],
        'Binge eating': ['Fruits', 'Vegetables', 'Whole Grains'],
        'Pica': ['Milk', 'Potatoes', 'Eggs'],
        'Rumination Disorder': ['Non-citrus fruits', 'Tender meat', 'Mashed Potatoes'],
        'Night eating syndrome': ['Tofu', 'Strawberries', 'Yogurt with granola'],
        'OSFED': ['Quinoa', 'Almonds', 'Beans'],
        'Diabulimia': ['Brown Bread', 'Cashew', 'Onions'],
        'Purging Disorder': ['Fish', 'Legumes', 'Lentils'],
        'Muscle Dysmorphoia': ['Poultry', 'Chia seed', 'Crackers'],
        
    }

    return food_recommendations.get(eating_disorder, 'No food recommendations available')

def get_dish_recommendations(eating_disorder):
    dish_recommendations = {
        'Anorexia': ['1. Grilled Chicken and Quinoa Salad (400 cal)', '2. Salmon and Sweet Potato Bowl (450 cal)', '3. Greek Yogurt Parfait with Berries and Nuts (500 cal)'],
        'Bulimia': ['1. Vegetable Stir-Fry with Tofu and Brown Rice (400 cal)', '2. Turkey and Avocado Wrap (450 cal)', '3. Chickpea and Vegetable Curry(400)'],
        'Binge eating': ['1. Lentil and Vegetable Soup (350 cal)', '2. Baked Salmon with Asparagus and Brown Rice (400 cal)', '3. Chickpea and Avocado Salad (450 cal)'],
        'Pica': ['1. Spinach and Chickpea Stew (300 cal)', '2. Beef and Vegetable Stir-Fry (450 cal)', '3. Fortified Cereal with Milk and Berries (400 cal)'],
        'Rumination Disorder': ['1. Poached Chicken and Vegetable Soup (330 cal)', '2. Oatmeal with Banana and Almond Butter (370 cal)', '3. Steamed Fish with Sweet Potato and Green Beans (470 cal)'],
        'Night eating syndrome': ['1. Quinoa and Vegetable Stir-Fry (400 cal)', '2. Greek Yogurt Parfait with Berries and Nuts (500 cal)', '3. Baked Salmon with Sweet Potato and Asparagus (500 cal)'],
        'OSFED': ['1. Chicken and Vegetable Stir-Fry (400 cal)', '2. Lentil and Spinach Salad (400 cal)', '3. Salmon and Sweet Potato Bowl (500 cal)'],
        'Diabulimia': [' 1. Grilled Chicken with Quinoa and Roasted Vegetables (400 cal)' , '2. Salmon and Spinach Salad (510 cal)', '3. Greek Yogurt and Berry Parfait (480 cal)'],
        'Purging Disorder': ['1. Vegetable and Lentil Soup (350 cal)', '2. Baked Chicken with Roasted Vegetables (400 cal)', '3. Greek Yogurt Smoothie Bowl (450 cal)'],
        'Muscle Dysmorphoia': ['1. Grilled Steak with Sweet Potato and Steamed Broccoli (470 cal)', '2. Quinoa and Black Bean Bowl with Avocado (510 cal)', '3. Chicken and Vegetable Stir-Fry with Brown Rice (480 cal)'],
        
    }

    return dish_recommendations.get(eating_disorder, 'No dish recommendations available')

def bfss(visited, graph, node): #function for BFS
  global M
  global N
  visited.append(node)
  queue.append(node)
  while queue:  # Creating loop to visit each node
    M = queue.pop(0)


    for neighbour in graph[M]:
        if neighbour not in visited:
            if neighbour == "8:00 AM":
                N = graph[M]
            visited.append(neighbour)
            queue.append(neighbour)

def bfs(visited, graph, node): #function for BFS
  global TARGET_CALORIES_29

  visited.append(node)
  queue.append(node)
  while queue:  # Creating loop to visit each node
    m = queue.pop(0)
    
    if TARGET_CALORIES_29 > 0:
        if isinstance(m, int):  # Check if m is an integer
            TARGET_CALORIES_29 -= m
            print(TARGET_CALORIES_29)


    for neighbour in graph[m]:
        if neighbour not in visited:
            visited.append(neighbour)
            queue.append(neighbour)


def calculate_calories(weight, gender, height, age, activity):
    if gender == 'male':
        b_m_r = 10 * weight + 6.25 * height - 5 * age + 5
        b_m_r = b_m_r * activity
    elif gender == 'female':
        b_m_r = 10 * weight + 6.25 * height - 5 * age - 161
        b_m_r = b_m_r * activity 

    
    return b_m_r

TARGETCALORIES3 = None
@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():

    global TARGETCALORIES3
    global EDISORDEER
    global TCALORIES
    global TARGET_CALORIES_29
    existing_note2 = Form.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST': 
        age = float(request.form.get('age'))
        EDISORDEER = request.form.get('e-disordeer')
        weight = float(request.form.get('weight'))
        activity = float(request.form.get('activity-level'))
        height = float(request.form.get('height'))
        gender = request.form.get('gender')
        goal = request.form.get('goal')
        if age < 4:
           flash('Email must be greater than 3 characters.', category='error')
        elif weight < 2:
           flash('First name must be greater than 1 character.', category='error')
        elif activity < 0:
           flash('First name must be greater than 1 character.', category='error')
        elif height < 0:
           flash('First name must be greater than 1 character.', category='error')
        elif EDISORDEER is None:
           flash('First name must be greater than 1 character.', category='error')
        elif gender is None:
           flash('First name must be greater than 1 character.', category='error')
        elif goal is None:
           flash('First name must be greater than 1 character.', category='error')
        else:
            both = f"age: {age}, disorder: {EDISORDEER}, weight: {weight}, activity: {activity}, height: {height}, height: {gender}, goal: {goal}"
            new_form = Form(age=age, activity=activity, disorder=EDISORDEER, weight=weight, gender=gender, height=height, goal=goal, user_id=current_user.id, data=both)
            db.session.add(new_form)
            db.session.commit()
            print(activity)
            print(gender)
            print(goal)
            new_form = Calor(goal=goal, user_id=current_user.id, )
            db.session.add(new_form)
            db.session.commit()
            if activity == 1:
                activity = 1.2
            elif activity == 2:
                activity = 1.35
            elif activity == 3:
                activity = 1.5
            elif activity == 4:
                activity = 1.65
            elif activity == 5:
                activity = 1.8
            elif activity == 6:
                activity = 1.95
            
            user_eating_disorder = EDISORDEER

            recommendations = get_food_recommendations(user_eating_disorder)
            drecommendations = get_dish_recommendations(user_eating_disorder)
            print(f"Recommendations for {user_eating_disorder}: {drecommendations}")
            print(f"Recommendations for {user_eating_disorder}: {recommendations}")

            TCALORIES = calculate_calories(weight, gender, height, age, activity)
            print(TCALORIES)
            tcalories2 = TCALORIES - 500
            tcalories3 = TCALORIES + 500
            new_for2 = Cali(user_id=current_user.id, targetcalories=TCALORIES, targetcalories2 = tcalories2, targetcalories3 = tcalories3)
            db.session.add(new_for2)
            db.session.commit()
            cal_rec = f"Target Calories for a {gender}: {TCALORIES}, deficit: {tcalories2}, surplus: {tcalories3}."
            new_form = Recs(user_id=current_user.id, data=cal_rec)
            db.session.add(new_form)
            db.session.commit()
            if goal == 'gain-weight':
                TARGETCALORIES3 = tcalories3
            elif goal == 'lose-weight':
                TARGETCALORIES3 = tcalories2
            elif goal == 'same':
                TARGETCALORIES3 = TCALORIES
            rs = random.choice(('Smoothie with Banana, Spinach, and Protein powder- 450 cal', 'Hummus with veggie sticks- 250 cal', 'Trail Mix- 500 cal', 'Apple slices with almond butter- 300 cal', 'Avacado toast- 300 cal', 'Nut Butter and Banana Sandwich- 500 cal') )
            print(f"Target Calories for a {gender}: {TCALORIES}, deficit: {tcalories2}, surplus: {tcalories3}")
            TARGET_CALORIES_29 = TCALORIES
            print("Following is the Breadth-First Search")
            print(TCALORIES)
            bfs(visited, graph, user_eating_disorder)

            SNACK = None
            if TARGET_CALORIES_29 > 20:
                rs = random.choice(('Smoothie with Banana, Spinach, and Protein powder', 'Hummus with veggie sticks', 'Trail Mix', 'Apple slices with almond butter', 'Avacado toast', 'Nut Butter and Banana Sandwich') )
                SNACK = f"{rs} ({TARGET_CALORIES_29})"
            print(SNACK)
            Snacks.query.delete()
            new_form = Snacks(user_id=current_user.id, data=SNACK)
            db.session.add(new_form)
            db.session.commit()
            disorder_meals = graph2['Anorexia']
            print(disorder_meals)
            print(disorder_meals[1])
            new_note = Calo(data=TARGETCALORIES3, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html', existing_note=existing_note2)

@views.route('/airecommendations', methods =['POST', 'GET'])
@login_required
@form_required
def airecommendations():
    global SNACK, TARGET_CALORIES_29
    existing_note = Form.query.filter_by(user_id=current_user.id).first()
    existing_notes = Recs.query.filter_by(user_id=current_user.id).first()
    existing_notess = Snacks.query.filter_by(user_id=current_user.id).first()
    existing_nots = Cali.query.filter_by(user_id=current_user.id).first()


    print(SNACK)
    disorder_meals = graph2['Anorexia']
    print(disorder_meals)
    print(disorder_meals[1])
    disorder_meals1 = disorder_meals[0]
    disorder_meals2 = disorder_meals[1]
    disorder_meals3 = disorder_meals[2]
    return render_template('airecommendations.html', existing_note=existing_note.data, existing_notes=existing_notes.data, existing_notess=existing_notess.data, disorder_meals1=disorder_meals[0], disorder_meals2=disorder_meals[1], disorder_meals3=disorder_meals[2], existing_nots = existing_nots.targetcalories,existing_nots2 = existing_nots.targetcalories2, existing_nots3 = existing_nots.targetcalories3)

def target_calories_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if TARGETCALORIES3 == None:
            flash("Please set your target calories first.", category='warning')
            return redirect(url_for('views.home'))
        else:
            print("working")
        return f(*args, **kwargs)
    return decorated_function


@views.route('/get_target_calories', methods=['GET'])
@login_required
def get_target_calories():
    if TARGETCALORIES3:
        return jsonify({'target_calories': TARGETCALORIES3})
    else:
        return jsonify({'target_calories': 0})
    

    
@views.route('/indo')
def indo():
    return render_template('indo.html')

@views.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('indo'))
    
    file = request.files['file']
    image = Image.open(file.stream)
    
    # Decode the QR code
    decoded_objects = decode(image)
    if not decoded_objects:
        return "No QR code found"
    
    barcode_data = decoded_objects[0].data.decode('utf-8')
    
    # Call the food database API with the decoded barcode
    food_info = get_food_info(barcode_data)
    
    return render_template('result.html', food_info=food_info)

def get_food_info(barcode):
    API_URL = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:
            product = data.get('product', {})
            return {
                'name': product.get('product_name', 'N/A'),
                'calories': product.get('nutriments', {}).get('energy-kcal', 'N/A'),
                'carbs': product.get('nutriments', {}).get('carbohydrates_100g', 'N/A'),
                'protein': product.get('nutriments', {}).get('proteins_100g', 'N/A'),
                'fat': product.get('nutriments', {}).get('fat_100g', 'N/A')
            }
    return {"error": "Food item not found"}


@views.route('/eatingdisorders')
@login_required
def contact():
    return render_template('eating-disorders.html')

@views.route('/achievements')
@login_required
def achievements():
    return render_template('achievements.html')


@views.route('/about')
@login_required
def about():
    existing_notess = Dkey.query.filter_by(user_id=current_user.id).first()

    return render_template('about.html', existing_notess=existing_notess.dkey)

@views.route('/abouts')
def abouts():
    return render_template('abouts.html')


@views.route('/delete-note', methods = ['POST'])     
def delete_note():
    note_id = request.form.get('note_id')

    if note_id:
        # Retrieve the note from the database
        note = Note.query.get(note_id)

        if note and note.user_id == current_user.id:
            # Delete the note if it belongs to the current user
            db.session.delete(note)
            db.session.commit()
            return redirect(url_for('views.calorie'))
            

    return jsonify({'error': 'Failed to delete note'}), 400
            


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@views.route('/create_log', methods=['POST'])
def create_log():
    date = request.form.get('date')

    log = Log(date=datetime.strptime(date, '%Y-%m-%d'))

    db.session.add(log)
    db.session.commit()
    print("hello")
    return redirect(url_for('views.view', log_id=log.id))

@views.route('/dkey2')
def dkey2():
    return render_template('chat2.html')

@views.route('/user_chat')
def userchat():
    if 'user_id' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('auth.login'))

    return render_template('chat.html')

@views.route('/calorie')
@login_required
def index():
    logs = Log.query.order_by(Log.date.desc()).all()

    log_dates = []

    for log in logs:
        proteins = 0
        carbs = 0
        fats = 0
        calories = 0

        for food in log.foods:
            proteins += food.proteins
            carbs += food.carbs 
            fats += food.fats
            calories += food.calories

        log_dates.append({
            'log_date' : log,
            'proteins' : proteins,
            'carbs' : carbs,
            'fats' : fats,
            'calories' : calories
        })
    print("hello10")
    return render_template('index.html', log_dates=log_dates)

@views.route('/index2')
@login_required
def index2():
    logs = Log.query.order_by(Log.date.desc()).all()

    log_dates = []

    for log in logs:
        proteins = 0
        carbs = 0
        fats = 0
        calories = 0

        for food in log.foods:
            proteins += food.proteins
            carbs += food.carbs 
            fats += food.fats
            calories += food.calories

        log_dates.append({
            'log_date' : log,
            'proteins' : proteins,
            'carbs' : carbs,
            'fats' : fats,
            'calories' : calories
        })
    print("hello10")
    return render_template('indexcopy.html', log_dates=log_dates)

@views.route('/')
def base():
    return render_template('landingpage.html')

@views.route('/add')
def add():
    foods = Food.query.all()
    print("hello8")
    return render_template('add.html', foods=foods, food=None)

@views.route('/add', methods=['POST'])
def add_post():
    food_name = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbs = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    food_id = request.form.get('food-id')

    if food_id:
        food = Food.query.get_or_404(food_id)
        food.name = food_name
        food.proteins = proteins
        food.carbs = carbs
        food.fats = fats

    else:
        new_food = Food(
            name=food_name,
            proteins=proteins, 
            carbs=carbs, 
            fats=fats
        )
    
        db.session.add(new_food)

    db.session.commit()
    print("hello7")
    return redirect(url_for('views.add'))

@views.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    print("hello6")
    return redirect(url_for('views.add'))

@views.route('/edit_food/<int:food_id>')
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)
    foods = Food.query.all()
    print("hello5")
    return render_template('add.html', food=food, foods=foods)
    
@views.route('/view/<int:log_id>')
def view(log_id):
    global TARGETCALORIES3
    global DUP2_NOTE
    log = Log.query.get_or_404(log_id)

    foods = Food.query.all()

    totals = {
        'protein' : 0,
        'carbs' : 0,
        'fat' : 0,
        'calories' : 0
    }

    for food in log.foods:
        totals['protein'] += food.proteins
        totals['carbs'] += food.carbs
        totals['fat'] += food.fats 
        totals['calories'] += food.calories
        total = int(totals['calories'])
        print(TARGETCALORIES3) 
        if (TARGETCALORIES3 == None):
            DUP2_NOTE = None
            
        if DUP2_NOTE == None:
            existing_note = Calo.query.filter_by(user_id=current_user.id).first()

            dup_note = Cal(data=existing_note.data, user_id=current_user.id)#step 2
                
            TARGETCALORIES3 = float(dup_note.data)
            TARGETCALORIES3 = float(TARGETCALORIES3)
            
        TARGETCALORIES3 -= total
        totally = f""
        if (TARGETCALORIES3 < 0):
            TARGETCALORIES3 = None
            print("fatfuck")
            surp = f"surpassed"
            up_note = Calorie(data=surp, user_id = current_user.id)
        elif TARGETCALORIES3 == 0:
            met = f"met the goal"
            up_note = Calorie(data=met, user_id = current_user.id)
        else: # might make it crash
            good = f"need more"
            up_note = Calorie(data=good, user_id = current_user.id)
            DUP2_NOTE = Cal(data=TARGETCALORIES3, user_id=current_user.id)
            db.session.add(DUP2_NOTE)
            db.session.commit()   
    print("hello4")
    return render_template('view.html', foods=foods, log=log, totals=totals, TARGETCALORIES3=TARGETCALORIES3)

@views.route('/view2/<int:log_id>')
def view2(log_id):
    global TARGETCALORIES3

    log = Log.query.get_or_404(log_id)

    foods = Food.query.all()

    totals = {
        'protein' : 0,
        'carbs' : 0,
        'fat' : 0,
        'calories' : 0
    }

    for food in log.foods:
        totals['protein'] += food.proteins
        totals['carbs'] += food.carbs
        totals['fat'] += food.fats 
        totals['calories'] += food.calories
        total = int(totals['calories'])
        print(TARGETCALORIES3) 
        if (TARGETCALORIES3 == None):
            DUP2_NOTE = None
            
        if DUP2_NOTE == None:
            existing_note = Calo.query.filter_by(user_id=current_user.id).first()

            dup_note = Cal(data=existing_note.data, user_id=current_user.id)#step 2
                
            TARGETCALORIES3 = float(dup_note.data)
            TARGETCALORIES3 = float(TARGETCALORIES3)
            
        TARGETCALORIES3 -= total
        totally = f""
        if (TARGETCALORIES3 < 0):
            TARGETCALORIES3 = None
            print("fatfuck")
            surp = f"surpassed"
            up_note = Calorie(data=surp, user_id = current_user.id)
        elif TARGETCALORIES3 == 0:
            met = f"met the goal"
            up_note = Calorie(data=met, user_id = current_user.id)
        else: # might make it crash
            good = f"need more"
            up_note = Calorie(data=good, user_id = current_user.id)
            DUP2_NOTE = Cal(data=TARGETCALORIES3, user_id=current_user.id)
            db.session.add(DUP2_NOTE)
            db.session.commit()   
    print("hello4")
    return render_template('viewcopy.html', foods=foods, log=log, totals=totals, TARGETCALORIES3=TARGETCALORIES3)

@views.route('/add_food_to_log/<int:log_id>', methods=['POST'])
def add_food_to_log(log_id):
    log = Log.query.get_or_404(log_id)

    selected_food = request.form.get('food-select')

    food = Food.query.get(int(selected_food))
    log.foods.append(food)
    db.session.commit()
    print("hello3")
    return redirect(url_for('views.view', log_id=log_id))

@views.route('/remove_food_from_log/<int:log_id>/<int:food_id>')
def remove_food_from_log(log_id, food_id):
    log = Log.query.get(log_id)
    food = Food.query.get(food_id)
    log.foods.remove(food)
    db.session.commit()
    print("hello2")

    return redirect(url_for('views.view', log_id=log_id))



@views.route('/index1')
def main():
    return render_template('index1.html')

