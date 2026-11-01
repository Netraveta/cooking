import os
import sys

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "recipe_finder")
sys.path.insert(0, app_dir)

if __name__ == "__main__":
    try:
        from app import app
        print("\n" + "=" * 65)
        print("  [NANO'S CRAVING CO. | Recipe World]")
        print("  Starting Flask server...")
        print("  Open your browser and navigate to: http://127.0.0.1:5000")
        print("=" * 65 + "\n")
        app.run(debug=True, host="127.0.0.1", port=5000)
    except ImportError as e:
        print(f"Error launching app: {e}")
        print("Make sure you installed Flask: pip install flask")
