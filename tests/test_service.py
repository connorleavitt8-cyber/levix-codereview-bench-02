import unittest
from taskflow.store import TaskStore
from taskflow.service import TaskService
from taskflow.models import Priority


class TaskServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = TaskService(TaskStore(":memory:"))

    def test_add_and_open(self):
        self.svc.add_task("write spec", Priority.HIGH)
        self.assertEqual(len(self.svc.open_tasks()), 1)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.svc.add_task("   ")

    def test_by_priority_order(self):
        self.svc.add_task("low", Priority.LOW)
        self.svc.add_task("high", Priority.HIGH)
        order = [t.priority for t in self.svc.by_priority()]
        self.assertEqual(order[0], Priority.HIGH)
