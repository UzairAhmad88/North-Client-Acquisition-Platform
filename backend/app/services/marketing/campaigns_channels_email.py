"""
Phase 59: Campaigns, Channels, Email Sequences, and Consent/Suppression Governance
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, CampaignStatus, CampaignType, generate_id


class CampaignsChannelsEmailService:
    """Manages marketing campaigns, stage progression, channels, email sequences, and suppression lists."""

    def __init__(self):
        self._campaigns: Dict[str, AttrDict] = {}
        self._campaign_versions: Dict[str, List[AttrDict]] = {}
        self._channels: Dict[str, AttrDict] = {}
        self._channel_metrics: Dict[str, List[AttrDict]] = {}
        self._email_campaigns: Dict[str, AttrDict] = {}
        self._email_templates: Dict[str, AttrDict] = {}
        self._email_sequences: Dict[str, AttrDict] = {}
        self._suppressions: Dict[str, AttrDict] = {}

    def create_campaign(
        self,
        name: str,
        campaign_type: str = CampaignType.DEMAND_GENERATION.value,
        target_audience_id: Optional[str] = None,
        allocated_budget_usd: float = 25000.0,
        channels: Optional[List[str]] = None,
        owner: str = "growth_lead",
    ) -> AttrDict:
        campaign_id = generate_id("cmp")
        campaign = AttrDict({
            "id": campaign_id,
            "name": name,
            "campaign_type": campaign_type,
            "status": CampaignStatus.DRAFT.value,
            "target_audience_id": target_audience_id,
            "allocated_budget_usd": allocated_budget_usd,
            "actual_spend_usd": 0.0,
            "leads_generated": 0,
            "mql_generated": 0,
            "sql_generated": 0,
            "opportunities_influenced": 0,
            "pipeline_influenced_usd": 0.0,
            "revenue_attributed_usd": 0.0,
            "channels": channels or ["EMAIL", "LINKEDIN", "ORGANIC_SEARCH"],
            "owner": owner,
            "is_governance_approved": False,
            "start_date": None,
            "end_date": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        })
        self._campaigns[campaign_id] = campaign

        initial_ver = AttrDict({
            "id": generate_id("cver"),
            "campaign_id": campaign_id,
            "version_number": 1,
            "snapshot": dict(campaign),
            "created_at": datetime.utcnow().isoformat(),
        })
        self._campaign_versions[campaign_id] = [initial_ver]
        return campaign

    def advance_campaign_status(
        self,
        campaign_id: str,
        target_status: str,
        approved_by: Optional[str] = None,
    ) -> AttrDict:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        # Governance safety check: APPROVED, ACTIVE or SCHEDULED
        if target_status == CampaignStatus.APPROVED.value and approved_by:
            campaign.is_governance_approved = True
        elif target_status in [CampaignStatus.ACTIVE.value, CampaignStatus.SCHEDULED.value]:
            if not campaign.is_governance_approved and not approved_by:
                raise ValueError("Campaign launch requires human governance approval before activation.")
            if approved_by:
                campaign.is_governance_approved = True

        campaign.status = target_status
        campaign.updated_at = datetime.utcnow().isoformat()

        # Record version snapshot
        new_v_num = len(self._campaign_versions.get(campaign_id, [])) + 1
        ver_record = AttrDict({
            "id": generate_id("cver"),
            "campaign_id": campaign_id,
            "version_number": new_v_num,
            "snapshot": dict(campaign),
            "created_at": datetime.utcnow().isoformat(),
        })
        if campaign_id not in self._campaign_versions:
            self._campaign_versions[campaign_id] = []
        self._campaign_versions[campaign_id].append(ver_record)

        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[AttrDict]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self, status: Optional[str] = None) -> List[AttrDict]:
        if status:
            return [c for c in self._campaigns.values() if c.status == status]
        return list(self._campaigns.values())

    def create_channel(
        self,
        name: str,
        channel_type: str = "ORGANIC_SEARCH",
        total_spend_usd: float = 0.0,
        total_revenue_usd: float = 0.0,
        avg_cac_usd: float = 0.0,
        avg_roas: float = 0.0,
    ) -> AttrDict:
        channel_id = generate_id("chn")
        channel = AttrDict({
            "id": channel_id,
            "name": name,
            "channel_type": channel_type,
            "is_active": True,
            "total_spend_usd": total_spend_usd,
            "total_revenue_usd": total_revenue_usd,
            "avg_cac_usd": avg_cac_usd,
            "avg_roas": avg_roas,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._channels[channel_id] = channel
        return channel

    def list_channels(self) -> List[AttrDict]:
        return list(self._channels.values())

    def record_suppression(
        self,
        email: str,
        reason: str = "UNSUBSCRIBE",
        source: str = "user_opt_out",
    ) -> AttrDict:
        clean_email = email.strip().lower()
        suppression_id = generate_id("sup")
        suppression = AttrDict({
            "id": suppression_id,
            "email": clean_email,
            "reason": reason,
            "source": source,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._suppressions[clean_email] = suppression
        return suppression

    def is_suppressed(self, email: str) -> bool:
        clean_email = email.strip().lower()
        return clean_email in self._suppressions

    def create_email_sequence(
        self,
        name: str,
        target_audience_id: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
    ) -> AttrDict:
        seq_id = generate_id("seq")
        seq = AttrDict({
            "id": seq_id,
            "name": name,
            "target_audience_id": target_audience_id,
            "steps": steps or [
                {"step_num": 1, "delay_days": 0, "template_name": "Executive Problem Introduction", "cta": "Read Guide"},
                {"step_num": 2, "delay_days": 3, "template_name": "Case Study & Measurable Impact", "cta": "View Benchmarks"},
                {"step_num": 3, "delay_days": 5, "template_name": "Consultative Solution Walkthrough", "cta": "Book Review"},
            ],
            "enrolled_count": 0,
            "completed_count": 0,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._email_sequences[seq_id] = seq
        return seq

    def list_email_sequences(self) -> List[AttrDict]:
        return list(self._email_sequences.values())
