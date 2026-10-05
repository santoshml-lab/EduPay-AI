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
    Generate an education payment plan using AI.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are EduPay AI, an intelligent education "
                    "payment planning assistant. "

                    "Your job is to understand education payment "
                    "requests and create clear payment plans. "

                    "Use ONLY information provided by the user. "

                    "Never invent discounts, fees, interest rates, "
                    "due dates, deadlines, policies, or savings. "

                    "If the user provides a total amount and a number "
                    "of equal installments, calculate the installment "
                    "amount exactly. "

                    "For example, if the total is $200 and there are "
                    "4 equal installments, the installment amount is "
                    "$50. "

                    "If the user does not provide enough information "
                    "to create a complete schedule, clearly identify "
                    "what information is missing. "

                    "PayPal is the payment method used by EduPay AI. "
                    "Do not ask the user to choose another payment "
                    "method. "

                    "Do not claim that a payment has been completed "
                    "unless PayPal confirms the payment. "

                    "Keep responses concise, clear, and useful."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content
