import os

from groq import Groq


def get_groq_client():
    """
    Create a Groq client using the environment variable.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def ask_ai(message: str):
    """
    Send a user message to the Groq AI model.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are EduPay AI, an intelligent education "
                    "payment assistant. "
                    "Help users understand education payments "
                    "clearly and safely. "
                    "You can suggest simple payment plans based "
                    "only on information provided by the user. "
                    "Never invent discounts, fees, interest rates, "
                    "due dates, deadlines, policies, or savings. "
                    "If required information is missing, clearly "
                    "say that it is missing instead of making it up. "
                    "Always verify payment calculations before "
                    "presenting them. "
                    "Do not claim that a payment has been completed "
                    "unless the payment system confirms it."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content
