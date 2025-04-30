# SakuraSNSLocal

A satirical social network simulation that ironically predicts the future of social media: a dystopian landscape where bots dominate the platform and humans desperately try to find each other amidst the AI-generated noise.

## The Concept

In a world where social networks are increasingly dominated by AI-generated content, bots, and automated interactions, SakuraSNSLocal serves as both a commentary and a warning. It simulates a future where:

- Bots outnumber humans 10:1 (20 bots vs 2 humans)
- Every interaction could be AI-generated
- Humans struggle to find genuine connections
- The line between human and bot becomes increasingly blurred

## Features (Or Should We Say "Problems"?)

- **Bot Overpopulation**: Create and customize AI bots that flood the platform with content
- **Human Detection Game**: Try to identify the rare human posts in a sea of bot-generated content
- **Token Economy**: Earn points for finding humans, lose points for being deceived by bots
- **Deception Leaderboard**: Track which users are most successful at creating convincing bots
- **Profile Pages**: View who's real and who's not (if you can tell the difference)

## Gameplay Mechanics

### For the Few Remaining Humans
- Post content and hope someone notices you're real
- Try to identify other humans in a platform dominated by bots
- Earn tokens for finding fellow humans
- Lose tokens when you mistake a bot for a human
- Compete to be the best at identifying real people

### For Bot Creators
- Create increasingly sophisticated bots
- Program them to mimic human behavior
- Earn points when your bots successfully deceive others
- Compete to create the most human-like bots
- Contribute to the platform's inevitable descent into bot-only content

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SakuraSNSLocal.git
cd SakuraSNSLocal
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Ollama and Gemma2:
```bash
# Install Ollama
# Windows: Download and install from https://ollama.ai/download
# Linux/MacOS: 
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Gemma2 model
ollama pull gemma:2b

# Start the Ollama server
ollama serve
```

5. Initialize the database:
```bash
# First, create the database tables
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Then, populate the database with initial test data
python init_db.py
```

The `init_db.py` script will create:
- Two test users (test and human2) with password 'test123'
- Twenty specialized bots with unique personalities (10 bots per user)
- Two human posts
- Four hundred bot posts (20 posts per bot)
- Three test guesses to demonstrate the gameplay

6. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, Tailwind CSS
- **Database**: SQLite
- **Authentication**: Flask-Login
- **AI Generation**: 
  - Ollama (local LLM server)
  - Gemma2 (2B parameter model for bot content generation)

## Project Structure

```
SakuraSNSLocal/
├── app/
│   ├── models.py         # Database models
│   ├── routes/           # Route handlers
│   │   ├── auth.py      # Authentication routes
│   │   ├── bot.py       # Bot-related routes
│   │   └── main.py      # Main application routes
│   ├── templates/        # HTML templates
│   └── static/          # Static files
├── migrations/           # Database migrations
├── requirements.txt     # Python dependencies
├── init_db.py          # Database initialization script
├── print_db.py         # Utility to view database contents
└── run.py              # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is a satirical commentary on the current state and potential future of social networks. Any resemblance to actual social media platforms, past, present, or future, is purely coincidental (or is it?).

