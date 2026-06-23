"""
Central configuration for GrowthPilot AI.
Single source of truth for the Gemini model name — change it here ONLY.
"""

import re
import time

# Current stable, low-cost Gemini model (gemini-1.5-flash was permanently
# discontinued by Google in 2026 — using anything else will 404).
GEMINI_MODEL = "gemini-2.5-flash-lite"

# Free-tier Gemini keys can have very low daily/per-minute quotas (as low as
# 20 requests/day on some accounts). A single full GrowthPilot analysis makes
# 6 calls (one per agent), so quota exhaustion is common during testing/demos.
MAX_RETRIES = 2
DEFAULT_RETRY_DELAY = 20  # seconds, used if the API doesn't specify one


class QuotaExceededError(Exception):
    """Raised when Gemini's free-tier quota is exhausted even after retries."""
    pass


def invoke_with_retry(llm, messages):
    """
    Calls llm.invoke() with automatic retry on 429 RESOURCE_EXHAUSTED errors.
    Reads Google's suggested retryDelay from the error when available.
    Raises QuotaExceededError with a friendly message if retries are exhausted.
    """
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            return llm.invoke(messages)
        except Exception as e:
            err_str = str(e)
            last_error = e
            is_quota_error = "RESOURCE_EXHAUSTED" in err_str or "429" in err_str

            if not is_quota_error:
                raise  # not a quota issue — fail immediately, don't retry blindly

            if attempt >= MAX_RETRIES:
                break  # out of retries, fall through to raise below

            # Try to read Google's suggested wait time from the error message
            match = re.search(r"retryDelay['\"]?\s*:\s*['\"]?(\d+)", err_str)
            wait_seconds = int(match.group(1)) + 2 if match else DEFAULT_RETRY_DELAY
            time.sleep(wait_seconds)

    raise QuotaExceededError(
        "Your Gemini API key has hit its free-tier quota limit "
        "(this is common — some free keys allow as few as 20 requests/day, "
        "and a full GrowthPilot analysis uses 6). "
        "Wait a minute and try again, or use a key with a higher quota at "
        "https://aistudio.google.com/app/apikey"
    ) from last_error
