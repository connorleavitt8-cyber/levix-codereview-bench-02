# TaskFlow

A tiny task manager (SQLite + stdlib only). Used as a standardized code-review
test bench for Levix Labs Open Audits.

```bash
python -m taskflow.cli add "write the spec" --priority 3
python -m taskflow.cli list
python -m unittest discover -s tests
```
