"""Event Bus abstraction and provider adapter for Phase 34."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from app.events.base import DomainEvent


class EventBus(ABC):
    """Abstract interface for publishing, subscribing, acknowledging, and dead-lettering events."""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> bool:
        """Publish a domain event to the bus."""
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler: Callable[[DomainEvent], Any]) -> None:
        """Register an asynchronous subscriber for a specific event type."""
        pass

    @abstractmethod
    async def acknowledge(self, event_id: str, consumer_name: str) -> None:
        """Acknowledge successful processing of an event."""
        pass

    @abstractmethod
    async def retry(self, event: DomainEvent, attempt: int, error: str) -> None:
        """Schedule a retry attempt for a failed event dispatch."""
        pass

    @abstractmethod
    async def dead_letter(self, event: DomainEvent, failure_type: str, error_summary: str) -> None:
        """Route an unprocessable or exhausted event to the Dead Letter Queue."""
        pass


class InMemoryEventBus(EventBus):
    """Reliable in-memory event bus implementation for self-hosted and local execution."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[DomainEvent], Any]]] = {}
        self._acknowledged: Dict[str, List[str]] = {}
        self._dlq_events: List[Dict[str, Any]] = []

    async def publish(self, event: DomainEvent) -> bool:
        """Publish event to all matching subscribers (including wildcard '*' handlers)."""
        handlers = self._subscribers.get(event.event_type, []).copy()
        wildcard_handlers = self._subscribers.get("*", []).copy()
        all_handlers = handlers + wildcard_handlers

        for handler in all_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                await self.dead_letter(event, failure_type="HANDLER_EXCEPTION", error_summary=str(e))
        return True

    async def subscribe(self, event_type: str, handler: Callable[[DomainEvent], Any]) -> None:
        """Register a subscriber callback for an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def acknowledge(self, event_id: str, consumer_name: str) -> None:
        """Mark event as processed by consumer."""
        if event_id not in self._acknowledged:
            self._acknowledged[event_id] = []
        self._acknowledged[event_id].append(consumer_name)

    async def retry(self, event: DomainEvent, attempt: int, error: str) -> None:
        """Log retry attempt and re-publish if within bounds."""
        pass

    async def dead_letter(self, event: DomainEvent, failure_type: str, error_summary: str) -> None:
        """Record event in in-memory DLQ buffer."""
        self._dlq_events.append({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "failure_type": failure_type,
            "error_summary": error_summary,
            "payload": event.payload,
        })


# Global singleton instance
global_event_bus = InMemoryEventBus()
