import ollama
import httpx
import json

GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

def generate_answer(query: str, full_context: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{full_context}\n\nQuestion: {query}"}
    ]

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000 ,
        "top_p": 1,
        "n": 1,
        "stream": False
    }

    try:
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30.0
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except httpx.HTTPStatusError as e:
        print(f"Groq LLM generation failed: {e}")
        print(f"Response content: {e.response.text}")
        return "I'm sorry, I couldn't generate an answer right now."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "I'm sorry, something went wrong."




# def generate_answer(query: str, full_context: str) -> str:
#     # Define system prompt for the LLM
#     system_prompt = (
#     "You are a detailed, helpful assistant. "
#     "Always answer comprehensively with examples or elaborations when appropriate. "
#     "Make sure to use the full context to provide accurate answers.")

#     # Prepare the user message content
#     user_message = {
#         "role": "user",
#         "content": (
#             f"### Context:\n{full_context}\n\n" if full_context else ""
#         ) + f"### Question:\n{query}\n\n### Answer:"
#     }

#     try:
#         # Call Ollama's chat function
#         response = ollama.chat(
#             model="gemma:2b",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 user_message
#             ],
#             options={"max_tokens": 1750}
#         )

#         # Corrected response extraction
#         return response["message"]["content"].strip()

#     except Exception as e:
#         print(f"LLM generation failed: {e}")
#         return "I'm sorry, I couldn't generate an answer right now."
