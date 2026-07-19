from __future__ import annotations
from datetime import date, timedelta
from taskflow.models import Task, Priority
from taskflow.store import TaskStore


class TaskService:
    """High-level task operations."""

    def __init__(self, store: TaskStore):
        self.store = store

    def add_task(self, title: str, priority: Priority = Priority.MEDIUM, due: str | None = None) -> int:
        if not title.strip():
            raise ValueError("title must not be empty")
        return self.store.add(title, priority, due)

    def open_tasks(self) -> list[Task]:
        return [t for t in self.store.all() if not t.done]

    def by_priority(self) -> list[Task]:
        return sorted(self.store.all(), key=lambda t: t.priority, reverse=True)

    def due_soon(self, within_days: int = 3) -> list[Task]:
        """Return open tasks due within the next `within_days` days."""
        today = date.today()
        cutoff = today + timedelta(days=within_days)
        result = []
        for t in self.open_tasks():
            if t.due and t.due > today and t.due > cutoff:
                result.append(t)
        return result
