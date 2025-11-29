# utils/llama_helper.py
from litellm import completion

def ask_llama(prompt: str):
    try:
        response = completion(
            model="ollama/gpt-oss:20b",  # ✅ use one you actually have
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error contacting model: {e}"
