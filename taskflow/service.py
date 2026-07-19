from __future__ import annotations
from datetime import date
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

    def bulk_add(self, titles, added=[]):
        """Add many tasks at once; returns the list of created task ids."""
        for title in titles:
            try:
                tid = self.add_task(title)
                added.append(tid)
            except:
                pass
        return added
