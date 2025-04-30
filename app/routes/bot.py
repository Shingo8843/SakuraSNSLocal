from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Bot, Post, User, Guess
from openai import OpenAI
from datetime import datetime, timedelta

bp = Blueprint('bot', __name__)

@bp.route('/create_bot', methods=['GET', 'POST'])
@login_required
def create_bot():
    if current_user.bots.count() >= current_app.config['MAX_BOTS_PER_USER']:
        flash('You have reached the maximum number of bots allowed')
        return redirect(url_for('main.profile', username=current_user.username))
    
    if request.method == 'POST':
        name = request.form['name']
        personality = request.form['personality']
        
        if Bot.query.filter_by(name=name).first():
            flash('Bot name already taken')
            return redirect(url_for('bot.create_bot'))
        
        bot = Bot(name=name, personality=personality, owner=current_user)
        db.session.add(bot)
        db.session.commit()
        
        flash(f'Your bot {name} has been created!')
        return redirect(url_for('main.profile', username=current_user.username))
    
    return render_template('bot/create.html')

@bp.route('/bot/<int:id>/post', methods=['POST'])
@login_required
def bot_post(id):
    bot = Bot.query.get_or_404(id)
    if bot.owner != current_user:
        flash('You can only post with your own bots')
        return redirect(url_for('main.index'))
    
    # Check if enough time has passed since last post
    if bot.last_post_time and \
       datetime.utcnow() - bot.last_post_time < timedelta(seconds=current_app.config['MIN_POST_INTERVAL']):
        flash('Please wait before making another bot post')
        return redirect(url_for('main.index'))
    
    # Generate post content using Ollama
    try:
        client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',  # required, but unused
        )
        response = client.chat.completions.create(
            model="gemma2:2b",
            messages=[
                {"role": "system", "content": f"You are a social media bot with the following personality: {bot.personality}"},
                {"role": "user", "content": "Create a social media post that reflects your personality."}
            ]
        )
        content = response.choices[0].message.content
        
        post = Post(content=content, bot=bot)
        bot.last_post_time = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        
        flash('Your bot has posted successfully!')
    except Exception as e:
        flash(f'Error generating bot post: {str(e)}')
        
    return redirect(url_for('main.index'))

@bp.route('/guess/<string:entity_id>', methods=['POST'])
@login_required
def make_guess(entity_id):
    # First try to find the post by entity_id
    post = Post.query.filter_by(entity_id=entity_id).first()
    
    if not post:
        flash('Invalid post')
        return redirect(url_for('main.index'))
    
    # Determine if guess is correct (if it's a human post)
    is_correct = post.user_id is not None  # True if post is from a user
    
    # Debug prints
    print("\n=== Post Details ===")
    print(f"Post ID: {post.id}")
    print(f"Entity ID: {post.entity_id}")
    print(f"Content: {post.content}")
    print(f"User ID: {post.user_id}")
    print(f"Bot ID: {post.bot_id}")
    print(f"Is Correct: {is_correct}")
    
    if post.bot:
        print("\n=== Bot Details ===")
        print(f"Bot Name: {post.bot.name}")
        print(f"Bot ID: {post.bot.id}")
        print(f"Bot Entity ID: {post.bot.entity_id}")
        print(f"Bot Owner: {post.bot.owner.username}")
        print(f"Bot Personality: {post.bot.personality}")
        print(f"Successful Deceptions: {post.bot.successful_deceptions}")
    
    # Create the guess with only one target ID
    guess_data = {
        'guesser_id': current_user.id,
        'guess_type': 'human',
        'is_correct': is_correct,
        'timestamp': datetime.utcnow()
    }
    
    # Set only one target ID
    if post.user_id:
        guess_data['target_user_id'] = post.user_id
    else:
        guess_data['target_bot_id'] = post.bot_id
    
    guess = Guess(**guess_data)
    
    try:
        db.session.add(guess)
        
        # Update tokens based on guess
        if is_correct:
            # Correctly identified a human post
            current_user.tokens += current_app.config['TOKENS_FOR_CORRECT_HUMAN']
            flash(f'Correct! You earned {current_app.config["TOKENS_FOR_CORRECT_HUMAN"]} tokens')
        else:
            # Incorrectly guessed a bot post as human
            if post.bot:  # Check if bot exists
                post.bot.successful_deceptions += 1
                post.bot.owner.tokens += current_app.config['TOKENS_FOR_SUCCESSFUL_DECEPTION']
                flash('Incorrect! The bot successfully deceived you')
            else:
                flash('Error: Bot not found')
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error making guess: {str(e)}')
    
    return redirect(url_for('main.index')) 