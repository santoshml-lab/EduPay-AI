import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from ai import ask_ai, create_payment_plan

from paypal import create_paypal_order, capture_paypal_order


app = FastAPI(
    title="EduPay AI",
    description="AI-powered education payment assistant using PayPal Sandbox.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PaymentRequest(BaseModel):
    amount: str = Field(min_length=1)
    currency: str = "USD"
    description: str = "EduPay AI Education Payment"


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "EduPay AI backend is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

class AIRequest(BaseModel):
    message: str = Field(min_length=1)


@app.post("/ai/chat")
def ai_chat(request: AIRequest):
    try:
        answer = ask_ai(request.message)

        return {
            "status": "success",
            "message": request.message,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(error)}"
        )

@app.post("/ai/payment-plan")
def ai_payment_plan(request: AIRequest):
    try:
        plan = create_payment_plan(request.message)

        return {
            "status": "success",
            "message": request.message,
            "payment_plan": plan
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI payment plan failed: {str(error)}"
        )


@app.get("/paypal-config")
def paypal_config():
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    base_url = os.getenv(
        "PAYPAL_BASE_URL",
        "https://api-m.sandbox.paypal.com"
    )

    return {
        "paypal_configured": bool(client_id and client_secret),
        "sandbox": "sandbox" in base_url,
        "base_url": base_url
    }


@app.post("/paypal/create-order")
def create_order(request: PaymentRequest):
    try:
        order = create_paypal_order(
            amount=request.amount,
            currency=request.currency,
            description=request.description
        )

        return {
            "status": "success",
            "message": "PayPal Sandbox order created.",
            "order": order
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PayPal order creation failed: {str(error)}"
        )


@app.post("/paypal/capture-order/{order_id}")
def capture_order(order_id: str):
    try:
        result = capture_paypal_order(order_id)

        return {
            "status": "success",
            "message": "PayPal Sandbox order captured.",
            "order": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PayPal order capture failed: {str(error)}"
        )


@app.get("/paypal/order/{order_id}")
def get_order(order_id: str):
    try:
        import requests

        from paypal import get_paypal_access_token

        base_url = os.getenv(
            "PAYPAL_BASE_URL",
            "https://api-m.sandbox.paypal.com"
        )

        access_token = get_paypal_access_token()

        response = requests.get(
            f"{base_url}/v2/checkout/orders/{order_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if not response.ok:
            raise RuntimeError(response.text)

        return {
            "status": "success",
            "order": response.json()
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PayPal order lookup failed: {str(error)}"
        )


@app.get("/paypal/success")
def paypal_success(token: str | None = None):
    return {
        "status": "success",
        "message": "PayPal Sandbox checkout completed successfully.",
        "order_id": token,
        "next_step": "Capture the approved PayPal order."
    }


@app.get("/paypal/cancel")
def paypal_cancel(token: str | None = None):
    return {
        "status": "cancelled",
        "message": "PayPal Sandbox checkout was cancelled.",
        "order_id": token
    }


