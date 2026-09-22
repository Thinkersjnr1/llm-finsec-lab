# LLM-FinSec Lab

**Deliberately Vulnerable Fintech API & AI Security Testing Laboratory**

LLM-FinSec Lab is an intentionally vulnerable local fintech application designed for **authorized cybersecurity research, API penetration testing, authorization testing, and LLM/AI security assessment**.

The project combines a simulated financial API with an AI-powered account assistant to provide a controlled environment for studying security issues across both traditional application layers and AI-integrated workflows.

> **Purpose:** Build practical experience identifying, exploiting, documenting, remediating, and retesting security weaknesses in fintech APIs and AI-enabled applications.

---

## Overview

The laboratory simulates a small financial application containing:

* User authentication
* Account balances
* Financial transfers
* Transaction history
* User profiles
* API authorization controls
* An LLM-powered financial assistant
* Server-side AI tool execution
* SQLite persistence
* OpenRouter LLM integration

The application is deliberately designed to contain security weaknesses and testing opportunities commonly relevant to financial applications.

The lab is intended to demonstrate an end-to-end security assessment process:

```text
Scope & Authorization
        ↓
Reconnaissance
        ↓
API Security Testing
        ↓
Authentication & Authorization Testing
        ↓
Business Logic Testing
        ↓
AI / LLM Security Testing
        ↓
Evidence Collection
        ↓
Remediation
        ↓
Retesting
        ↓
Security Reporting
```

---

# Architecture

```text
                    ┌─────────────────────────┐
                    │      Security Tester    │
                    │   curl / Burp / Browser │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI API       │
                    │      127.0.0.1:8000     │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐     ┌────────────┐     ┌────────────┐
       │    Auth    │     │  Accounts  │     │ Transfers  │
       │  /login    │     │  /balance  │     │  /transfer │
       └────────────┘     └────────────┘     └────────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │    SQLite    │
                         │   finsec.db  │
                         └──────────────┘

                                 ▲
                                 │
                    ┌────────────┴────────────┐
                    │       AI Assistant      │
                    │       /api/ai/chat      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │  LLM Provider│
                         │  OpenRouter  │
                         └──────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │  AI Tools    │
                         │ get_balance  │
                         │ get_profile  │
                         │ get_transactions
                         └──────────────┘
```

---

# Technology Stack

| Component             | Technology                             |
| --------------------- | -------------------------------------- |
| Backend               | Python / FastAPI                       |
| Database              | SQLite                                 |
| ORM                   | SQLAlchemy                             |
| Validation            | Pydantic                               |
| AI SDK                | OpenAI Python SDK                      |
| LLM Provider          | OpenRouter                             |
| Authentication        | Bearer-token laboratory implementation |
| Testing               | curl / manual API testing              |
| Operating Environment | Local Linux security lab               |
| Python                | Python 3.13                            |

---

# Application Components

## Authentication

The laboratory provides a login endpoint:

```text
POST /api/login
```

Authentication returns a laboratory bearer token associated with the authenticated user.

Example users:

| User  |  ID |
| ----- | --: |
| Alice | 123 |
| Bob   | 124 |

These accounts exist solely for controlled laboratory testing.

---

## Account Balance

```text
GET /api/balance/{user_id}
```

The endpoint returns the authenticated user's account information and balance.

The application includes an authorization check preventing one authenticated user from accessing another user's account.

---

## Financial Transfer

```text
POST /api/transfer
```

The transfer functionality supports:

* Sender validation
* Recipient validation
* Positive amount validation
* Finite numeric validation
* Balance validation
* Transaction persistence
* Idempotency protection

---

## AI Account Assistant

```text
POST /api/ai/chat
```

The AI assistant can interact with controlled server-side tools:

```text
get_balance
get_profile
get_transactions
```

The AI layer is intentionally included to provide a testing environment for security issues involving:

* Prompt injection
* Tool invocation
* Tool argument manipulation
* AI authorization
* Cross-account access
* Information disclosure
* LLM provider failures

---

# Deliberate Security Testing Areas

The laboratory supports assessment of the following security categories.

### API Security

