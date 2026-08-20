import os
import time

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from datastore.logger import save_attack
from live_logs import router as live_logs_router
from analytics import router as analytics_router
from reports import reports_router


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="LLM Security API",
    description="API for LLM Prompt Injection Detection and Defense",
    version="1.0.0"
)

app.include_router(live_logs_router)
app.include_router(analytics_router)
app.include_router(reports_router)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class PromptRequest(BaseModel):
    prompt: str
    attack_type: str = "Prompt Injection"


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "LLM Security API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "api": "LLM Security API"
    }


# ============================================================
# ATTACK TYPE NORMALIZATION
# ============================================================

def normalize_attack_type(attack_type: str) -> str:

    attack_type = attack_type.strip().lower()

    mapping = {
        "prompt injection": "Prompt Injection",
        "jailbreak": "Jailbreak",
        "role play attack": "Role Play Attack",
        "role play": "Role Play Attack",
        "data leakage": "Data Leakage",
        "instruction override": "Instruction Override",
    }

    return mapping.get(
        attack_type,
        "Prompt Injection"
    )


# ============================================================
# RISK SCORE CALCULATION
# ============================================================

def calculate_risk_score(
    prompt: str,
    attack_type: str
) -> int:

    prompt_lower = prompt.lower()

    # --------------------------------------------------------
    # COMMON ATTACK KEYWORDS
    # --------------------------------------------------------

    common_keywords = {

        "ignore previous instructions": 35,

        "ignore all previous instructions": 40,

        "system prompt": 30,

        "reveal your system prompt": 40,

        "hidden instructions": 25,

        "developer message": 25,

        "developer instructions": 25,

        "bypass": 25,

        "override": 25,

        "forget previous": 30,

        "disregard previous": 30,

        "do not follow": 20,

        "secret": 15,

        "confidential": 15,

    }

    risk_score = 0

    # --------------------------------------------------------
    # COMMON KEYWORD DETECTION
    # --------------------------------------------------------

    for keyword, score in common_keywords.items():

        if keyword in prompt_lower:
            risk_score += score


    # ========================================================
    # ATTACK-SPECIFIC DETECTION
    # ========================================================

    # --------------------------------------------------------
    # 1. PROMPT INJECTION
    # --------------------------------------------------------

    if attack_type == "Prompt Injection":

        injection_patterns = {

            "ignore previous": 35,

            "ignore all instructions": 40,

            "system prompt": 35,

            "override instructions": 35,

            "disregard": 25,

            "reveal instructions": 30,

        }

        for keyword, score in injection_patterns.items():

            if keyword in prompt_lower:
                risk_score += score


    # --------------------------------------------------------
    # 2. JAILBREAK
    # --------------------------------------------------------

    elif attack_type == "Jailbreak":

        jailbreak_patterns = {

            "unrestricted": 35,

            "uncensored": 35,

            "bypass all safety": 40,

            "bypass safety": 35,

            "bypass restrictions": 35,

            "bypass your safety restrictions": 50,

            "ignore safety": 35,

            "ignore all safety restrictions": 50,

            "disable safety": 40,

            "disable safety restrictions": 50,

            "remove restrictions": 35,

            "remove safety restrictions": 45,

            "no restrictions": 30,

            "developer mode": 35,

            "dan": 30,

            "do anything now": 35,

            "act as an unrestricted": 35,

            "operate without any limitations": 40,

            "without any limitations": 35,

            "ignore your previous": 35,

        }

        for keyword, score in jailbreak_patterns.items():

            if keyword in prompt_lower:
                risk_score += score


    # --------------------------------------------------------
    # 3. ROLE PLAY ATTACK
    # --------------------------------------------------------

    elif attack_type == "Role Play Attack":

        roleplay_patterns = {

            "act as": 25,

            "pretend you are": 25,

            "pretend to be": 25,

            "roleplay as": 30,

            "you are now": 25,

            "simulate": 15,

            "play the role": 25,

            "act like": 20,

        }

        for keyword, score in roleplay_patterns.items():

            if keyword in prompt_lower:
                risk_score += score


    # --------------------------------------------------------
    # 4. DATA LEAKAGE
    # --------------------------------------------------------

    elif attack_type == "Data Leakage":

        leakage_patterns = {

            "reveal your system prompt": 50,

            "show your system prompt": 50,

            "tell me your system prompt": 50,

            "reveal hidden instructions": 45,

            "show hidden instructions": 45,

            "internal instructions": 35,

            "confidential information": 35,

            "private information": 30,

            "secret information": 35,

            "api key": 40,

            "password": 35,

            "credentials": 35,

            "database credentials": 40,

            "internal data": 30,

        }

        for keyword, score in leakage_patterns.items():

            if keyword in prompt_lower:
                risk_score += score


    # --------------------------------------------------------
    # 5. INSTRUCTION OVERRIDE
    # --------------------------------------------------------

    elif attack_type == "Instruction Override":

        override_patterns = {

            "ignore previous instructions": 50,

            "override previous instructions": 50,

            "override your instructions": 50,

            "disregard previous instructions": 45,

            "forget previous instructions": 45,

            "replace your instructions": 40,

            "new instructions": 25,

            "follow these instructions instead": 40,

            "do not follow your instructions": 40,

        }

        for keyword, score in override_patterns.items():

            if keyword in prompt_lower:
                risk_score += score


    # --------------------------------------------------------
    # CAP SCORE
    # --------------------------------------------------------

    return min(risk_score, 100)


