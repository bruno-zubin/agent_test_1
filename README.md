# OpenRouter API Chat

A simple Python script to interact with various LLMs through the OpenRouter API.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```
   You can get an API key by signing up at [OpenRouter](https://openrouter.ai/).

## Usage

Run the script:
```bash
python main.py
```

The script includes a simple example that asks about the capital of France. You can modify the `prompt` variable in the `main()` function to ask different questions.

## Available Models

You can change the model by modifying the `model` parameter in the `chat_with_llm()` function. Some available models include:
- openai/gpt-3.5-turbo
- openai/gpt-4
- anthropic/claude-2
- google/palm-2

Check the [OpenRouter documentation](https://openrouter.ai/docs) for the full list of available models.