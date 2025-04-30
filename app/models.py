from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import uuid

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_verified_human = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    bots = db.relationship('Bot', backref='owner', lazy='dynamic')
    guesses_made = db.relationship('Guess', foreign_keys='Guess.guesser_id', backref='guesser', lazy='dynamic')
    guesses_received = db.relationship('Guess', foreign_keys='Guess.target_user_id', backref='target_user', lazy='dynamic')
    entity_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    __table_args__ = (
        db.UniqueConstraint('entity_id', name='uq_user_entity_id'),
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    personality = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    successful_deceptions = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_post_time = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='bot', lazy='dynamic')
    guesses_received = db.relationship('Guess', foreign_keys='Guess.target_bot_id', backref='target_bot', lazy='dynamic')
    entity_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    __table_args__ = (
        db.UniqueConstraint('entity_id', name='uq_bot_entity_id'),
    )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))
    likes = db.Column(db.Integer, default=0)
    entity_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # Either user_id or bot_id should be set, not both
    __table_args__ = (
        db.CheckConstraint('NOT(user_id IS NULL AND bot_id IS NULL)', name='ck_post_author_not_null'),
        db.CheckConstraint('NOT(user_id IS NOT NULL AND bot_id IS NOT NULL)', name='ck_post_single_author'),
        db.UniqueConstraint('entity_id', name='uq_post_entity_id'),
    )

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guesser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))
    guess_type = db.Column(db.String(10), nullable=False)  # 'human' or 'bot'
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    entity_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    __table_args__ = (
        db.CheckConstraint('NOT(target_user_id IS NULL AND target_bot_id IS NULL)', name='ck_guess_target_not_null'),
        db.CheckConstraint('NOT(target_user_id IS NOT NULL AND target_bot_id IS NOT NULL)', name='ck_guess_single_target'),
        db.UniqueConstraint('entity_id', name='uq_guess_entity_id'),
    )

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 