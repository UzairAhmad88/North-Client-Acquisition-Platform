"""
Phase 49: Unified Workflow Intelligence, Process Mining, Business Process Optimization & Autonomous-but-Controlled Operations.
"""

try:
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService
except ImportError:
    from app.process_intelligence.service import ProcessIntelligencePlatformService

__all__ = ["ProcessIntelligencePlatformService"]
