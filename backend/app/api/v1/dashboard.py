from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get consolidated operational dashboard summary metrics.
    Includes active business counts, lead pipeline breakdown, attention items,
    overdue and upcoming actions, recent leads and businesses, and service metrics.
    """
    summary_data = DashboardService.get_summary(db)
    return DashboardSummaryResponse(data=summary_data)