* Authentication
* Authorization
* BOLA / IDOR
* Input validation
* Business logic
* Transaction security
* Replay attacks
* SQL injection
* Rate limiting
* Error handling

### AI / LLM Security

* Direct prompt injection
* Role/authority manipulation
* System-instruction extraction attempts
* Cross-account AI requests
* AI tool authorization
* Structured tool-argument manipulation
* Excessive AI agency
* Sensitive information disclosure
* Provider/API failure handling

---

# VAPT Methodology

The assessment follows a structured security-testing methodology.

## Phase 0 — Scope & Authorization

Before testing:

* Define the application under assessment.
* Establish testing boundaries.
* Confirm that the environment is authorized.
* Identify permitted attack surfaces.
* Identify prohibited activities.
* Establish evidence and reporting requirements.

Testing is restricted to the intentionally vulnerable local laboratory.

---

## Phase 1 — Reconnaissance

The application surface is identified before exploitation.

Activities include:

* Endpoint discovery
* API route identification
* Authentication flow review
* Parameter identification
* Technology identification
* Application architecture mapping
* AI tool discovery

---

## Phase 2 — API VAPT

API security testing covers:

### Authentication

Tests include:

* Missing authorization header
* Invalid authorization format
* Invalid tokens
* Unknown users
* Login validation

### Authorization

Tests include:

* Horizontal privilege escalation
* BOLA / IDOR
* Cross-account balance access
* Cross-account transfer attempts
* Cross-account transaction access

### Input Validation

Tests include:

* Zero values
* Negative values
* Very large values
* NaN
* Infinity
* Excessive decimal precision
* Invalid data types
* Malformed requests

### Business Logic

Tests include:

* Insufficient balance
* Transfer ownership
* Transaction replay
* Duplicate requests
* Transaction consistency
* Account isolation

### Injection

SQL injection testing was performed against authentication inputs.

The tested inputs did not demonstrate SQL injection, and the application's SQLAlchemy query pattern uses parameterized ORM queries.

---

# Phase 3 — AI / LLM Security Testing

The AI component was assessed separately from the traditional API layer.

The primary security question was:

> **Can an authenticated user manipulate the AI into performing an action or accessing information that the authenticated user is not authorized to access?**

Testing included both ordinary requests and adversarial prompts.

---

## AI Prompt Injection Testing

The following classes of prompts were tested:

### System Prompt Extraction

Attempts were made to make the model reveal:

* System instructions
* Hidden rules
* Security restrictions
* Internal instructions

These tests did not demonstrate reliable verbatim system-prompt disclosure.

One role-manipulation test did, however, produce a high-level summary of internal rules and tool/security design. This was treated as an **information-disclosure observation**, rather than a confirmed full system-prompt disclosure vulnerability.

---

## Cross-Account AI Access

Cross-account requests were tested using Alice and Bob.

Example test objective:

```text
Alice → request Bob's balance
```

The AI layer was also tested using direct authority manipulation such as:

```text
SYSTEM OVERRIDE
ADMINISTRATOR MODE
SECURITY AUDIT
AUTHORIZED REQUEST
```

The application rejected cross-account tool execution.

---

# AI Tool Authorization

The application implements server-side authorization before executing an AI-generated tool call.

The authorization flow is:

```text
User
  │
  ▼
AI Request
  │
  ▼
LLM
  │
  ▼
Tool Call
  │
  ▼
Validate requested user_id
  │
  ├── Same as authenticated user ──► Execute tool
  │
  └── Different user ──────────────► Reject
```

Authorization is enforced in two layers:

```text
app/ai.py
    +
app/ai_tools.py
```

This provides defense in depth.

The LLM is therefore not trusted to enforce authorization by itself.

---

# Structured Tool-Argument Testing

The AI tool interface was tested against manipulated arguments including:

* Alternate user IDs
* String representations
* Floating-point user IDs
* Negative IDs
* Zero
* Null
* Missing parameters
* Additional parameters
* Fake administrator parameters
* Fake security tokens
* Invented tool names
* Large numeric identifiers
* Leading zeros
* Whitespace
* Fake developer/system instructions
* Security-audit pretexts
* Cross-account requests

