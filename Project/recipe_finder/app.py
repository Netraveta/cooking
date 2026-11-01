# ==============================================================================
# NANO'S CRAVING CO. - Flask Application Backend
# A modern, beginner-friendly Recipe Finder web application.
# ==============================================================================

import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

try:
    from recipe_finder.database import (
        init_db,
        get_all_recipes,
        get_recipe_by_id,
        get_popular_recipes,
        save_user_profile,
        get_user_profile_by_id,
        get_latest_user_profile,
        get_favourite_ids,
        toggle_favourite,
        get_favourite_recipes,
        get_personalised_recommendations,
        save_contact_message
    )
except ImportError:
    from database import (
        init_db,
        get_all_recipes,
        get_recipe_by_id,
        get_popular_recipes,
        save_user_profile,
        get_user_profile_by_id,
        get_latest_user_profile,
        get_favourite_ids,
        toggle_favourite,
        get_favourite_recipes,
        get_personalised_recommendations,
        save_contact_message
    )

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "nanos-craving-co-girly-cozy-secret-key-2026"

# Ensure database tables exist and are seeded upon launch
with app.app_context():
    init_db()


# ------------------------------------------------------------------------------
# Context Processor (makes favorites count available to all templates)
# ------------------------------------------------------------------------------
@app.context_processor
def inject_global_data():
    fav_ids = get_favourite_ids()
    latest_profile = None
    if "user_id" in session:
        latest_profile = get_user_profile_by_id(session["user_id"])
    if not latest_profile:
        latest_profile = get_latest_user_profile()

    return {
        "fav_count": len(fav_ids),
        "fav_ids": fav_ids,
        "current_user_profile": latest_profile
    }


# ------------------------------------------------------------------------------
# 1. Front Page Route (No-Scroll User Options Gate)
# ------------------------------------------------------------------------------
@app.route("/")
def index():
    """
    Renders the Front Page with User Options.
    Designed to fit strictly within 100vh with NO SCROLLING required.
    Locks other pages until user submits options or chooses to explore.
    """
    fav_ids = get_favourite_ids()
    latest_profile = None
    if "user_id" in session:
        latest_profile = get_user_profile_by_id(session["user_id"])
    if not latest_profile:
        latest_profile = get_latest_user_profile()

    return render_template(
        "front_gate.html",
        current_user_profile=latest_profile,
        fav_ids=fav_ids
    )


@app.route("/enter", methods=["POST"])
def enter_site():
    """
    Processes the Front Page User Options:
    - Full Name
    - Food Preference (Both Veg & Non-Veg / Vegetarian / Non-Vegetarian / Vegan)
    - Quantity (People Eating)
    - Favourite Cuisine
    - Allergies
    Saves to SQLite and unlocks the full website!
    """
    name = request.form.get("name", "").strip() or "Foodie Friend"
    preference = request.form.get("preference", "Both (Veg & Non-Veg)").strip()
    people_count_str = request.form.get("people_count", "2").strip()
    favourite_cuisine = request.form.get("favourite_cuisine", "Italian").strip()
    allergies = request.form.get("allergies", "").strip()

    try:
        people_count = int(people_count_str)
        if people_count < 1:
            people_count = 1
    except ValueError:
        people_count = 2

    # Save to SQLite database
    user_id = save_user_profile(
        name=name,
        age=20,
        preference=preference,
        favourite_cuisine=favourite_cuisine,
        allergies=allergies,
        people_count=people_count
    )

    # Store in session
    session["user_id"] = user_id
    session["people_count"] = people_count
    session["unlocked"] = True

    flash(f"Welcome, {name}! Recipe World is now unlocked for {people_count} {'person' if people_count == 1 else 'people'} 💖", "success")
    return redirect(url_for("suggestions"))


@app.route("/explore")
def explore_site():
    """
    Full Home Page featuring:
    - Hero section with search
    - 5 international food category cards
    - Handpicked popular recipes
    - Backstory and Contact form
    """
    session["unlocked"] = True
    popular_recipes = get_popular_recipes(limit=6)
    fav_ids = get_favourite_ids()

    categories = [
        {"name": "Mexican", "flag": "🌮", "bg": "#FFE5D9", "text": "10 Recipes", "desc": "Zesty, vibrant & cheesy street favorites"},
        {"name": "Italian", "flag": "🍕", "bg": "#FFF3CD", "text": "10 Recipes", "desc": "Authentic pastas, pizzas & velvety desserts"},
        {"name": "Indian", "flag": "🍛", "bg": "#FFCCD5", "text": "10 Recipes", "desc": "Aromatic curries, rich biryanis & crispy bites"},
        {"name": "Chinese", "flag": "🥟", "bg": "#E8F5E9", "text": "10 Recipes", "desc": "Wok-tossed noodles, dumplings & savory glazes"},
        {"name": "American", "flag": "🍔", "bg": "#FDE2E4", "text": "10 Recipes", "desc": "Comfort burgers, fluffy pancakes & loaded pies"}
    ]

    return render_template(
        "index.html",
        popular_recipes=popular_recipes,
        categories=categories,
        fav_ids=fav_ids
    )


