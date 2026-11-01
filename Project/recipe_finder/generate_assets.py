# Script to generate 50 beautiful, girly-aesthetic SVG food illustrations for NANO'S CRAVING CO.
import os

recipes_meta = [
    # Mexican
    (1, "Tacos", "Mexican", "#FFF0F3", "#FFCCD5", "🌮", "#E63946"),
    (2, "Chicken Quesadilla", "Mexican", "#FFF3E6", "#FFE5D9", "🧀", "#FB8500"),
    (3, "Enchiladas", "Mexican", "#FFF0F3", "#FFCCD5", "🌯", "#E63946"),
    (4, "Guacamole", "Mexican", "#E8F5E9", "#D8F3DC", "🥑", "#2D6A4F"),
    (5, "Mexican Burrito", "Mexican", "#FFF3E6", "#FFE5D9", "🌯", "#FB8500"),
    (6, "Nachos", "Mexican", "#FFF9E6", "#FDE2E4", "🧀", "#E76F51"),
    (7, "Chilaquiles", "Mexican", "#FFF3E6", "#FFE5D9", "🍳", "#F4A261"),
    (8, "Mexican Rice", "Mexican", "#FFF0F3", "#FFE5D9", "🍚", "#E63946"),
    (9, "Fajitas", "Mexican", "#FFF3E6", "#FFD7BA", "🫑", "#FB8500"),
    (10, "Elote (Mexican Street Corn)", "Mexican", "#FFF9E6", "#FDE2E4", "🌽", "#F4A261"),

    # Italian
    (11, "Margherita Pizza", "Italian", "#FFF0F3", "#FFE5D9", "🍕", "#E63946"),
    (12, "Spaghetti Carbonara", "Italian", "#FFF9E6", "#FFF3CD", "🍝", "#E76F51"),
    (13, "Lasagna", "Italian", "#FFF0F3", "#FFE5D9", "🥘", "#E63946"),
    (14, "Alfredo Pasta", "Italian", "#FFF9E6", "#FFF3CD", "🍝", "#B5838D"),
    (15, "Bruschetta", "Italian", "#E8F5E9", "#D8F3DC", "🥖", "#2D6A4F"),
    (16, "Risotto", "Italian", "#FFF9E6", "#FFF3CD", "🍲", "#B5838D"),
    (17, "Pesto Pasta", "Italian", "#E8F5E9", "#D8F3DC", "🍝", "#40916C"),
    (18, "Ravioli", "Italian", "#FFF9E6", "#FFE5D9", "🥟", "#E76F51"),
    (19, "Garlic Bread", "Italian", "#FFF9E6", "#FFF3CD", "🥖", "#DDA15E"),
    (20, "Tiramisu", "Italian", "#FDF0ED", "#EBD4CB", "☕", "#6B4226"),

    # Indian
    (21, "Shwarma", "Indian", "#FFF3E6", "#FFE5D9", "🌯", "#E76F51"),
    (22, "Chicken Biryani", "Indian", "#FFF9E6", "#FFD7BA", "🍛", "#E76F51"),
    (23, "Masala Dosa", "Indian", "#FFF9E6", "#FFE5D9", "🥞", "#DDA15E"),
    (24, "Vada Pav", "Indian", "#FFF3E6", "#FFE5D9", "🍔", "#FB8500"),
    (25, "Pav Bhaji", "Indian", "#FFF0F3", "#FFE5D9", "🍲", "#E63946"),
    (26, "Butter Chicken", "Indian", "#FFF0F3", "#FFCCD5", "🍗", "#E63946"),
    (27, "Missal Pav", "Indian", "#FFF0F3", "#FFE5D9", "🍲", "#E63946"),
    (28, "Paneer Matar", "Indian", "#E8F5E9", "#D8F3DC", "🍲", "#2D6A4F"),
    (29, "Aloo Paratha", "Indian", "#FFF9E6", "#FFF3CD", "🫓", "#DDA15E"),
    (30, "Samosa", "Indian", "#FFF9E6", "#FFE5D9", "🥟", "#E76F51"),

    # Chinese
    (31, "Veg Fried Rice", "Chinese", "#FFF9E6", "#FFF3CD", "🍚", "#E76F51"),
    (32, "Hakka Noodles", "Chinese", "#FFF3E6", "#FFE5D9", "🍜", "#FB8500"),
    (33, "Spring Rolls", "Chinese", "#FFF9E6", "#FFE5D9", "🥢", "#DDA15E"),
    (34, "Manchurian", "Chinese", "#FFF0F3", "#FFE5D9", "🍲", "#E63946"),
    (35, "Kung Pao Chicken", "Chinese", "#FFF0F3", "#FFD7BA", "🍗", "#E63946"),
    (36, "Dumplings", "Chinese", "#FFF9E6", "#FFE5D9", "🥟", "#E76F51"),
    (37, "Hot and Sour Soup", "Chinese", "#FFF0F3", "#FFE5D9", "🥣", "#E63946"),
    (38, "Chilli Paneer", "Chinese", "#FFF0F3", "#FFE5D9", "🌶️", "#E63946"),
    (39, "Chow Mein", "Chinese", "#FFF3E6", "#FFE5D9", "🍜", "#FB8500"),
    (40, "Sweet and Sour Chicken", "Chinese", "#FFF3E6", "#FFE5D9", "🍗", "#FB8500"),

    # American
    (41, "Classic Burger", "American", "#FFF3E6", "#FFE5D9", "🍔", "#FB8500"),
    (42, "Pancakes", "American", "#FFF9E6", "#FFE5D9", "🥞", "#DDA15E"),
    (43, "Mac and Cheese", "American", "#FFF9E6", "#FFF3CD", "🧀", "#FB8500"),
    (44, "Club Sandwich", "American", "#FFF9E6", "#FFE5D9", "🥪", "#DDA15E"),
    (45, "Hot Dog", "American", "#FFF0F3", "#FFE5D9", "🌭", "#E63946"),
    (46, "Cheesecake", "American", "#FFF0F3", "#FFCCD5", "🍰", "#FF758F"),
    (47, "Chocolate Brownies", "American", "#FDF0ED", "#EBD4CB", "🍫", "#6B4226"),
    (48, "French Fries", "American", "#FFF9E6", "#FFF3CD", "🍟", "#FB8500"),
    (49, "BBQ Chicken", "American", "#FFF0F3", "#FFE5D9", "🍗", "#E63946"),
    (50, "Apple Pie", "American", "#FFF9E6", "#FFE5D9", "🥧", "#DDA15E")
]

