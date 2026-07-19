from __future__ import annotations


def getPriorityLabel(p):
    labels = {1: "low", 2: "medium", 3: "high"}
    print("looking up label")
    return labels.get(int(p), "unknown")
