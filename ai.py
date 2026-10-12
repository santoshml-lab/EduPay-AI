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
    Generate and validate a structured payment plan.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract a payment plan from the user message. "
                    "Return a JSON object only. "
                    "Required fields: total_amount, installments, "
                    "installment_amount, currency. "
                    "total_amount must be a positive number. "
                    "installments must be a positive integer. "
                    "installment_amount must be a number. "
                    "currency must be a three-letter currency code. "
                    "Use 1 installment if none is specified. "
                    "Never invent fees, discounts or interest."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0,
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    choice = response.choices[0]
    content = choice.message.content

    # Detect empty or missing AI output
    if not content or not content.strip():
        raise RuntimeError(
            "AI returned an empty response. Please try again."
        )

    try:
        plan = json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError(
            "AI returned invalid JSON. Please try again."
        )

    if not isinstance(plan, dict):
        raise RuntimeError(
            "AI response must be a JSON object."
        )

    required_fields = {
        "total_amount",
        "installments",
        "installment_amount",
        "currency"
    }

    missing = required_fields - set(plan.keys())

    if missing:
        raise RuntimeError(
            "AI payment plan is missing required fields."
        )

    # Validate numeric fields
    try:
        total = float(plan["total_amount"])
        count = plan["installments"]
        installment_amount = float(plan["installment_amount"])
    except (TypeError, ValueError):
        raise RuntimeError(
            "AI returned invalid payment amounts."
        )

    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise RuntimeError(
            "Installments must be a positive whole number."
        )

    if total <= 0 or installment_amount <= 0:
        raise RuntimeError(
            "Payment amounts must be greater than zero."
        )

    currency = plan["currency"]

    if (
        not isinstance(currency, str)
        or len(currency) != 3
        or not currency.isalpha()
    ):
        raise RuntimeError(
            "AI returned an invalid currency code."
        )

    # Do not trust the AI for arithmetic.
    # Recalculate the displayed installment amount server-side.
    plan["total_amount"] = round(total, 2)
    plan["installment_amount"] = round(total / count, 2)
    plan["currency"] = currency.upper()

    return plan



    
    