out_dir = os.path.join("recipe_finder", "static", "images")
os.makedirs(out_dir, exist_ok=True)

for rid, name, cuisine, c1, c2, emoji, accent in recipes_meta:
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
  <defs>
    <linearGradient id="bgGrad{rid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}" />
      <stop offset="100%" stop-color="{c2}" />
    </linearGradient>
    <filter id="shadow{rid}" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="{accent}" flood-opacity="0.18" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="500" fill="url(#bgGrad{rid})" rx="24"/>
  
  <!-- Decorative Circles & Sparkles -->
  <circle cx="120" cy="90" r="60" fill="#FFFFFF" fill-opacity="0.4" />
  <circle cx="700" cy="400" r="90" fill="#FFFFFF" fill-opacity="0.35" />
  <circle cx="680" cy="110" r="30" fill="{accent}" fill-opacity="0.15" />
  <circle cx="100" cy="420" r="45" fill="{accent}" fill-opacity="0.12" />

  <!-- Girly Sparkles & Stars -->
  <g fill="{accent}" opacity="0.6">
    <path d="M 620 70 Q 620 85 605 85 Q 620 85 620 100 Q 620 85 635 85 Q 620 85 620 70 Z" />
    <path d="M 180 370 Q 180 380 170 380 Q 180 380 180 390 Q 180 380 190 380 Q 180 380 180 370 Z" />
    <path d="M 730 250 Q 730 260 720 260 Q 730 260 730 270 Q 730 260 740 260 Q 730 260 730 250 Z" />
  </g>

  <!-- Central Dish Card Platform -->
  <g filter="url(#shadow{rid})">
    <circle cx="400" cy="220" r="140" fill="#FFFFFF" />
    <circle cx="400" cy="220" r="128" fill="{c1}" fill-opacity="0.6" stroke="{accent}" stroke-width="2.5" stroke-dasharray="6,6"/>
  </g>

  <!-- Giant Emoji / Food Illustration -->
  <text x="400" y="270" font-size="110" text-anchor="middle" font-family="'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif">{emoji}</text>

  <!-- Cuisine Tag Badge -->
  <g transform="translate(400, 65)">
    <rect x="-85" y="-18" width="170" height="36" rx="18" fill="{accent}" />
    <text x="0" y="5" font-family="'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">{cuisine.upper()} SPECIAL</text>
  </g>

  <!-- Recipe Title Ribbon -->
  <g transform="translate(400, 420)">
    <rect x="-260" y="-36" width="520" height="62" rx="20" fill="#FFFFFF" fill-opacity="0.95" />
    <text x="0" y="4" font-family="'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif" font-size="24" font-weight="800" fill="#2B2D42" text-anchor="middle">{name}</text>
    <text x="0" y="21" font-family="'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="{accent}" text-anchor="middle" letter-spacing="1">NANO'S CRAVING CO. ✨</text>
  </g>
</svg>'''
    
    file_path = os.path.join(out_dir, f"recipe_{rid}.svg")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

print(f"Generated {len(recipes_meta)} SVG recipe visuals in {out_dir}")
