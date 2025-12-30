from app_modules import create_app, init_db
from config import config
import sys
import os

def start_app():
    return create_app(test_config=config["development"].__dict__)

app = start_app()

# -----------------------------------------
# COMMAND LINE TOOL
# -----------------------------------------

def cli():
    """
    Command Line Interface
    Usage:
        python app.py run
        python app.py init-db
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python app.py run")
        print("  python app.py init-db")
        return

    command = sys.argv[1].lower()

    if command == "init-db":
        with app.app_context():
            init_db()
        print("Database initialized successfully.")
        return

    if command == "run":
        app.run(host="0.0.0.0", port=5000)
        return

    print(f"Unknown command: {command}")
    print("Available commands: run, init-db")

if __name__ == "__main__":
    cli()
    
