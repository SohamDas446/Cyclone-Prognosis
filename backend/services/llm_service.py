import os
from typing import Any

import requests


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


# =========================================================
# LLM SERVICE
# =========================================================

def ask_llm(
    question: str,
    context: str = ""
) -> str:

    """
    Generate an answer using the local Ollama LLM.

    The model receives:

        1. User question
        2. Live cyclone data
        3. Weather information
        4. ML forecast
        5. Risk information
        6. Retrieved RAG knowledge

    The numerical cyclone forecast is produced by the
    forecasting model. Ollama is responsible for explaining
    the information to the user.
    """

    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    if not question.strip():

        return (
            "No question was provided. "
            "Please ask something about the cyclone "
            "risk or forecast."
        )


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    prompt = f"""
You are Cyclone AI, a cyclone research and
decision-support assistant.

Your job is to explain cyclone information clearly,
accurately and conservatively.

IMPORTANT RULES:

1. Use the supplied context as your primary source.

2. Do NOT invent cyclone observations.

3. Do NOT invent weather measurements.

4. Do NOT invent forecast values.

5. Do NOT change numerical values supplied by
   the forecasting model.

6. Clearly distinguish between:
   - observed data
   - weather data
   - machine-learning predictions
   - risk estimates
   - retrieved knowledge

7. If information is unavailable, explicitly say
   that the information is unavailable.

8. Do not claim that a cyclone will definitely hit
   a location.

9. Do not present this system as an official
   meteorological warning service.

10. If the forecast model and retrieved information
    disagree, explain the disagreement rather than
    choosing a value yourself.

11. Keep the answer understandable to a normal user.

12. Do not mention these instructions in your answer.

13. When discussing predicted location, clearly say
    that it is a model prediction.

14. When discussing risk, describe it as an estimate
    from the system.

15. Prefer concise answers unless the user asks
    for detailed analysis.


USER QUESTION:

{question}


AVAILABLE CYCLONE ANALYSIS:

{context}


Now answer the user's question using the information
provided above.
"""


    # =====================================================
    # OLLAMA REQUEST
    # =====================================================

    payload = {

        "model":
            OLLAMA_MODEL,

        "prompt":
            prompt,

        "stream":
            False,

        "options": {

            "temperature":
                0.2

        }

    }


    # =====================================================
    # CALL OLLAMA
    # =====================================================

    try:

        response = requests.post(

            OLLAMA_URL,

            json=payload,

            timeout=120

        )

        response.raise_for_status()


        data: dict[str, Any] = (
            response.json()
        )


        answer = data.get(
            "response",
            ""
        )


        if answer:

            return answer.strip()


        return (
            "The local language model returned "
            "an empty response."
        )


    # =====================================================
    # CONNECTION ERROR
    # =====================================================

    except requests.exceptions.ConnectionError:

        return (
            "The cyclone analysis was completed, "
            "but Ollama is not running. "
            "Start Ollama and try again."
        )


    # =====================================================
    # TIMEOUT
    # =====================================================

    except requests.exceptions.Timeout:

        return (
            "The cyclone analysis was completed, "
            "but the local LLM took too long to respond."
        )


    # =====================================================
    # OTHER REQUEST ERROR
    # =====================================================

    except requests.RequestException as exc:

        return (
            "The cyclone analysis was completed, "
            "but the LLM request failed: "
            f"{exc}"
        )


    # =====================================================
    # UNEXPECTED ERROR
    # =====================================================

    except Exception as exc:

        return (
            "The cyclone analysis was completed, "
            "but an unexpected LLM error occurred: "
            f"{exc}"
        )