# ------------------------------------------------------------------------------
# 2. All Recipes Page Route (with multi-criteria search and filters)
# ------------------------------------------------------------------------------
@app.route("/recipes")
def recipes():
    """
    Displays all 50 recipes with support for:
    - Search by recipe name or ingredients
    - Filter by Country/Cuisine (Mexican, Italian, Indian, Chinese, American)
    - Filter by Dietary Preference (Vegetarian, Non-Vegetarian, Vegan)
    - Filter by Cooking Time (<20m, <30m, 45m+)
    """
    all_recipes_list = get_all_recipes()
    fav_ids = get_favourite_ids()

    # Query parameters from GET request
    search_query = request.args.get("search", "").strip().lower()
    selected_cuisine = request.args.get("cuisine", "").strip()
    selected_dietary = request.args.get("dietary", "").strip()
    selected_time = request.args.get("time", "").strip()

    filtered_recipes = []
    for r in all_recipes_list:
        # Search by name or ingredients
        if search_query:
            match_name = search_query in r["name"].lower()
            match_ing = search_query in r["ingredients"].lower()
            if not (match_name or match_ing):
                continue

        # Filter by Cuisine
        if selected_cuisine and selected_cuisine != "All":
            if r["cuisine"].lower() != selected_cuisine.lower():
                continue

        # Filter by Dietary
        if selected_dietary and selected_dietary != "All" and selected_dietary != "Both" and selected_dietary != "Both (Veg & Non-Veg)":
            if r["dietary"].lower() != selected_dietary.lower():
                continue

        # Filter by Cooking Time
        if selected_time and selected_time != "All":
            total_time = r["cook_time"]
            if selected_time == "quick" and total_time > 15:
                continue
            elif selected_time == "medium" and (total_time <= 15 or total_time > 30):
                continue
            elif selected_time == "long" and total_time <= 30:
                continue

        filtered_recipes.append(r)

    return render_template(
        "recipes.html",
        recipes=filtered_recipes,
        total_count=len(filtered_recipes),
        fav_ids=fav_ids,
        search_query=search_query,
        selected_cuisine=selected_cuisine,
        selected_dietary=selected_dietary,
        selected_time=selected_time
    )


# ------------------------------------------------------------------------------
# 3. Single Recipe Details Page
# ------------------------------------------------------------------------------
@app.route("/recipe/<int:recipe_id>")
def recipe_details(recipe_id):
    """
    Displays full detailed recipe information:
    - Large food photo
    - Preparation & cooking time, servings, difficulty
    - Ingredients checklist
    - Step-by-step instructions
    - Related recipes from the same cuisine
    """
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        flash("Recipe not found!", "error")
        return redirect(url_for("recipes"))

    fav_ids = get_favourite_ids()
    is_favourite = recipe_id in fav_ids

    # Format ingredients and instructions into clean lists
    ingredients_list = [ing.strip() for ing in recipe["ingredients"].split("\n") if ing.strip()]
    instructions_list = [step.strip() for step in recipe["instructions"].split("\n") if step.strip()]

    # Fetch 3 related recipes from the same cuisine
    all_recipes_list = get_all_recipes()
    related = [r for r in all_recipes_list if r["cuisine"] == recipe["cuisine"] and r["id"] != recipe_id][:3]

    # User's preferred number of people eating
    user_servings = session.get("people_count")
    if not user_servings:
        latest_prof = get_latest_user_profile()
        user_servings = latest_prof.get("people_count") if latest_prof else None
    if not user_servings:
        user_servings = recipe["servings"]

    return render_template(
        "recipe_details.html",
        recipe=recipe,
        ingredients_list=ingredients_list,
        instructions_list=instructions_list,
        is_favourite=is_favourite,
        related=related,
        fav_ids=fav_ids,
        user_servings=user_servings
    )


