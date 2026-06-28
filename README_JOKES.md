# Random Joke Generator

A simple yet powerful Python application that fetches random jokes from the **JokeAPI** external service.

## Features

✨ **Multi-Category Support**
- Programming jokes
- Miscellaneous jokes
- Knock-Knock jokes
- General jokes
- Dark jokes

🔒 **Safe Mode**
- Toggle adult content filtering
- Explicit content warnings

⚡ **Easy to Use**
- Simple API
- Error handling
- Beautiful formatted output

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from joke_generator import JokeGenerator

# Create a generator instance
generator = JokeGenerator()

# Get a random programming joke
joke = generator.get_random_joke(category="Programming")
print(generator.format_joke(joke))
```

### Get Multiple Jokes

```python
# Fetch 5 jokes
jokes = generator.get_multiple_jokes(count=5, category="General")

for joke in jokes:
    print(generator.format_joke(joke))
```

### Different Categories

```python
categories = ["Programming", "Miscellaneous", "General", "Knock-Knock"]

for category in categories:
    joke = generator.get_random_joke(category=category)
    print(generator.format_joke(joke))
```

### Safe Mode Control

```python
# With safe mode (default)
joke = generator.get_random_joke(safe_mode=True)

# Without safe mode
joke = generator.get_random_joke(safe_mode=False)
```

## Running the Demo

Execute the main joke generator:
```bash
python joke_generator.py
```

Run the examples:
```bash
python joke_examples.py
```

## API Reference

### JokeGenerator Class

#### `get_random_joke(category="Programming", safe_mode=True)`
Fetches a single random joke.

**Parameters:**
- `category` (str): Joke category
- `safe_mode` (bool): Filter adult content

**Returns:** Dictionary with joke data or None on error

#### `get_multiple_jokes(count=5, category="Programming", safe_mode=True)`
Fetches multiple random jokes.

**Parameters:**
- `count` (int): Number of jokes to fetch
- `category` (str): Joke category
- `safe_mode` (bool): Filter adult content

**Returns:** List of joke dictionaries

#### `format_joke(joke)`
Formats a joke for display.

**Parameters:**
- `joke` (dict): Joke dictionary from API

**Returns:** Formatted string representation

## Joke Response Format

### Single-Part Joke
```json
{
  "type": "single",
  "joke": "Why do programmers prefer dark mode?",
  "category": "Programming"
}
```

### Two-Part Joke
```json
{
  "type": "twopart",
  "setup": "Why do programmers prefer dark mode?",
  "delivery": "Because light attracts bugs!",
  "category": "Programming"
}
```

## Error Handling

The generator gracefully handles:
- ✅ Network timeouts
- ✅ Connection errors
- ✅ HTTP errors
- ✅ Invalid JSON responses
- ✅ API unavailability

All errors return `None` with a descriptive error message.

## Available Categories

| Category | Description |
|----------|-------------|
| **Programming** | Developer and programming-related jokes |
| **Miscellaneous** | Various random jokes |
| **General** | General humor |
| **Knock-Knock** | Classic knock-knock jokes |
| **Dark** | Dark humor jokes |

## External API

This project uses **JokeAPI** (https://jokeapi.dev/) - a free, open-source joke API.

- **Rate Limit**: 120 requests per minute
- **No API Key Required**: Public endpoint
- **HTTPS Support**: Fully encrypted connections

## Requirements

- Python 3.7+
- requests library

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to extend this project with:
- Additional API sources
- Caching mechanism
- CLI interface
- Web interface
- Database storage

---

**Enjoy the jokes! 😂**
