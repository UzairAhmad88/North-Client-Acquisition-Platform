"""Bounded retry strategy with exponential backoff and jitter calculations."""

import math
import random
from typing import Optional


class RetryPolicy:
    """Configurable retry policy calculating bounded delay backoff."""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_backoff_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
        max_backoff_seconds: float = 60.0,
        jitter: bool = True,
    ):
        self.max_attempts = max_attempts
        self.initial_backoff_seconds = initial_backoff_seconds
        self.backoff_multiplier = backoff_multiplier
        self.max_backoff_seconds = max_backoff_seconds
        self.jitter = jitter

    def should_retry(self, current_attempt: int) -> bool:
        """Determine if an operation should be retried given current attempt count."""
        return current_attempt < self.max_attempts

    def compute_backoff_seconds(self, current_attempt: int) -> float:
        """Calculate the exponential delay for next retry attempt with optional jitter."""
        if current_attempt <= 0:
            return 0.0

        backoff = self.initial_backoff_seconds * math.pow(
            self.backoff_multiplier, current_attempt - 1
        )
        backoff = min(backoff, self.max_backoff_seconds)

        if self.jitter:
            # Full jitter: random between 0 and computed backoff
            backoff = random.uniform(0.5 * backoff, backoff)

        return round(backoff, 2)
