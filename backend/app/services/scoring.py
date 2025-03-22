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

def assess_risk(unified_score: float):
    """Classifies risk based on credit score."""
    if unified_score >= 750:
        return "Low Risk"
    elif unified_score >= 650:
        return "Medium Risk"
    else:
        return "High Risk"
