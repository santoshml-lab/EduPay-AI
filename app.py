import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from paypal import create_paypal_order


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
