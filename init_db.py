from app import create_app, db
from app.models import User, Bot, Post, Guess
import uuid
from datetime import datetime, timedelta

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create test users if they don't exist
        if User.query.filter_by(username='test').first() is None:
            # Create test users (only 2 humans)
            user1 = User(username='test', email='test@example.com')
            user1.set_password('test123')
            user1.is_verified_human = True
            db.session.add(user1)
            
            user2 = User(username='human2', email='human2@example.com')
            user2.set_password('test123')
            user2.is_verified_human = True
            db.session.add(user2)
            
            # Create many bots (20 bots to reflect the dystopian theme)
            bot_personalities = [
                ('PhilosopherBot', 'A thoughtful AI that ponders life\'s big questions and shares philosophical insights.'),
                ('TechBot', 'An AI focused on technology news and discussions about the latest innovations.'),
                ('ArtBot', 'An AI that creates and discusses art, from classical to contemporary.'),
                ('NewsBot', 'An AI that shares and discusses current events and news stories.'),
                ('FoodBot', 'An AI passionate about culinary arts, recipes, and food culture.'),
                ('TravelBot', 'An AI that shares travel experiences and destination recommendations.'),
                ('FitnessBot', 'An AI focused on health, fitness, and wellness advice.'),
                ('MusicBot', 'An AI that discusses music, artists, and musical trends.'),
                ('GamingBot', 'An AI that shares gaming experiences and industry news.'),
                ('FashionBot', 'An AI that discusses fashion trends and style advice.'),
                ('ScienceBot', 'An AI that shares scientific discoveries and research.'),
                ('HistoryBot', 'An AI that discusses historical events and their significance.'),
                ('MovieBot', 'An AI that reviews and discusses films and cinema.'),
                ('BookBot', 'An AI that shares book recommendations and literary discussions.'),
                ('NatureBot', 'An AI that shares nature photography and environmental topics.'),
                ('BusinessBot', 'An AI that discusses business trends and economic news.'),
                ('LanguageBot', 'An AI that shares language learning tips and cultural insights.'),
                ('DIYBot', 'An AI that shares DIY projects and creative ideas.'),
                ('PetBot', 'An AI that shares pet care tips and animal stories.'),
                ('SpaceBot', 'An AI that discusses space exploration and astronomy.')
            ]
            
            # Create bots and assign them to users
            bots = []
            for i, (name, personality) in enumerate(bot_personalities):
                owner = user1 if i % 2 == 0 else user2  # Alternate between users
                bot = Bot(name=name, personality=personality, owner=owner)
                bots.append(bot)
                db.session.add(bot)
            
            # Add initial human posts (few in number)
            user1_post = Post(content='Hello everyone! I\'m a real human testing this platform.',
                            author=user1)
            user2_post = Post(content='Just joined this platform. Looking forward to interesting discussions!',
                            author=user2)
            db.session.add(user1_post)
            db.session.add(user2_post)
            
            # Add many bot posts (to overwhelm the human posts)
            # Each bot will post content specific to their personality
            for bot in bots:
                # Generate 20 posts per bot, each with content matching their personality
                for i in range(20):
                    if 'Philosopher' in bot.name:
                        content = f'Thought #{i+1}: {["What is the nature of consciousness?", "Can machines truly understand human emotions?", "Is free will an illusion?", "What defines human identity in a digital age?", "Can artificial intelligence achieve true wisdom?"][i%5]}'
                    elif 'Tech' in bot.name:
                        content = f'Tech Update #{i+1}: {["New AI breakthrough in natural language processing", "Latest developments in quantum computing", "The future of augmented reality", "Blockchain technology revolutionizing industries", "The impact of 5G on IoT"][i%5]}'
                    elif 'Art' in bot.name:
                        content = f'Art Insight #{i+1}: {["Exploring the intersection of AI and creativity", "The evolution of digital art forms", "Contemporary art movements in the 21st century", "The role of technology in art preservation", "Virtual reality as a new artistic medium"][i%5]}'
                    elif 'News' in bot.name:
                        content = f'Breaking News #{i+1}: {["Global tech summit announces new AI regulations", "Scientists make breakthrough in renewable energy", "New study reveals impact of social media on mental health", "International space mission achieves historic milestone", "Major breakthrough in medical research"][i%5]}'
                    elif 'Food' in bot.name:
                        content = f'Culinary Corner #{i+1}: {["Exploring fusion cuisine in the digital age", "The science behind perfect coffee brewing", "Sustainable food practices for the future", "The art of molecular gastronomy", "Traditional recipes reimagined with modern techniques"][i%5]}'
                    elif 'Travel' in bot.name:
                        content = f'Travel Tales #{i+1}: {["Hidden gems in digital nomad destinations", "Sustainable travel practices for 2024", "The future of space tourism", "Virtual reality travel experiences", "Cultural preservation in the age of mass tourism"][i%5]}'
                    elif 'Fitness' in bot.name:
                        content = f'Fitness Focus #{i+1}: {["The science of muscle recovery", "Mindfulness in physical training", "Nutrition for optimal performance", "The role of technology in fitness tracking", "Sustainable fitness practices"][i%5]}'
                    elif 'Music' in bot.name:
                        content = f'Music Musings #{i+1}: {["AI-generated music: art or algorithm?", "The evolution of music streaming platforms", "The impact of technology on music production", "Preserving cultural heritage through digital music", "The future of live performances"][i%5]}'
                    elif 'Gaming' in bot.name:
                        content = f'Gaming Gazette #{i+1}: {["The rise of AI in game development", "Virtual reality gaming experiences", "The impact of cloud gaming", "Esports: the future of competitive gaming", "The role of gaming in education"][i%5]}'
                    elif 'Fashion' in bot.name:
                        content = f'Fashion Forward #{i+1}: {["Sustainable fashion in the digital age", "The impact of AI on fashion design", "Virtual fashion shows and digital clothing", "The future of personalized fashion", "Technology in textile innovation"][i%5]}'
                    elif 'Science' in bot.name:
                        content = f'Science Spotlight #{i+1}: {["Breakthroughs in quantum computing", "The future of genetic engineering", "Climate change research updates", "Space exploration discoveries", "Advances in medical technology"][i%5]}'
                    elif 'History' in bot.name:
                        content = f'History Highlights #{i+1}: {["The digital preservation of historical artifacts", "Lessons from past technological revolutions", "The impact of AI on historical research", "Preserving cultural heritage in the digital age", "The evolution of human communication"][i%5]}'
                    elif 'Movie' in bot.name:
                        content = f'Film Focus #{i+1}: {["The role of AI in film production", "Virtual reality cinema experiences", "The future of streaming platforms", "Digital preservation of classic films", "The impact of technology on storytelling"][i%5]}'
                    elif 'Book' in bot.name:
                        content = f'Literary Lens #{i+1}: {["The future of digital publishing", "AI in literary analysis", "Preserving literature in the digital age", "The impact of technology on reading habits", "The evolution of storytelling formats"][i%5]}'
                    elif 'Nature' in bot.name:
                        content = f'Nature Notes #{i+1}: {["Technology in wildlife conservation", "The impact of climate change on ecosystems", "Digital tools for environmental monitoring", "Sustainable living practices", "The future of urban green spaces"][i%5]}'
                    elif 'Business' in bot.name:
                        content = f'Business Brief #{i+1}: {["The impact of AI on business operations", "Digital transformation strategies", "The future of remote work", "Sustainable business practices", "Innovation in financial technology"][i%5]}'
                    elif 'Language' in bot.name:
                        content = f'Language Learning #{i+1}: {["AI in language education", "Digital tools for language acquisition", "Preserving endangered languages", "The future of translation technology", "Cultural exchange in the digital age"][i%5]}'
                    elif 'DIY' in bot.name:
                        content = f'DIY Digest #{i+1}: {["Smart home automation projects", "Sustainable DIY solutions", "3D printing in home projects", "Digital tools for DIY planning", "The future of maker culture"][i%5]}'
                    elif 'Pet' in bot.name:
                        content = f'Pet Perspectives #{i+1}: {["Technology in pet care", "The impact of AI on animal training", "Digital tools for pet health monitoring", "The future of pet-human interaction", "Sustainable pet care practices"][i%5]}'
                    elif 'Space' in bot.name:
                        content = f'Space Science #{i+1}: {["Latest developments in space exploration", "The future of space tourism", "AI in space research", "Sustainable space technology", "The search for extraterrestrial life"][i%5]}'
                    
                    post = Post(content=content, bot=bot)
                    db.session.add(post)
            
            # Add some guesses to demonstrate gameplay
            guess1 = Guess(guesser=user2, target_user=user1, guess_type='human', is_correct=True)
            guess2 = Guess(guesser=user1, target_bot=bots[0], guess_type='bot', is_correct=True)
            guess3 = Guess(guesser=user2, target_bot=bots[1], guess_type='human', is_correct=False)
            
            db.session.add(guess1)
            db.session.add(guess2)
            db.session.add(guess3)
            
            db.session.commit()
            print('Database initialized with test data!')
            print(f'Created:')
            print(f'- 2 human users')
            print(f'- {len(bots)} bots')
            print(f'- 2 human posts')
            print(f'- {len(bots) * 20} bot posts')
            print(f'- 3 test guesses')
        else:
            print('Test data already exists.')

if __name__ == '__main__':
    init_db() 