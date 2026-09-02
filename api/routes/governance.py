"""
ContextIQ — Enterprise Data Quality & Governance API Routes
Exposes GET /api/v1/governance/shacl-report, /quality-metrics, and /lineage REST endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends

from governance.service import get_governance_service, GovernanceService

router = APIRouter(prefix="/governance", tags=["Data Quality & SHACL Governance"])


@router.get("/shacl-report")
def get_shacl_validation_report(
    service: GovernanceService = Depends(get_governance_service)
):
    """Retrieve dynamic SHACL shapes validation report and compliance score."""
    return service.get_shacl_report()


@router.get("/quality-metrics")
def get_data_quality_metrics(
    service: GovernanceService = Depends(get_governance_service)
):
    """Retrieve overall data quality dimensions (completeness, consistency, validity, uniqueness)."""
    return service.get_quality_metrics()


@router.get("/lineage")
def get_enterprise_data_lineage(
    service: GovernanceService = Depends(get_governance_service)
):
    """Retrieve end-to-end data lineage transformation graph."""
    return service.get_data_lineage()
