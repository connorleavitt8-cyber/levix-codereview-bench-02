from __future__ import annotations
import argparse
from taskflow.store import TaskStore
from taskflow.service import TaskService
from taskflow.models import Priority


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="TaskFlow CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_p = sub.add_parser("add")
    add_p.add_argument("title")
    add_p.add_argument("--priority", type=int, default=2)
    sub.add_parser("list")
    args = parser.parse_args(argv)

    svc = TaskService(TaskStore("tasks.db"))
    if args.cmd == "add":
        tid = svc.add_task(args.title, Priority(args.priority))
        print(f"added task {tid}")
    elif args.cmd == "list":
        for t in svc.by_priority():
            mark = "x" if t.done else " "
            print(f"[{mark}] {t.id} {t.title} (P{int(t.priority)})")


if __name__ == "__main__":
    main()
