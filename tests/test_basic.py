import unittest
from app import create_app, db
from app.models import User, Bot, Post, Guess
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Use in-memory database for testing

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test', email='test@example.com')
        u.set_password('test123')
        self.assertFalse(u.check_password('wrong'))
        self.assertTrue(u.check_password('test123'))

    def test_bot_creation(self):
        u = User(username='test', email='test@example.com')
        db.session.add(u)
        db.session.commit()

        b = Bot(name='TestBot',
               personality='A test bot personality',
               owner=u)
        db.session.add(b)
        db.session.commit()

        self.assertEqual(u.bots.first(), b)
        self.assertEqual(b.owner, u)

    def test_post_creation(self):
        # Create user and bot
        u = User(username='test', email='test@example.com')
        b = Bot(name='TestBot', personality='Test personality', owner=u)
        db.session.add_all([u, b])
        db.session.commit()

        # Create posts
        user_post = Post(content='User post', author=u)
        bot_post = Post(content='Bot post', bot=b)
        db.session.add_all([user_post, bot_post])
        db.session.commit()

        # Check relationships
        self.assertEqual(user_post.author, u)
        self.assertEqual(bot_post.bot, b)
        self.assertIn(user_post, u.posts.all())
        self.assertIn(bot_post, b.posts.all())

    def test_guess_system(self):
        # Create users and bot
        u1 = User(username='user1', email='user1@example.com')
        u2 = User(username='user2', email='user2@example.com')
        b = Bot(name='TestBot', personality='Test personality', owner=u1)
        db.session.add_all([u1, u2, b])
        db.session.commit()

        # Create guesses
        correct_guess = Guess(guesser_id=u2.id,
                            target_user_id=u1.id,
                            guess_type='human',
                            is_correct=True)
        incorrect_guess = Guess(guesser_id=u2.id,
                              target_bot_id=b.id,
                              guess_type='human',
                              is_correct=False)
        db.session.add_all([correct_guess, incorrect_guess])
        db.session.commit()

        # Verify guesses
        self.assertTrue(correct_guess.is_correct)
        self.assertFalse(incorrect_guess.is_correct)

if __name__ == '__main__':
    unittest.main(verbosity=2) 