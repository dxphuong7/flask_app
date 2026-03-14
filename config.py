# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    ENV = "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
    API_KEY = os.getenv("API_KEY")
    PORT = int(os.getenv("PORT", 5000))

class ProductionConfig:
    DEBUG = False
    ENV = "production"
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_KEY = os.getenv("API_KEY")
    PORT = int(os.getenv("PORT", 5000))

class TestingConfig:
    DEBUG = True
    TESTING = True
    ENV = "testing"
    DATABASE_URL = "sqlite:///test.db"
    PORT = 5000

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)