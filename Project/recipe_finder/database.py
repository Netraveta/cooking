# ==============================================================================
# NANO'S CRAVING CO. - Database Management Module
# Handles SQLite database connection, table initialization, and SQL queries.
# ==============================================================================

import sqlite3
import os

try:
    from recipe_finder.recipes_data import ALL_RECIPES
except ImportError:
    from recipes_data import ALL_RECIPES

DB_PATH = os.path.join(os.path.dirname(__file__), "recipes.db")


def get_db():
    """
    Establishes a connection to the SQLite database.
    row_factory = sqlite3.Row allows column access by name (like a dictionary).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database schema and seeds the 50 recipes if not already loaded.
    """
    conn = get_db()
    cursor = conn.cursor()

    # 1. Create Recipes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            dietary TEXT NOT NULL,
            prep_time INTEGER NOT NULL,
            cook_time INTEGER NOT NULL,
            servings INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            description TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            image_url TEXT NOT NULL,
            local_image TEXT NOT NULL
        )
    """)

    # 2. Create User Profiles Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            preference TEXT NOT NULL,
            favourite_cuisine TEXT NOT NULL,
            allergies TEXT,
            people_count INTEGER DEFAULT 2,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check and add people_count column if updating existing database
    cursor.execute("PRAGMA table_info(user_profiles)")
    columns = [col[1] for col in cursor.fetchall()]
    if "people_count" not in columns:
        cursor.execute("ALTER TABLE user_profiles ADD COLUMN people_count INTEGER DEFAULT 2")

    # 3. Create Favourites Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    # 4. Create Contact Messages Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Seed recipes if empty
    cursor.execute("SELECT COUNT(*) as count FROM recipes")
    count = cursor.fetchone()["count"]

    if count < len(ALL_RECIPES):
        print(f"Seeding {len(ALL_RECIPES)} recipes into SQLite database...")
        for r in ALL_RECIPES:
            cursor.execute("""
                INSERT OR REPLACE INTO recipes 
                (id, name, cuisine, dietary, prep_time, cook_time, servings, difficulty, description, ingredients, instructions, image_url, local_image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r["id"], r["name"], r["cuisine"], r["dietary"],
                r["prep_time"], r["cook_time"], r["servings"], r["difficulty"],
                r["description"], r["ingredients"], r["instructions"],
                r["image_url"], r["local_image"]
            ))
        conn.commit()
        print("Successfully seeded all 50 recipes!")

    conn.close()


def get_all_recipes():
    """Retrieve all 50 recipes ordered by cuisine and id."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY id ASC")
    recipes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return recipes


def get_recipe_by_id(recipe_id):
    """Retrieve a single recipe by its primary key ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_popular_recipes(limit=6):
    """Retrieve a handpicked set of popular recipes across cuisines for the home page."""
    conn = get_db()
    cursor = conn.cursor()
    # Pick classic showstoppers: Tacos (1), Margherita Pizza (11), Chicken Biryani (22), Hakka Noodles (32), Classic Burger (41), Pancakes (42)
    cursor.execute("SELECT * FROM recipes WHERE id IN (1, 11, 22, 32, 41, 42) LIMIT ?", (limit,))
    recipes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return recipes


def save_user_profile(name, age, preference, favourite_cuisine, allergies, people_count=2):
    """Save user preferences details into the database including party size (people count)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_profiles (name, age, preference, favourite_cuisine, allergies, people_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, preference, favourite_cuisine, allergies, people_count))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_latest_user_profile():
    """Fetch the most recently submitted user profile."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_profile_by_id(user_id):
    """Fetch user profile by its ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_favourite_ids():
    """Return a set of recipe IDs that have been favorited."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_id FROM favourites")
    fav_ids = {row["recipe_id"] for row in cursor.fetchall()}
    conn.close()
    return fav_ids


def toggle_favourite(recipe_id):
    """Toggle a recipe in/out of favourites."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM favourites WHERE recipe_id = ?", (recipe_id,))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM favourites WHERE recipe_id = ?", (recipe_id,))
        is_fav = False
    else:
        cursor.execute("INSERT INTO favourites (recipe_id) VALUES (?)", (recipe_id,))
        is_fav = True

    conn.commit()
    cursor.execute("SELECT COUNT(*) as count FROM favourites")
    total_favs = cursor.fetchone()["count"]
    conn.close()
    return is_fav, total_favs


def get_favourite_recipes():
    """Retrieve all full recipe objects that are marked as favorites."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.* FROM recipes r
        JOIN favourites f ON r.id = f.recipe_id
        ORDER BY f.created_at DESC
    """)
    recipes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return recipes


def save_contact_message(name, email, message):
    """Save user contact inquiry into the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contact_messages (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))
    conn.commit()
    conn.close()


def get_personalised_recommendations(profile):
    """
    Core Personalised Recommendation Algorithm:
    1. Filter by dietary preference (Vegetarian, Vegan, Non-Vegetarian).
    2. Exclude any recipes containing words from the user's allergy / avoid list.
    3. Partition into top picks matching user's favourite cuisine, and other matching picks.
    """
    if not profile:
        return [], []

    all_recipes = get_all_recipes()
    pref = profile.get("preference", "Non-Vegetarian").strip().lower()
    fav_cuisine = profile.get("favourite_cuisine", "Italian").strip().lower()
    allergies_text = profile.get("allergies", "") or ""

    # Parse allergy keywords: split by comma, semicolon, space and clean up
    raw_allergies = [a.strip().lower() for a in allergies_text.replace(";", ",").split(",") if a.strip()]
    # Remove trivial words like "no", "none", "n/a"
    avoid_keywords = [w for w in raw_allergies if w not in ["no", "none", "n/a", "nil", "nothing"]]

    matching_recipes = []

    for r in all_recipes:
        r_diet = r["dietary"].strip().lower()
        r_text = (r["name"] + " " + r["ingredients"] + " " + r["description"]).lower()

        # Check dietary rule:
        if pref in ["both", "both (veg and nonveg)", "both (veg & non-veg)", "both (veg and non-veg)", "all"]:
            # Includes both Vegetarian, Non-Vegetarian, and Vegan dishes
            pass
        elif pref == "vegetarian":
            if r_diet not in ["vegetarian", "vegan"]:
                continue
        elif pref == "vegan":
            if r_diet != "vegan":
                continue
        elif pref == "non-vegetarian":
            if r_diet != "non-vegetarian":
                continue

        # Check allergy exclusions:
        has_allergy = False
        for allergen in avoid_keywords:
            if allergen in r_text:
                has_allergy = True
                break
        if has_allergy:
            continue

        matching_recipes.append(r)

    # Separate into primary picks (favourite cuisine) and secondary picks (other cuisines)
    primary_picks = [r for r in matching_recipes if r["cuisine"].strip().lower() == fav_cuisine]
    other_picks = [r for r in matching_recipes if r["cuisine"].strip().lower() != fav_cuisine]

    return primary_picks, other_picks
