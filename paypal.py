import os
import requests


def get_paypal_access_token():
    """
    Get an OAuth 2.0 access token from PayPal Sandbox.
    """

    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    base_url = os.getenv(
        "PAYPAL_BASE_URL",
        "https://api-m.sandbox.paypal.com"
    )

    if not client_id or not client_secret:
        raise RuntimeError(
            "PayPal credentials are not configured."
        )

    response = requests.post(
        f"{base_url}/v1/oauth2/token",
        auth=(client_id, client_secret),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US"
        },
        data={
            "grant_type": "client_credentials"
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()["access_token"]


def create_paypal_order(
    amount: str,
    currency: str = "USD",
    description: str = "EduPay AI Education Payment"
):
    """
    Create a PayPal Sandbox order.
    """

    base_url = os.getenv(
        "PAYPAL_BASE_URL",
        "https://api-m.sandbox.paypal.com"
    )

    access_token = get_paypal_access_token()

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "description": description,
                "amount": {
                    "currency_code": currency,
                    "value": amount
                }
            }
        ]
    }

    response = requests.post(
        f"{base_url}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    

    return response.json()

def capture_paypal_order(order_id: str):
    """
    Capture an approved PayPal Sandbox order.
    """

    base_url = os.getenv(
        "PAYPAL_BASE_URL",
        "https://api-m.sandbox.paypal.com"
    )

    access_token = get_paypal_access_token()

    response = requests.post(
        f"{base_url}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()
