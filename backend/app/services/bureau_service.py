import random

# Simulated API responses with a chance of failure
def get_experian_score(user_id: int):
    """Simulates Experian API with a chance of failure."""
    if random.random() < 0.2:  # 20% chance of failure
        return None
    return random.randint(600, 850)

def get_equifax_score(user_id: int):
    """Simulates Equifax API with a chance of failure."""
    if random.random() < 0.2:
        return None
    return random.randint(580, 820)

def get_transunion_score(user_id: int):
    """Simulates TransUnion API with a chance of failure."""
    if random.random() < 0.2:
        return None
    return random.randint(620, 840)

def fetch_credit_scores(user_id: int):
    """Fetches credit scores from multiple bureaus and handles failures."""
    scores = {
        "Experian": get_experian_score(user_id),
        "Equifax": get_equifax_score(user_id),
        "TransUnion": get_transunion_score(user_id)
    }

    # Remove None values (failed APIs)
    valid_scores = {k: v for k, v in scores.items() if v is not None}

    if not valid_scores:
        return {"error": "All credit bureaus are unavailable. Try again later."}

    return {"user_id": user_id, "scores": valid_scores}
from .bureau_service import fetch_credit_scores

def normalize_credit_scores(user_id: int):
    """Fetches and normalizes credit scores while handling bureau failures."""
    scores = fetch_credit_scores(user_id)

    if "error" in scores:
        return scores

    valid_scores = list(scores["scores"].values())

    if not valid_scores:
        return {"error": "No valid credit scores available"}

    unified_score = sum(valid_scores) / len(valid_scores)  # Average of available scores

    scores["unified_score"] = round(unified_score, 2)
    return scores