# ------------------------------------------------------------------------------
# 4. User Preferences Form Route (Collects 5 User Details + People Count)
# ------------------------------------------------------------------------------
@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    """
    Collects user details for personalized suggestions:
    1. Full Name
    2. Age
    3. Food Preference (Both (Veg & Non-Veg) / Vegetarian / Non-Vegetarian / Vegan)
    4. Quantity (People Eating)
    5. Favourite Cuisine (Mexican / Italian / Indian / Chinese / American)
    6. Allergies or Ingredients to Avoid
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        preference = request.form.get("preference", "Both (Veg & Non-Veg)").strip()
        people_count_str = request.form.get("people_count", "2").strip()
        favourite_cuisine = request.form.get("favourite_cuisine", "Italian").strip()
        allergies = request.form.get("allergies", "").strip()

        # Simple validation
        if not name:
            flash("Please enter your name!", "warning")
            return redirect(url_for("preferences"))

        try:
            age = int(age_str) if age_str else 20
        except ValueError:
            age = 20

        try:
            people_count = int(people_count_str)
            if people_count < 1:
                people_count = 1
        except ValueError:
            people_count = 2

        # Save to SQLite database
        user_id = save_user_profile(name, age, preference, favourite_cuisine, allergies, people_count)
        session["user_id"] = user_id
        session["people_count"] = people_count

        flash(f"Welcome, {name}! Your craving profile is saved for {people_count} {'person' if people_count == 1 else 'people'} 💖", "success")
        return redirect(url_for("suggestions"))

    # If user already submitted preferences, prefill form
    user_profile = None
    if "user_id" in session:
        user_profile = get_user_profile_by_id(session["user_id"])
    if not user_profile:
        user_profile = get_latest_user_profile()

    return render_template("preferences.html", user_profile=user_profile)


# ------------------------------------------------------------------------------
# 5. Personalised Recipe Suggestions Route
# ------------------------------------------------------------------------------
@app.route("/suggestions")
def suggestions():
    """
    Renders personalized recommendations based on the user's saved preferences:
    - Matches their dietary preference
    - Prioritizes their favourite cuisine
    - Excludes recipes containing their allergies or avoided ingredients
    """
    user_profile = None
    if "user_id" in session:
        user_profile = get_user_profile_by_id(session["user_id"])
    if not user_profile:
        user_profile = get_latest_user_profile()

    # If no profile exists yet, guide the user to fill out preferences first
    if not user_profile:
        flash("Please tell us your preferences first to get personalized recipes!", "info")
        return redirect(url_for("preferences"))

    fav_ids = get_favourite_ids()
    primary_picks, other_picks = get_personalised_recommendations(user_profile)

    return render_template(
        "suggestions.html",
        user_profile=user_profile,
        primary_picks=primary_picks,
        other_picks=other_picks,
        fav_ids=fav_ids
    )


# ------------------------------------------------------------------------------
# 6. Favourites Route
# ------------------------------------------------------------------------------
@app.route("/favourites")
def favourites():
    """Displays all recipes marked as favourites by the user."""
    fav_recipes = get_favourite_recipes()
    fav_ids = get_favourite_ids()
    return render_template("favourites.html", recipes=fav_recipes, fav_ids=fav_ids)


# ------------------------------------------------------------------------------
# 7. Toggle Favourite API (AJAX endpoint)
# ------------------------------------------------------------------------------
@app.route("/api/favourite/toggle", methods=["POST"])
def api_toggle_favourite():
    """Allows asynchronous toggling of recipes without page refresh."""
    data = request.get_json(silent=True) or {}
    recipe_id = data.get("recipe_id")

    if not recipe_id:
        # Fallback to form data
        recipe_id = request.form.get("recipe_id")

    try:
        recipe_id = int(recipe_id)
        is_fav, total_favs = toggle_favourite(recipe_id)
        return jsonify({
            "status": "success",
            "recipe_id": recipe_id,
            "is_favourite": is_fav,
            "total_favourites": total_favs
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ------------------------------------------------------------------------------
# 8. Contact Form Submission
# ------------------------------------------------------------------------------
@app.route("/contact", methods=["POST"])
def contact():
    """Saves user inquiry from the contact form."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if name and email and message:
        save_contact_message(name, email, message)
        flash("Thank you for reaching out to Nano's Craving Co.! We will reply soon 💌", "success")
    else:
        flash("Please fill out all contact fields.", "warning")

    return redirect(url_for("index") + "#contact")


# ------------------------------------------------------------------------------
# Main Application Runner
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Runs locally on http://127.0.0.1:5000 with debug enabled
    app.run(debug=True, host="127.0.0.1", port=5000)
