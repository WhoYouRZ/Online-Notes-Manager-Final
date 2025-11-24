from app_modules import create_app
from config import config

def start_app():
    return create_app(test_config=config["development"].__dict__)


if __name__ == "__main__":
    app = start_app()
    app.run(host="0.0.0.0", port=5000)
