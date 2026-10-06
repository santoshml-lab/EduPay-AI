# EduPay AI

AI-powered education payment assistant that converts natural-language education payment requests into structured payment plans and connects them with PayPal Sandbox.

## Overview

EduPay AI helps users plan education payments using natural language.

A user can describe an education payment request such as:

> I need to pay $999 for an advanced AI certification course. I want to split it into 3 equal installments.

EduPay AI uses AI to understand the request and generate:

- Total payment amount
- Number of installments
- Installment amount
- Currency

## How It Works

```text
User Payment Request
        |
        v
AI Payment Planner
        |
        v
Structured Payment Plan
        |
        v
PayPal Sandbox Order
        |
        v
PayPal Checkout
        |
        v
Payment Approval
        |
        v
Automatic Capture
        |
        v
Payment Success

I need to pay $999 for an advanced AI certification course.
I want to split it into 3 equal installments.

Total Amount: USD 999
Installments: 3
Each Payment: USD 333

## Key Features

### AI Payment Understanding

EduPay AI understands natural-language education payment requests.

### Smart Payment Planning

The AI extracts the total amount and installment count and calculates the installment amount.

```text
Installment Amount = Total Amount / Number of Installments

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Cloudflare Workers

### Backend

- Python
- FastAPI
- Uvicorn
- Requests

### AI

- Groq API
- OpenAI GPT-OSS-20B model through Groq

### Payments

- PayPal REST API
- PayPal Sandbox

### Deployment

- Frontend: Cloudflare Workers
- Backend: Render

## Backend API

### Health Check

```text
GET /health

POST /ai/payment-plan

{
  "message": "I need to pay $999 for an advanced AI certification course. I want to split it into 3 equal installments."
}

{
  "status": "success",
  "message": "I need to pay $999 for an advanced AI certification course. I want to split it into 3 equal installments.",
  "payment_plan": {
    "total_amount": 999,
    "installments": 3,
    "installment_amount": 333,
    "currency": "USD"
  }
}

POST /paypal/create-order

GET /paypal/order/{order_id}

## Environment Variables

The backend requires the following environment variables:

```text
PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET
PAYPAL_BASE_URL
GROQ_API_KEY

PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com

## Local Backend Setup

Clone the repository:

```bash
git clone https://github.com/santoshml-lab/EduPay-AI.git

cd EduPay-AI

python -m venv venv

pip install -r requirements.txt

uvicorn app:app --reload

http://localhost:8000

## Hosted Application

### Frontend

https://edupay-ai-frontend.santoshkrsbg36.workers.dev/

### Backend

https://edupay-ai.onrender.com/

### Backend Health Check

https://edupay-ai.onrender.com/health

## Testing

The application has been tested with multiple education payment scenarios.

### Test 1

```text
Total: USD 200
Installments: 4
Each Payment: USD 50

Total: USD 360
Installments: 6
Each Payment: USD 60

Total: USD 150
Installments: 1
Each Payment: USD 150

Total: USD 999
Installments: 3
Each Payment: USD 333

Natural Language Request
        ↓
AI Payment Plan
        ↓
Payment Plan Display
        ↓
PayPal Order Creation
        ↓
PayPal Sandbox Checkout
        ↓
Buyer Approval
        ↓
Automatic Capture
        ↓
Payment Confirmation
        ↓
Order ID + Capture ID
        ↓
Create Another Payment Plan

## PayPal Sandbox

EduPay AI uses PayPal Sandbox for payment testing and demonstration.

All transactions in the hosted demo are test transactions.

No real money is charged during Sandbox transactions.

## Project Status

EduPay AI is a working prototype demonstrating an AI-powered education payment experience integrated with PayPal Sandbox.

The complete AI-to-payment workflow has been tested successfully.

## License

This project is released under the MIT License.

See the `LICENSE` file for details.

## Hackathon

Built for the PayPal AI Hackathon.

The project combines:

- Artificial Intelligence
- Education
- Payment Planning
- Natural Language Processing
- PayPal Sandbox
- Automated Payment Capture

