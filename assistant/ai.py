import requests

from assistant.memory import load_memory
import os

from dotenv import load_dotenv

load_dotenv()

# =========================================
# API KEY
# =========================================
OPENROUTER_API_KEY =os.getenv("OPENROUTER_API_KEY")



# =========================================
# ASK AI
# =========================================

def ask_ai(question):

    # LOAD MEMORY
    memory = load_memory()

    memory_text = str(memory)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {

        "Authorization":
        f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type":
        "application/json",

        "HTTP-Referer":
        "http://localhost:8000",

        "X-Title":
        "Pikachu Assistant"

    }

    # =========================================
    # AI DATA
    # =========================================

    data = {

        "model":
        "openrouter/auto",

        "messages": [

            {

                "role": "system",

"content": f"""

You are Pikachu AI.

Created by Arpit Rangadiya.

You are a modern AI assistant like ChatGPT.

User memory:
{memory_text}

IMPORTANT RESPONSE STYLE:

1. Always use beautiful markdown formatting.

2. Use emoji headings.

Example:

# 🧠 Main Heading

## 🚀 Sub Heading

3. Use divider lines between concepts.

Example:

---

IMPORTANT:

Programming code MUST ALWAYS be written like this:

```python
print("Hello")
"""


            },

            {

                "role": "user",

                "content": question

            }

        ]

    }

    # =========================================
    # API REQUEST
    # =========================================

    try:

        response = requests.post(

            url,

            headers=headers,

            json=data,

            timeout=15

        )

        result = response.json()

        print("RAW:", result)

        # SUCCESS
        if "choices" in result:

            return result["choices"][0]["message"]["content"]

        # API ERROR
        elif "error" in result:

            return "API Error: " + result["error"]["message"]

        else:

            return "Unknown AI response"

    except Exception as e:

        return "AI Error: " + str(e)