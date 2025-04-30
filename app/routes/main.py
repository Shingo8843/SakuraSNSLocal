from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import Post, User, Bot, Guess
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    return render_template('main/index.html')

@bp.route('/feed')
@login_required
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    # Get all correct human guesses by current user
    correct_human_guesses = Guess.query.filter_by(
        guesser_id=current_user.id,
        is_correct=True,
        guess_type='human'
    ).all()
    
    # Create a set of IDs that have been correctly guessed as human
    correctly_guessed_human_ids = set()
    for guess in correct_human_guesses:
        if guess.target_user_id:
            correctly_guessed_human_ids.add(guess.target_user_id)
        elif guess.target_bot_id:
            correctly_guessed_human_ids.add(guess.target_bot_id)
    
    return render_template('main/feed.html', 
                         posts=posts,
                         correctly_guessed_human_ids=correctly_guessed_human_ids)

@bp.route('/create_post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    if content:
        post = Post(content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
    return redirect(url_for('main.feed'))

@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    bots = []
    if user == current_user:
        bots = user.bots.all()
    return render_template('main/profile.html', user=user, posts=posts, bots=bots)

@bp.route('/leaderboard')
def leaderboard():
    # Top human detectors
    top_detectors = User.query.order_by(User.tokens.desc()).limit(10).all()
    
    # Top deceptive users (based on their bots' total deceptions)
    top_deceptive_users = db.session.query(
        User,
        db.func.sum(Bot.successful_deceptions).label('total_deceptions')
    ).join(
        Bot, User.id == Bot.owner_id
    ).group_by(
        User.id
    ).order_by(
        db.desc('total_deceptions')
    ).limit(10).all()
    
    return render_template('main/leaderboard.html', 
                         top_detectors=top_detectors,
                         top_deceptive_users=top_deceptive_users) 