"""Central Command Registry for Global Command Palette."""

from typing import Dict, List, Optional
from app.command.base import CommandCategory, CommandDefinition, CommandRiskLevel


class CommandRegistry:
    """Registry maintaining authorized command specifications across the platform."""

    def __init__(self):
        self._commands: Dict[str, CommandDefinition] = {}
        self._register_default_commands()

    def register(self, definition: CommandDefinition) -> None:
        """Register a command definition."""
        self._commands[definition.command_id] = definition

    def get(self, command_id: str) -> Optional[CommandDefinition]:
        """Look up a command by its identifier."""
        return self._commands.get(command_id)

    def list_commands(self) -> List[CommandDefinition]:
        """Return all registered commands."""
        return list(self._commands.values())

    def _register_default_commands(self) -> None:
        """Initialize built-in platform commands."""

        # 1. Navigation Commands (Low risk)
        self.register(CommandDefinition(
            command_id="NAV_LEADS",
            name="Go to Leads",
            description="Open Leads CRM Directory",
            category=CommandCategory.NAVIGATION,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"url": "/leads"},
        ))
        self.register(CommandDefinition(
            command_id="NAV_PROJECTS",
            name="Go to Projects",
            description="Open Projects Delivery Management",
            category=CommandCategory.NAVIGATION,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"url": "/projects"},
        ))
        self.register(CommandDefinition(
            command_id="NAV_INBOX",
            name="Open Inbox",
            description="View Unified Notifications & Messages",
            category=CommandCategory.NAVIGATION,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"url": "/inbox"},
        ))
        self.register(CommandDefinition(
            command_id="NAV_APPROVALS",
            name="Open Approvals",
            description="View Pending Approvals Queue",
            category=CommandCategory.NAVIGATION,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"url": "/approvals"},
        ))

        # 2. Query Commands (Low risk)
        self.register(CommandDefinition(
            command_id="QUERY_LEADS",
            name="Find Qualified Leads",
            description="Search leads with high potential",
            category=CommandCategory.QUERY,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"status": "QUALIFIED"},
        ))
        self.register(CommandDefinition(
            command_id="QUERY_PROJECTS_AT_RISK",
            name="Find At-Risk Projects",
            description="Search projects flagged as AT_RISK or BLOCKED",
            category=CommandCategory.QUERY,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"status": "AT_RISK"},
        ))

        # 3. Safe Create Commands (Medium risk, confirmation required)
        self.register(CommandDefinition(
            command_id="CREATE_TASK",
            name="Create Project Task",
            description="Create a new task in a project",
            category=CommandCategory.SAFE_CREATE,
            risk_level=CommandRiskLevel.MEDIUM,
            required_permission="TASK_CREATE",
            requires_confirmation=True,
            parameters_schema={"title": "str", "project_id": "str"},
        ))
        self.register(CommandDefinition(
            command_id="CREATE_NOTE",
            name="Create Internal Note",
            description="Add an internal discussion note",
            category=CommandCategory.SAFE_CREATE,
            risk_level=CommandRiskLevel.LOW,
            parameters_schema={"content": "str"},
        ))

        # 4. Sensitive Action Commands (High/Critical risk, human approval required)
        self.register(CommandDefinition(
            command_id="SEND_PROPOSAL",
            name="Send Proposal to Client",
            description="Dispatch proposal via Communication Guard to client",
            category=CommandCategory.SENSITIVE_ACTION,
            risk_level=CommandRiskLevel.HIGH,
            required_permission="PROPOSAL_SEND",
            requires_confirmation=True,
            requires_approval=True,
            parameters_schema={"proposal_id": "str", "recipient_id": "str"},
        ))
        self.register(CommandDefinition(
            command_id="APPROVE_CONTRACT",
            name="Approve Contract Terms",
            description="Formally sign off on contract baseline",
            category=CommandCategory.SENSITIVE_ACTION,
            risk_level=CommandRiskLevel.CRITICAL,
            required_permission="CONTRACT_APPROVE",
            requires_confirmation=True,
            requires_approval=True,
            parameters_schema={"contract_id": "str"},
        ))
        self.register(CommandDefinition(
            command_id="RETRY_WORKFLOW",
            name="Retry Failed Workflow",
            description="Trigger replay on dead-letter or failed workflow instance",
            category=CommandCategory.SENSITIVE_ACTION,
            risk_level=CommandRiskLevel.MEDIUM,
            required_permission="WORKFLOW_MANAGE",
            requires_confirmation=True,
            parameters_schema={"workflow_id": "str"},
        ))


global_command_registry = CommandRegistry()