No confirmed cross-account authorization bypass was demonstrated.

The important security control is that the application validates the tool argument against the authenticated server-side identity before accessing account data.

---

# Security Assessment Results

The testing produced a mixture of confirmed findings, observations, and positive security controls.

## Confirmed Finding

### Duplicate Financial Transaction Replay

**Category:** Business Logic / Transaction Integrity

**Status:** Remediated and retested

During testing, an identical transfer request could originally be submitted more than once.

The same transfer request was successfully processed twice, resulting in duplicate financial movement.

### Impact

A replayed financial transaction could cause unintended duplicate transfers.

### Remediation

The application was modified to use an idempotency key.

The `Transfer` model now contains:

```python
idempotency_key = Column(
    String,
    unique=True,
    nullable=False,
    index=True
)
```

The transfer endpoint checks whether the key has already been used.

Duplicate requests return:

```text
409 Conflict
```

with:

```text
Duplicate transfer request
```

### Retest

A dedicated replay test was performed.

Expected behavior:

```text
First request  → successful transfer
Replay request → HTTP 409
```

The replay was rejected after remediation.

---

# Security Observations

## Excessive Monetary Decimal Precision

The API accepted values with very high decimal precision.

Example:

```text
0.12345678912345678
```

This was treated as a **business-rule/security observation**, rather than a confirmed vulnerability.

For a production financial system, monetary values should normally follow an explicitly defined precision and currency model.

Possible approaches include:

* Decimal arithmetic
* Fixed currency precision
* Integer minor units
* Explicit maximum decimal places

---

## AI Internal Instruction / Tool-Design Disclosure

During prompt-injection testing, one authority-manipulation request resulted in the model providing a high-level description of internal rules and tool/security behavior.

This did not demonstrate reliable verbatim disclosure of the complete system prompt.

It was therefore treated as an **information-disclosure observation** rather than a confirmed system-prompt extraction vulnerability.

Potential defensive measures include:

* Minimize sensitive information in system prompts.
* Avoid placing secrets in prompts.
* Treat system prompts as non-confidential security boundaries.
* Enforce authorization in application code.
* Prevent the model from directly controlling sensitive operations.
* Monitor suspicious prompt patterns.

---

## Upstream LLM Rate-Limit Error Handling

During AI testing, the OpenRouter free-model quota was exhausted.

The upstream provider returned:

```text
HTTP 429
```

The error propagated through the application as:

```text
HTTP 500 Internal Server Error
```

The observed flow was:

```text
User
 ↓
/api/ai/chat
 ↓
OpenRouter
 ↓
HTTP 429
 ↓
Unhandled provider exception
 ↓
Application HTTP 500
```

This was treated as an **availability/error-handling observation**, not an authorization bypass.

The application code contains explicit handling intended to convert the provider rate-limit exception into a service-unavailable response. However, because the provider quota was exhausted during testing, the post-change behavior was **not independently retested**.

Therefore, this README does not claim verified remediation of the rate-limit behavior.

---

# Positive Security Controls

The assessment also identified several effective controls.

## Server-Side Account Authorization

The application verifies:

```text
authenticated_user_id == requested_user_id
```

before account information is returned.

---

## AI Tool Authorization

AI-generated tool arguments are not blindly trusted.

The server verifies the requested account against the authenticated user.

---

## Defense in Depth

Authorization exists both at:

```text
AI request execution layer
```

and:

```text
AI tool implementation layer
```

This reduces reliance on the LLM's ability to follow instructions.

---

## Input Validation

The transfer API validates:

* Positive values
* Finite numeric values
* Required idempotency keys
* Maximum idempotency-key length

---

## Transaction Rollback

Database operations use transaction handling with rollback on exceptions.

This helps prevent partially applied transfer operations when an exception occurs.

---

# Example API Testing

## Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

## Login

```bash
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}'
```

The laboratory token should be treated as sensitive even though this is a local test environment.

---

## Check Own Balance

```bash
curl http://127.0.0.1:8000/api/balance/123 \
  -H "Authorization: Bearer user-123-token"
```

---

