# Deployment guide

## Important: Vercel compatibility

This project is a Streamlit application. Streamlit maintains a long-lived WebSocket connection, while Vercel is primarily a serverless/static platform. The Streamlit server should not be deployed directly to Vercel.

## Recommended: Streamlit Community Cloud

1. Open [share.streamlit.io](https://share.streamlit.io/).
2. Choose `light2tech/ai-research-image-generator`.
3. Select branch `main` and file `app.py`.
4. In **Advanced settings → Secrets**, add:

```toml
OPENAI_API_KEY = "your-key"
OPENAI_TEXT_MODEL = "gpt-4.1-mini"
OPENAI_IMAGE_MODEL = "gpt-image-1"
```

5. Deploy.

The app reads `OPENAI_API_KEY` from both Streamlit Secrets and local environment variables.

## Deploy with Render

The repository includes `render.yaml` and `Dockerfile`.

1. Create a new **Blueprint** on [Render](https://render.com/).
2. Select this GitHub repository.
3. Add `OPENAI_API_KEY` as a secret environment variable.
4. Deploy. Render supplies the `PORT` value automatically.

## Deploy with Docker

```bash
docker build -t ai-research-image-generator .
docker run --rm -p 8501:8501 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  ai-research-image-generator
```

Open http://localhost:8501.

## Why Vercel failed

A `vercel.json` file cannot make a Streamlit process compatible with Vercel's serverless runtime. To use Vercel, the application would need to be rebuilt as a browser frontend plus serverless API routes, with a separate durable job/queue design for research and image generation. The current Docker/Streamlit deployment is the smallest reliable path.
