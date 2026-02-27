import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=os.getenv("HUGGINGFACE_API_KEY")
)
def ask_llm(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an intelligent academic assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"