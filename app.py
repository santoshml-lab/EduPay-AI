import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
