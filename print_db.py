from app import create_app, db
from app.models import User, Bot, Post, Guess

app = create_app()

def print_database():
    with app.app_context():
        print("\n=== Users ===")
        for user in User.query.all():
            print(f"User: {user.username} (ID: {user.id})")
            print(f"  Tokens: {user.tokens}")
            print(f"  Is Verified Human: {user.is_verified_human}")
            print(f"  Created At: {user.created_at}")
            print()

        print("\n=== Bots ===")
        for bot in Bot.query.all():
            print(f"Bot: {bot.name} (ID: {bot.id})")
            print(f"  Owner: {bot.owner.username}")
            print(f"  Personality: {bot.personality}")
            print(f"  Successful Deceptions: {bot.successful_deceptions}")
            print(f"  Created At: {bot.created_at}")
            print()

        print("\n=== Posts ===")
        for post in Post.query.all():
            author = post.author.username if post.author else post.bot.name
            print(f"Post ID: {post.id}")
            print(f"  Content: {post.content}")
            print(f"  Author: {author}")
            print(f"  Timestamp: {post.timestamp}")
            print(f"  Likes: {post.likes}")
            print()

        print("\n=== Guesses ===")
        for guess in Guess.query.all():
            guesser = User.query.get(guess.guesser_id)
            target_user = User.query.get(guess.target_user_id) if guess.target_user_id else None
            target_bot = Bot.query.get(guess.target_bot_id) if guess.target_bot_id else None
            target = target_user.username if target_user else target_bot.name if target_bot else "Unknown"
            
            print(f"Guess ID: {guess.id}")
            print(f"  Guesser: {guesser.username}")
            print(f"  Target: {target}")
            print(f"  Guess Type: {guess.guess_type}")
            print(f"  Is Correct: {guess.is_correct}")
            print(f"  Timestamp: {guess.timestamp}")
            print()

if __name__ == '__main__':
    print_database() 