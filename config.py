import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Token economy settings
    TOKENS_FOR_CORRECT_HUMAN = 10
    TOKENS_FOR_SUCCESSFUL_DECEPTION = 5
    
    # Bot settings
    MAX_BOTS_PER_USER = 3
    MIN_POST_INTERVAL = 300  # 5 minutes between bot posts
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60 