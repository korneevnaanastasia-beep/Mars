import os
from pathlib import Path

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    BASEDIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASEDIR / 'data' / 'portal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
