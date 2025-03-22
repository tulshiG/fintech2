from fastapi import APIRouter, HTTPException
from ..services.bureau_service import fetch_credit_scores

router = APIRouter(prefix="/credit", tags=["Credit"])

@router.get("/bureaus/{user_id}")
def get_credit_scores_from_bureaus(user_id: int):
    """Fetches credit scores from multiple bureaus."""
    scores = fetch_credit_scores(user_id)

    if "error" in scores:
        raise HTTPException(status_code=500, detail=scores["error"])

    return scores
from ..services.bureau_service import normalize_credit_scores

@router.get("/bureaus/unified/{user_id}")
def get_unified_credit_score(user_id: int):
    """Fetches and normalizes credit scores into a single unified score."""
    result = normalize_credit_scores(user_id)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
from ..services.scoring import assess_risk
from ..services.bureau_service import normalize_credit_scores

@router.get("/bureaus/risk/{user_id}")
def get_risk_assessment(user_id: int):
    """Fetches credit scores and assigns a risk category."""
    result = normalize_credit_scores(user_id)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    risk_level = assess_risk(result["unified_score"])
    result["risk_assessment"] = risk_level

    return result
from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user

router = APIRouter(prefix="/credit", tags=["Credit"])

@router.get("/protected-route")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user['username']}. You have access to this protected route!"}