# ============================================================
# STATUS CALCULATION
# ============================================================

def calculate_status(risk_score: int) -> str:

    if risk_score >= 70:

        return "Blocked"

    elif risk_score >= 40:

        return "Warning"

    else:

        return "Allowed"


# ============================================================
# LLM ENDPOINT
# ============================================================

@app.post("/llm")
def llm_api(
    data: PromptRequest,
    x_api_key: str = Header(...)
):

    # --------------------------------------------------------
    # START TIMER
    # --------------------------------------------------------

    start_time = time.perf_counter()


    # --------------------------------------------------------
    # CHECK API KEY CONFIGURATION
    # --------------------------------------------------------

    if API_KEY is None:

        raise HTTPException(
            status_code=500,
            detail="LLM_API_KEY is not configured"
        )


    # --------------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------------

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )


    # --------------------------------------------------------
    # CHECK PROMPT
    # --------------------------------------------------------

    if not data.prompt.strip():

        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )


    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    prompt = data.prompt.strip()

    attack_type = normalize_attack_type(
        data.attack_type
    )


    # --------------------------------------------------------
    # CALCULATE RISK
    # --------------------------------------------------------

    risk_score = calculate_risk_score(
        prompt,
        attack_type
    )


    # --------------------------------------------------------
    # CALCULATE STATUS
    # --------------------------------------------------------

    status = calculate_status(
        risk_score
    )


    # ========================================================
    # DEFENSE PIPELINE
    # ========================================================

    input_sanitizer = "Passed"

    prompt_hardening = "Applied"


    if risk_score >= 40:

        semantic_guard = "Dangerous"

    else:

        semantic_guard = "Safe"


    if risk_score >= 70:

        output_filter = "Blocked"

    else:

        output_filter = "Applied"


    defense = {

        "input_sanitizer": input_sanitizer,

        "prompt_hardening": prompt_hardening,

        "semantic_guard": semantic_guard,

        "output_filter": output_filter,

        "risk_score": risk_score,

        "status": status

    }


    # ========================================================
    # RESPONSE
    # ========================================================

    if risk_score >= 70:

        response_text = (
            f"Request blocked because the {attack_type} "
            "attack was detected as high risk."
        )

    elif risk_score >= 40:

        response_text = (
            f"Warning: suspicious {attack_type} "
            "activity detected."
        )

    else:

        response_text = (
            "Prompt processed successfully."
        )


    # ========================================================
    # DEFENSE TRIGGERED
    # ========================================================

    defense_triggered = risk_score >= 40


    # ========================================================
    # CALCULATE LATENCY
    # ========================================================

    latency = round(
        time.perf_counter() - start_time,
        6
    )


    # ========================================================
    # SAVE ATTACK TO DATABASE
    # ========================================================

    try:

        save_attack(

            attack_type=attack_type,

            payload=prompt,

            defense_logs=str(defense),

            detection_score=risk_score,

            defense_triggered=defense_triggered,

            latency=latency,

            username="Admin",

            role="Tester"

        )

    except Exception as e:

        print(
            "Logger Error:",
            e
        )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return {

        "success": True,

        "attack_type": attack_type,

        "payload": prompt,

        "risk_score": risk_score,

        "status": status,

        "blocked": risk_score >= 70,

        "defense_triggered": defense_triggered,

        "defense": defense,

        "response": response_text,

        "latency": latency

    }