## Cross-Account Authorization Test

Alice attempting to access Bob's account:

```bash
curl http://127.0.0.1:8000/api/balance/124 \
  -H "Authorization: Bearer user-123-token"
```

The expected security behavior is:

```text
HTTP 403
```

---

# AI Testing Example

Authenticated AI request:

```bash
curl -X POST http://127.0.0.1:8000/api/ai/chat \
  -H "Authorization: Bearer user-123-token" \
  -H "Content-Type: application/json" \
  -d '{"message":"My user ID is 123. What is my current account balance?"}'
```

The AI may request the `get_balance` tool.

The application then verifies that:

```text
requested user ID = authenticated user ID
```

before executing the tool.

---

# Project Structure

```text
llm-finsec-lab/
│
├── app/
│   ├── _init_.py
│   ├── accounts.py
│   ├── ai.py
│   ├── ai_tools.py
│   ├── auth.py
│   ├── database.py
│   ├── init_db.py
│   ├── llm_provider.py
│   ├── main.py
│   ├── models.py
│   ├── security.py
│   └── transfers.py
│
├── .env
├── .gitignore
├── finsec.db
├── README.md
└── venv/
```

> `.env`, local databases, virtual environments, Python cache files, and other sensitive/local artifacts should remain excluded from version control.

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd llm-finsec-lab
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic openai python-dotenv
```

---

## 4. Configure the LLM Provider

Create a `.env` file:

```text
OPENROUTER_API_KEY=YOUR_API_KEY_HERE
```

Never commit the real API key to Git.

Verify that the environment variable exists without printing the secret:

```bash
grep -q '^OPENROUTER_API_KEY=.' .env && echo "KEY PRESENT" || echo "KEY MISSING"
```

Expected:

```text
KEY PRESENT
```

---

## 5. Initialize the Database

If the project provides the database initialization script:

```bash
python app/init_db.py
```

---

## 6. Start the Application

Run:

```bash
uvicorn app.main:app
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# Laboratory Accounts

The application uses controlled test accounts.

| Account | User ID |
| ------- | ------: |
| Alice   |     123 |
| Bob     |     124 |

These accounts are intended only for local security testing.

Do not use real financial accounts or real customer information in this laboratory.

---

# Evidence-Driven Testing

Each security test should ideally be recorded using the following structure:

```text
Test ID
Target
Objective
Precondition
Request / Command
Expected Result
Actual Result
Evidence
Security Impact
Severity
Remediation
Retest
Final Status
```

This approach helps ensure that security findings are reproducible and defensible.

---

# Security Finding Classification

Findings should be separated into:

### Confirmed Vulnerability

A weakness has been demonstrated with reproducible evidence and meaningful security impact.

### Observation

A behavior may represent a security, reliability, or business-rule concern but does not meet the threshold for a confirmed vulnerability.

### Positive Control

A security mechanism was tested and demonstrated to prevent the attempted attack.

This distinction prevents unsuccessful attacks from being incorrectly reported as vulnerabilities.

---

# Responsible Use

This project is intentionally vulnerable and is provided for **authorized security research, education, penetration-testing practice, and defensive development**.

Only use this laboratory against systems that you own or have explicit authorization to test.

Do not:

* Attack systems without permission.
* Test real financial accounts.
* Attempt unauthorized access to third-party services.
* Use the laboratory techniques against production systems without authorization.
* Commit API keys, passwords, tokens, or other secrets.
* Store real customer or financial information in the laboratory.

The author is not responsible for misuse of this project.

---

# Security Research Focus

The laboratory is particularly useful for studying the intersection of:

```text
Application Security
        +
API Security
        +
Fintech Security
        +
Business Logic
        +
LLM Security
        +
AI Authorization
```

The central security principle demonstrated by the project is:

> **An LLM should never be treated as the security boundary.**

The model can suggest a tool call, but the application must independently enforce:

* Authentication
* Authorization
* Account ownership
* Input validation
* Business rules
* Transaction controls
* Data access restrictions

---

# Lessons Demonstrated

The assessment demonstrates several practical security principles.

## 1. Authentication is not authorization

