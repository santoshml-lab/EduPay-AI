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

def create_payment_plan(message):
    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=1000,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You create simple payment plans.

Return one valid JSON object only.
Do not use Markdown or code fences.
Always include these exact fields:
- total_amount: number
- installments: integer
- installment_amount: number
- currency: three-letter currency code
- installment_schedule: array of objects containing
  number and amount

Example of the required JSON structure:
{
  "total_amount": 250.00,
  "installments": 3,
  "installment_amount": 83.33,
  "currency": "USD",
  "installment_schedule": [
    {"number": 1, "amount": 83.33},
    {"number": 2, "amount": 83.33},
    {"number": 3, "amount": 83.34}
  ]
}

The schedule must add up exactly to total_amount.
Do not add fees or interest.
Use the amount, currency and installment count requested
by the user.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise ValueError("AI returned an empty payment plan.")

    try:
        plan = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"AI returned invalid JSON: {content[:300]}"
        ) from exc

    required = [
        "total_amount",
        "installments",
        "installment_amount",
        "currency",
        "installment_schedule",
    ]

    for field in required:
        if field not in plan:
            raise ValueError(f"Payment plan is missing: {field}")

    if (
        not isinstance(plan["installments"], int)
        or plan["installments"] < 1
    ):
        raise ValueError("Installment count must be a positive integer.")

    schedule = plan["installment_schedule"]

    if not isinstance(schedule, list):
        raise ValueError("Installment schedule must be a list.")

    if len(schedule) != plan["installments"]:
        raise ValueError("Installment count does not match the schedule.")

    try:
        total_cents = round(float(plan["total_amount"]) * 100)
        amounts = [
            round(float(item["amount"]) * 100)
            for item in schedule
        ]
    except (TypeError, ValueError, KeyError) as exc:
        raise ValueError("Payment plan contains invalid amounts.") from exc

    if total_cents <= 0 or any(amount <= 0 for amount in amounts):
        raise ValueError("All payment amounts must be positive.")

    if sum(amounts) != total_cents:
        raise ValueError("Installments do not add up to the total.")

    plan["installment_schedule"] = [
        {"number": i + 1, "amount": amount / 100}
        for i, amount in enumerate(amounts)
    ]

    plan["total_amount"] = total_cents / 100
    plan["installment_amount"] = amounts[0] / 100
    plan["currency"] = str(plan["currency"]).upper()

    return plan



    

    



    
    

    



    
    
