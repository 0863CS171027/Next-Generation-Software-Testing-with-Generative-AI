# Joke Generator Project - Quick Start

## 🎯 Quickest Way to Run

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Run the Application
```bash
python joke_project/main.py
```

## 📦 Complete Installation

### Full Setup (Recommended)
```bash
# Install all dependencies
pip install -r requirements.txt

# Install the project
pip install -e .

# Run the application
joke-generator
```

## 📝 Using as a Module

```python
from joke_project.joke_generator import JokeGenerator

generator = JokeGenerator()
joke = generator.get_random_joke()
print(generator.format_joke(joke))
```

## 🧪 Run Tests

```bash
pip install pytest
pytest joke_project/tests.py -v
```

## 📂 Project Structure

```
joke_project/
├── __init__.py           # Package init
├── joke_generator.py     # Core logic
├── config.py            # Configuration
├── utils.py             # Cache & stats
├── app.py               # CLI app
├── main.py              # Entry point
└── tests.py             # Unit tests

setup.py                 # Package setup
requirements.txt         # Dependencies
```

## 🚀 Features

✨ Multiple joke categories
🔒 Safe mode support
💾 Automatic caching
📊 Statistics tracking
🎮 Interactive menu
📝 Comprehensive logging
🧪 Full test coverage

## 🎭 Interactive Menu Options

1. Get a random joke
2. Get multiple jokes
3. Get joke by category
4. View statistics
5. Clear cache
6. Exit

## 📖 More Information

- Full documentation: `JOKE_PROJECT_README.md`
- Installation guide: `INSTALLATION.md`
- API documentation: `README_JOKES.md`

---

**Start now: `python joke_project/main.py`** 🎉
