import os
import json

from groq import Groq
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


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
    """Generate a validated payment plan with exact cent amounts."""

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract a payment plan from the user's message. "
                    "Return only a JSON object with total_amount, "
                    "installments, installment_amount and currency. "
                    "total_amount must be a positive number. "
                    "installments must be a positive integer. "
                    "Use 1 installment if not specified. "
                    "currency must be a three-letter currency code. "
                    "Never invent fees, discounts or interest."
                )
            },
            {"role": "user", "content": message}
        ],
        temperature=0,
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise RuntimeError("AI returned an empty response.")

    try:
        plan = json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError("AI returned invalid JSON.")

    if not isinstance(plan, dict):
        raise RuntimeError("AI response must be a JSON object.")

    required = {
        "total_amount", "installments",
        "installment_amount", "currency"
    }

    if not required.issubset(plan):
        raise RuntimeError("AI payment plan is missing required fields.")

    try:
        total = Decimal(str(plan["total_amount"])).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        count = plan["installments"]
    except (InvalidOperation, ValueError, TypeError):
        raise RuntimeError("AI returned invalid payment amounts.")

    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise RuntimeError("Installments must be a positive whole number.")

    if total <= 0:
        raise RuntimeError("Total amount must be greater than zero.")

    currency = plan["currency"]

    if (
        not isinstance(currency, str)
        or len(currency) != 3
        or not currency.isalpha()
    ):
        raise RuntimeError("AI returned an invalid currency code.")

    # Work in cents to avoid floating-point rounding errors.
    total_cents = int(total * 100)

    if count > total_cents:
        raise RuntimeError(
            "Too many installments for the requested amount."
        )

    base_cents, remainder = divmod(total_cents, count)

    schedule = []

    for index in range(count):
        cents = base_cents

        # Add remaining cents to the final installments.
        if index >= count - remainder:
            cents += 1

        schedule.append({
            "number": index + 1,
            "amount": f"{cents // 100}.{cents % 100:02d}"
        })

    plan["total_amount"] = f"{total_cents // 100}.{total_cents % 100:02d}"
    plan["installments"] = count
    plan["installment_schedule"] = schedule

    # Keep compatibility with the existing frontend.
    plan["installment_amount"] = schedule[0]["amount"]
    plan["currency"] = currency.upper()

    return plan



    
    

    



    
    
