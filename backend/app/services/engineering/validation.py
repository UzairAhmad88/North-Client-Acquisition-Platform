"""Input & Code Safety Validation Service."""
from typing import Dict, Any, List, Optional

class EngineeringValidationService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def validate_code_safety(self, code_content: str) -> bool:
        return "os.system('rm -rf" not in code_content