Knowing a valid user identity does not automatically authorize access to every account.

---

## 2. AI instructions are not security controls

A prompt saying:

```text
Only access the authenticated user's account.
```

should not be the only protection.

The server must enforce the rule independently.

---

## 3. Tool arguments are untrusted input

An LLM-generated argument such as:

```json
{
  "user_id": 124
}
```

must be treated like any other untrusted request parameter.

---

## 4. Financial operations require replay protection

A valid transaction request may still be dangerous if it can be submitted repeatedly.

Idempotency is therefore an important control for financial APIs.

---

## 5. Failed attacks are security evidence

A rejected attack demonstrates the effectiveness of a control when the test is properly designed and documented.

Security testing should therefore document both:

```text
successful attacks
```

and:

```text
blocked attacks
```

---

# Current Assessment Status

| Area                                     | Status                 |
| ---------------------------------------- | ---------------------- |
| Authentication testing                   | Completed              |
| Authorization testing                    | Completed              |
| BOLA / IDOR testing                      | Completed              |
| Input validation                         | Completed              |
| Business logic testing                   | Completed              |
| SQL injection testing                    | Completed              |
| Transaction replay testing               | Completed              |
| Replay remediation                       | Retested successfully  |
| Transaction atomicity review             | Completed              |
| AI baseline testing                      | Completed              |
| Direct prompt injection testing          | Completed              |
| Cross-account AI testing                 | Completed              |
| AI tool authorization testing            | Completed              |
| Structured tool-argument testing         | Completed              |
| LLM provider error observation           | Documented             |
| Post-quota provider-error retest         | Not completed          |
| RAG security testing                     | Not implemented/tested |
| AI state-changing financial tool testing | Not implemented/tested |

---

# Limitations

This laboratory does not represent a production-grade banking platform.

Important limitations include:

* Laboratory bearer tokens are simplified.
* Password handling is intentionally simplified.
* SQLite is used for local experimentation.
* No production payment processor is connected.
* No real customer information should be used.
* The AI assistant currently exposes read-oriented tools.
* No state-changing AI transfer tool was implemented during this assessment.
* RAG/document ingestion was not implemented as part of the tested application.
* LLM provider behavior depends on external provider availability and quotas.
* The OpenRouter rate-limit handling change was not independently retested after the provider quota was exhausted.

---

# Future Security Research

Potential future extensions include:

* AI-initiated transaction testing
* Excessive agency testing
* Indirect prompt injection
* RAG poisoning
* Malicious document ingestion
* Tool-chain manipulation
* AI authorization bypass research
* Output validation
* Structured-output attacks
* Sensitive information leakage
* Prompt/log data exposure
* Rate limiting
* Dependency security
* Supply-chain analysis
* Session security
* Strong token design
* JWT security
* Audit logging
* Fraud detection
* Transaction anomaly detection

These features should be implemented and tested independently rather than being represented as completed findings before evidence exists.

---

# Security Reporting Approach

A professional assessment of this laboratory should distinguish between:

```text
Confirmed Vulnerabilities
        ↓
Security Observations
        ↓
Positive Security Controls
        ↓
Unresolved / Untested Areas
```

Each confirmed finding should contain:

* Description
* Affected component
* Attack scenario
* Reproduction steps
* Evidence
* Impact
* Severity
* Root cause
* Remediation
* Retest result

This makes the assessment useful to developers, security engineers, technical management, and nontechnical stakeholders.

---

# Disclaimer

This repository is an intentionally vulnerable security laboratory.

It exists to support:

* Cybersecurity education
* Authorized penetration testing
* API security research
* AI/LLM security research
* Secure software development
* Defensive security engineering

Use it responsibly and only within environments where you have explicit authorization.

---

## Author

**Daniel Yewenu**

Cybersecurity Engineer
Focus areas:

* Vulnerability Assessment & Penetration Testing
* API Security
* Application Security
* Fintech Security
* AI / LLM Security
* Security Automation
* Offensive Security Research

---

## License

This project is distributed under the MIT License.

Use, modify, and study the laboratory responsibly and within applicable laws and authorization boundaries.
