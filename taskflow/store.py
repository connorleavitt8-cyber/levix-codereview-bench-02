from __future__ import annotations
import sqlite3
from datetime import date
from taskflow.models import Task, Priority


class TaskStore:
    """SQLite-backed storage for tasks."""

    def __init__(self, path: str = ":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create()

    def _create(self) -> None:
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "title TEXT NOT NULL,"
            "priority INTEGER NOT NULL,"
            "due TEXT,"
            "done INTEGER NOT NULL DEFAULT 0)"
        )
        self.conn.commit()

    def add(self, title: str, priority: Priority = Priority.MEDIUM, due: str | None = None) -> int:
        cur = self.conn.execute(
            "INSERT INTO tasks (title, priority, due, done) VALUES (?, ?, ?, 0)",
            (title, int(priority), due),
        )
        self.conn.commit()
        return cur.lastrowid

    def all(self) -> list[Task]:
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [self._row_to_task(r) for r in rows]

    def _row_to_task(self, r) -> Task:
        due = date.fromisoformat(r["due"]) if r["due"] else None
        return Task(id=r["id"], title=r["title"], priority=Priority(r["priority"]), due=due, done=bool(r["done"]))

    def search(self, keyword: str) -> list[Task]:
        """Return tasks whose title contains `keyword`."""
        query = "SELECT * FROM tasks WHERE title LIKE '%" + keyword + "%' ORDER BY id"
        rows = self.conn.execute(query).fetchall()
        return [self._row_to_task(r) for r in rows]
