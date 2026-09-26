import base64
import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Research & Image Generator", page_icon="🧭", layout="wide")


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Add it to your .env file.")
    return OpenAI(api_key=api_key)


def research_topic(client: OpenAI, topic: str) -> str:
    model = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
    response = client.responses.create(
        model=model,
        tools=[{"type": "web_search_preview"}],
        input=(
            "Research the following topic using reliable, recent sources. Return a concise "
            "brief with: key facts, useful context, uncertainty or conflicting evidence, "
            "and a final section titled Sources containing the URLs used. Cite claims inline "
            f"when possible. Topic: {topic}"
        ),
    )
    return response.output_text


def create_image(client: OpenAI, topic: str, research: str, style: str) -> tuple[bytes, str]:
    text_model = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
    prompt_response = client.responses.create(
        model=text_model,
        input=(
            "Create one detailed, safe image-generation prompt based on this topic and "
            "research. Do not include text, labels, logos, or citations in the image. "
            f"Topic: {topic}\nStyle: {style}\nResearch:\n{research}"
        ),
    )
    image_prompt = prompt_response.output_text.strip()
    image_response = client.images.generate(
        model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"),
        prompt=image_prompt,
        size="1024x1024",
    )
    image_data = getattr(image_response.data[0], "b64_json", None)
    if not image_data:
        raise RuntimeError("The image service returned no image data.")
    return base64.b64decode(image_data), image_prompt


st.title("🧭 Research & Image Generator")
st.write("Research a topic, then turn the findings into an illustrative picture.")

with st.sidebar:
    st.header("Settings")
    style = st.selectbox(
        "Image style",
        ["editorial illustration", "photorealistic", "watercolor", "cinematic concept art", "minimalist 3D"],
    )
    st.caption("Research and image generation use your configured OpenAI API key.")

topic = st.text_input("What should I research and illustrate?", placeholder="Example: How coral reefs support ocean ecosystems")

if st.button("Research and generate", type="primary", disabled=not topic.strip()):
    try:
        client = get_client()
        with st.spinner("Researching reliable sources..."):
            research = research_topic(client, topic.strip())
        st.session_state["research"] = research
        st.session_state["topic"] = topic.strip()

        with st.spinner("Creating your image..."):
            image_bytes, image_prompt = create_image(client, topic.strip(), research, style)
        st.session_state["image_bytes"] = image_bytes
        st.session_state["image_prompt"] = image_prompt
    except Exception as exc:
        st.error(f"Something went wrong: {exc}")

if "research" in st.session_state:
    left, right = st.columns(2)
    with left:
        st.subheader("Research brief")
        st.markdown(st.session_state["research"])
    with right:
        st.subheader("Generated picture")
        st.image(st.session_state["image_bytes"], use_container_width=True)
        st.download_button(
            "Download PNG",
            data=st.session_state["image_bytes"],
            file_name="research-illustration.png",
            mime="image/png",
        )
        with st.expander("Image prompt"):
            st.write(st.session_state.get("image_prompt", ""))
