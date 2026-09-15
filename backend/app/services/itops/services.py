"""Service Portfolio, CMDB Configuration Items & Topology Mapping Service."""

from typing import List, Dict, Any

class ItOpsServicesService:
    @staticmethod
    def list_services(tenant_id: str = "tenant-default") -> List[Dict[str, Any]]:
        return [
            {
                "service_code": "SVC-AUTH-API",
                "name": "Identity & Authentication Service",
                "business_owner": "Chief Security Officer",
                "technical_owner": "IAM Platform Team",
                "criticality": "TIER_1",
                "availability_target": 99.99,
                "current_status": "OPERATIONAL",
                "uptime_30d": 99.995,
                "monthly_cost_usd": 1240.0
            },
            {
                "service_code": "SVC-PAYMENT-GATEWAY",
                "name": "Checkout & Payment Gateway",
                "business_owner": "VP E-Commerce",
                "technical_owner": "Payments Platform Team",
                "criticality": "TIER_1",
                "availability_target": 99.99,
                "current_status": "OPERATIONAL",
                "uptime_30d": 99.98,
                "monthly_cost_usd": 3850.0
            },
            {
                "service_code": "SVC-ANALYTICS-ENGINE",
                "name": "Phase 79 Governed Analytics Platform",
                "business_owner": "Chief Data Officer",
                "technical_owner": "Lakehouse Team",
                "criticality": "TIER_2",
                "availability_target": 99.9,
                "current_status": "OPERATIONAL",
                "uptime_30d": 99.92,
                "monthly_cost_usd": 4820.0
            }
        ]

    @staticmethod
    def get_cmdb_topology(service_code: str = "SVC-PAYMENT-GATEWAY", tenant_id: str = "tenant-default") -> Dict[str, Any]:
        return {
            "root_service": service_code,
            "nodes": [
                {"id": "USER-SESSION", "label": "End User Browser / Mobile App", "type": "USER"},
                {"id": "SVC-PAYMENT-GATEWAY", "label": "Payment Gateway API", "type": "SERVICE", "tier": "TIER_1"},
                {"id": "API-STRIPE-INTEGRATION", "label": "Third-Party Stripe Adapter", "type": "API"},
                {"id": "DB-PAYMENTS-PG", "label": "PostgreSQL Payments Cluster", "type": "DATABASE"},
                {"id": "K8S-CLUSTER-US-EAST", "label": "AWS EKS K8s Cluster", "type": "INFRASTRUCTURE"}
            ],
            "edges": [
                {"source": "USER-SESSION", "target": "SVC-PAYMENT-GATEWAY", "label": "HTTPS POST /charge"},
                {"source": "SVC-PAYMENT-GATEWAY", "target": "API-STRIPE-INTEGRATION", "label": "mTLS Call"},
                {"source": "SVC-PAYMENT-GATEWAY", "target": "DB-PAYMENTS-PG", "label": "SQL Read/Write"},
                {"source": "SVC-PAYMENT-GATEWAY", "target": "K8S-CLUSTER-US-EAST", "label": "Hosted On"}
            ]
        }
