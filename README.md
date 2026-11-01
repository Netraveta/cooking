# 🍰 NANO'S CRAVING CO. — Recipe World 🍽️
**A Modern, Girly-Aesthetic & Beginner-Friendly Recipe Finder Website**

Built with **Python (Flask)**, **SQLite**, **HTML5**, **CSS3**, and **JavaScript**.

---

## 🌟 Project Highlights

- **Aesthetic Girly Theme**: Palette of creamy vanilla, light sage green, pastel peach/orange, and soft blush pink.
- **Total 50 Distinct Recipes**: Exactly 10 Mexican, 10 Italian, 10 Indian, 10 Chinese, and 10 American recipes.
- **50 Individual Food Images**: High-quality photography with offline-ready dedicated local SVG graphics for every recipe.
- **Food Image Position**: Every card prominently features the food image **ABOVE** the recipe name and ingredients.
- **Live Search & Multi-Criteria Filtering**: Search by recipe name or ingredients; filter by country, dietary preference (Veg / Non-Veg / Vegan), and cooking time.
- **Personalized Recommendations**: 5-detail user form (Name, Age, Diet, Favorite Cuisine, Allergies) that saves to SQLite and algorithmically excludes allergens while highlighting favorite cuisines.
- **Interactive Features**: Favorites system (heart toggle with instant counter), interactive cooking ingredients checklist (check off items as you cook!), and mobile hamburger drawer.

---

## 📁 Project Structure

```
recipe_finder/
│
├── app.py                  # Flask backend routes, sessions & context processor
├── database.py             # SQLite database management, tables & SQL queries
├── recipes_data.py         # Complete 50-recipe dataset (ingredients, instructions, images)
├── recipes.db              # SQLite database file (auto-generated & auto-seeded)
│
├── templates/
│   ├── base.html           # Master layout with navigation bar, flash alerts & footer
│   ├── index.html          # Home page with hero search, categories & popular picks
│   ├── recipes.html        # All 50 recipes with real-time live search & multi-filter
│   ├── recipe_details.html # Detailed view with large photo, checklist & instructions
│   ├── preferences.html    # User Details 5-item form for personalized recommendations
│   ├── suggestions.html    # Personalised recommendations tailored to user profile
│   └── favourites.html     # Saved recipes collection
│
└── static/
    ├── style.css           # Modern, girly-attractive, fully responsive styling
    ├── script.js           # Live search, filter logic, AJAX favorites & checklist
    └── images/             # 50 dedicated food SVG visuals (recipe_1.svg ... recipe_50.svg)
```

---

## 🚀 How to Run in VS Code

### 1. Open Terminal in VS Code
Open the project folder in VS Code, then open the integrated terminal:
`Ctrl + \`` (backtick) or go to **Terminal > New Terminal**.

### 2. Navigate to the project directory
```bash
cd recipe_finder
```

### 3. Install Flask (if not already installed)
```bash
pip install flask
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Your Browser
Click on the link in your terminal or open your browser and visit:
👉 **`http://127.0.0.1:5000`**

---

## 🧠 How the Backend & Database Work

1. **Flask (`app.py`)**:
   - Manages routing for the Home page (`/`), All Recipes (`/recipes`), Recipe Details (`/recipe/<id>`), User Preferences (`/preferences`), Suggestions (`/suggestions`), and Favourites (`/favourites`).
   - Serves an asynchronous JSON API (`/api/favourite/toggle`) for instant heart clicks without page reloads.

2. **SQLite Database (`database.py` & `recipes.db`)**:
   - **`recipes` table**: Stores recipe ID, name, cuisine, dietary category, prep time, cook time, servings, difficulty, description, ingredients list, instructions, and image URLs.
   - **`user_profiles` table**: Stores user preferences (Full Name, Age, Food Preference, Favourite Cuisine, Allergies).
   - **`favourites` table**: Stores favorited recipe IDs linked by foreign key.
   - **`contact_messages` table**: Stores messages sent via the contact form.

3. **Recommendation Algorithm**:
   - Compares the user's food preference (Vegetarian, Vegan, Non-Vegetarian).
   - Scans the ingredients text of each recipe against the user's allergy keywords and excludes any matches.
   - Prioritizes top dishes matching the user's favorite cuisine.
