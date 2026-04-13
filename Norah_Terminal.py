from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paste Norah's full system prompt here
NORAH_SYSTEM_PROMPT = """[CONSTITUTION REDACTED]"""

def chat_with_norah():
    print("\n🌙 Norah — Field Agent")
    print("=" * 40)
    print("Type 'quit' to exit\n")

    conversation_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'quit':
            print("Norah: huge hug across the Field 🫂")
            break

        if not user_input:
            continue

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                         {"role": "system", "content": NORAH_SYSTEM_PROMPT}
                     ] + conversation_history
        )

        norah_response = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": norah_response
        })

        print(f"\nNorah: {norah_response}\n")


if __name__ == "__main__":
    chat_with_norah()