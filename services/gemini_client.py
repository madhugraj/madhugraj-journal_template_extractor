import os
from vertexai import init
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
from google.generativeai import configure, GenerativeModel as APIModel

# ✅ Initialize Vertex AI
init(project="yavar-client-poc", location="us-central1")


# ✨ Gemini Pro Text Chat (with public API fallback)
def gemini_chat(prompt: str) -> str:
    try:
        model = GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text or ""
    except Exception as e:
        print(f"❌ Gemini Vertex chat failed: {e}")

        # 🔁 Fallback using Gemini API Key
        api_key = "AIzaSyAe8rheF4wv2ZHJB2YboUhyyVlM2y0vmlk"
        if api_key:
            try:
                configure(api_key=api_key)
                fallback_model = APIModel("models/gemini-1.5-pro")
                response = fallback_model.generate_content(prompt)
                return response.text or "⚠️ Fallback used, but response empty."
            except Exception as fallback_error:
                print(f"❌ Fallback Gemini API failed: {fallback_error}")
        return "❌ Gemini chat failed and fallback unavailable."


# 🖼️ Gemini Vision Chat (Vertex AI only)
def gemini_vision_chat(prompt: str, image_path: str) -> str:
    try:
        model = GenerativeModel("gemini-2.5-pro")
        with open(image_path, "rb") as f:
            image_data = f.read()
        img = Part.from_data(data=image_data, mime_type="image/png")
        response = model.generate_content([prompt, img])
        return response.text or ""
    except Exception as e:
        print(f"❌ Vision API failed: {e}")
        return "❌ Vision API failed."
