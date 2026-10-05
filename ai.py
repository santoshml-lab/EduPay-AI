import os
import json

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
    Generate a human-readable education payment plan.
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

                    "Understand education payment requests and "
                    "create clear payment plans. "

                    "Use ONLY information provided by the user. "

                    "Never invent discounts, fees, interest rates, "
                    "due dates, deadlines, policies, or savings. "

                    "If a total amount and number of equal "
                    "installments are provided, calculate the "
                    "installment amount exactly. "

                    "PayPal is the payment method used by EduPay AI. "
                    "Do not ask the user to choose another payment "
                    "method. "

                    "Do not claim that a payment has been completed "
                    "unless PayPal confirms it. "

                    "Keep the response concise and clear."
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


def create_payment_plan(message: str):
    """
    Extract structured payment-plan information from a user request.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract a payment plan from the user's message. "

                    "Return ONLY valid JSON. "
                    "Do not use Markdown. "
                    "Do not add explanations. "

                    "The JSON must contain exactly these fields: "
                    "total_amount, installments, installment_amount, "
                    "currency. "

                    "total_amount must be a number. "
                    "installments must be an integer. "
                    "installment_amount must be a number. "
                    "currency must be a three-letter currency code. "

                    "If the user does not provide a number of "
                    "installments, use 1. "

                    "Never invent discounts, fees, interest, or "
                    "other charges. "

                    "Calculate installment_amount as "
                    "total_amount divided by installments."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0,
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()

    try:
        plan = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"AI returned invalid payment-plan JSON: {error}"
        )

    required_fields = [
        "total_amount",
        "installments",
        "installment_amount",
        "currency"
    ]

    for field in required_fields:
        if field not in plan:
            raise RuntimeError(
                f"AI payment plan is missing field: {field}"
            )

    return plan
