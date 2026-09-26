# AI Research & Image Generator

A small Streamlit app that researches a topic with web search and turns the result into an image prompt and generated picture.

## Features

- Researches a topic using OpenAI's web-search tool.
- Produces a concise, cited research brief.
- Creates an image prompt grounded in the research.
- Generates an image with OpenAI's image model.

## Setup

1. Create an API key at https://platform.openai.com/api-keys.
2. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

4. Run the app:

```bash
streamlit run app.py
```

The generated image is available for download from the app. Never commit your `.env` file.

## Configuration

- `OPENAI_API_KEY`: required.
- `OPENAI_TEXT_MODEL`: optional, defaults to `gpt-4.1-mini`.
- `OPENAI_IMAGE_MODEL`: optional, defaults to `gpt-image-1`.
