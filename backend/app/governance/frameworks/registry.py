"""
Governance Framework Registry & Standard Regulatory Catalog (Section 6 & 7).
"""

from typing import Dict, List, Optional
from backend.app.governance.base import (
    FrameworkCategory,
    GovernanceFramework,
    GovernanceRequirement,
    RequirementStatus,
)


class FrameworkRegistry:
    """Central repository of supported compliance frameworks and regulatory clauses."""

    def __init__(self):
        self._frameworks: Dict[str, GovernanceFramework] = {}
        self._requirements: Dict[str, List[GovernanceRequirement]] = {}
        self._seed_default_frameworks()

    def _seed_default_frameworks(self) -> None:
        """Seeds canonical industry frameworks and standard regulatory requirements."""
        # 1. SOC 2 Type II
        soc2 = GovernanceFramework(
            framework_code="SOC2_TYPE_II",
            name="AICPA SOC 2 Type II Trust Services Criteria",
            version="2017-rev",
            category=FrameworkCategory.INFORMATION_SECURITY,
            description="Security, Confidentiality, and Availability criteria for service organizations.",
            owner="soc2_lead_auditor",
        )
        self.register_framework(soc2)
        self.register_requirements("SOC2_TYPE_II", [
            GovernanceRequirement(
                requirement_code="SOC2_CC6.1",
                framework_code="SOC2_TYPE_II",
                title="Logical Access Security & Identification",
                description="The entity implements logical access security software, infrastructure, and architectures over protected information assets.",
                category="ACCESS_CONTROL",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="SOC2_CC6.3",
                framework_code="SOC2_TYPE_II",
                title="Role-Based Least Privilege Authorization",
                description="The entity authorizes, modifies, or removes access based on roles, least privilege, and segregation of duties.",
                category="AUTHORIZATION",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="SOC2_CC6.8",
                framework_code="SOC2_TYPE_II",
                title="Unauthorized & Malicious Code Detection",
                description="The entity implements controls to prevent or detect and act upon the introduction of unauthorized or malicious code/actions.",
                category="THREAT_DETECTION",
                priority="HIGH",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="SOC2_A1.2",
                framework_code="SOC2_TYPE_II",
                title="Environmental & Disaster Recovery Backups",
                description="The entity authorizes, designs, develops, implements, operates, and monitors recovery processes to meet availability objectives.",
                category="RESILIENCE",
                priority="HIGH",
                status=RequirementStatus.IMPLEMENTED
            ),
        ])

        # 2. ISO/IEC 27001:2022
        iso27001 = GovernanceFramework(
            framework_code="ISO_27001_2022",
            name="ISO/IEC 27001:2022 Information Security Management",
            version="2022",
            category=FrameworkCategory.INFORMATION_SECURITY,
            description="International standard for managing information security risks systematically.",
            owner="ciso",
        )
        self.register_framework(iso27001)
        self.register_requirements("ISO_27001_2022", [
            GovernanceRequirement(
                requirement_code="ISO_A.5.15",
                framework_code="ISO_27001_2022",
                title="Access Control Policy & Enforcement",
                description="Rules to control physical and logical access to information and other associated assets shall be established and enforced.",
                category="IDENTITY_AND_ACCESS",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="ISO_A.8.24",
                framework_code="ISO_27001_2022",
                title="Use of Cryptography & Key Management",
                description="Rules for the effective use of cryptography, including cryptographic key management, shall be defined and implemented.",
                category="CRYPTOGRAPHY",
                priority="HIGH",
                status=RequirementStatus.IMPLEMENTED
            ),
        ])

        # 3. NIST AI Risk Management Framework 1.0
        nist_ai = GovernanceFramework(
            framework_code="NIST_AI_RMF_1.0",
            name="NIST AI Risk Management Framework",
            version="1.0",
            category=FrameworkCategory.AI_GOVERNANCE,
            description="Guidance for managing risks in the design, development, use, and evaluation of AI systems.",
            owner="ai_governance_lead",
        )
        self.register_framework(nist_ai)
        self.register_requirements("NIST_AI_RMF_1.0", [
            GovernanceRequirement(
                requirement_code="NIST_AI_GOVERN_1.1",
                framework_code="NIST_AI_RMF_1.0",
                title="Legal & Regulatory AI Compliance Boundaries",
                description="Legal and regulatory requirements involving AI are identified and mapped to operational system guardrails.",
                category="AI_SAFETY",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="NIST_AI_MANAGE_1.3",
                framework_code="NIST_AI_RMF_1.0",
                title="Human-in-the-Loop Oversight for High-Impact Actions",
                description="Mechanisms are in place to ensure human agency and authorization for high-impact AI agent actions.",
                category="HUMAN_OVERSIGHT",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
        ])

        # 4. GDPR (General Data Protection Regulation)
        gdpr = GovernanceFramework(
            framework_code="GDPR",
            name="General Data Protection Regulation (EU) 2016/679",
            version="2016/679",
            category=FrameworkCategory.PRIVACY,
            jurisdiction="EU",
            description="Protection of natural persons with regard to the processing of personal data and on the free movement of such data.",
            owner="dpo_lead",
        )
        self.register_framework(gdpr)
        self.register_requirements("GDPR", [
            GovernanceRequirement(
                requirement_code="GDPR_ART_5.1.c",
                framework_code="GDPR",
                title="Data Minimization Principle",
                description="Personal data shall be adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed.",
                category="PRIVACY_MINIMIZATION",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="GDPR_ART_17",
                framework_code="GDPR",
                title="Right to Erasure ('Right to be Forgotten')",
                description="The data subject shall have the right to obtain from the controller the erasure of personal data without undue delay.",
                category="DATA_SUBJECT_RIGHTS",
                priority="HIGH",
                status=RequirementStatus.IMPLEMENTED
            ),
            GovernanceRequirement(
                requirement_code="GDPR_ART_32",
                framework_code="GDPR",
                title="Security of Processing & Tenant Confidentiality",
                description="Implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.",
                category="TECHNICAL_SECURITY",
                priority="CRITICAL",
                status=RequirementStatus.IMPLEMENTED
            ),
        ])

    def register_framework(self, framework: GovernanceFramework) -> None:
        self._frameworks[framework.framework_code] = framework

    def register_requirements(self, framework_code: str, requirements: List[GovernanceRequirement]) -> None:
        if framework_code not in self._requirements:
            self._requirements[framework_code] = []
        self._requirements[framework_code].extend(requirements)

    def get_framework(self, framework_code: str) -> Optional[GovernanceFramework]:
        return self._frameworks.get(framework_code)

    def list_frameworks(self) -> List[GovernanceFramework]:
        return list(self._frameworks.values())

    def get_requirements(self, framework_code: str) -> List[GovernanceRequirement]:
        return self._requirements.get(framework_code, [])

    def get_requirement(self, framework_code: str, requirement_code: str) -> Optional[GovernanceRequirement]:
        reqs = self.get_requirements(framework_code)
        for r in reqs:
            if r.requirement_code == requirement_code:
                return r
        return None
