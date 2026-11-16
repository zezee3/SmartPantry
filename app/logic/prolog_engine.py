"""Adapter that asks SWI-Prolog to classify pantry item dates."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from app.services.functional_rules import fallback_classification


@dataclass(frozen=True)
class LogicResult:
    status: str
    priority: str
    engine: str


class PrologEngine:
    """Runs Prolog rules when SWI-Prolog is available, otherwise uses a fallback."""

    def __init__(self, rules_path=None, executable=None):
        self.rules_path = Path(
            rules_path or Path(__file__).with_name("pantry_rules.pl")
        )
        self.executable = executable or shutil.which("swipl")

    @property
    def engine_name(self):
        return "SWI-Prolog" if self.executable else "Python fallback"

    def classify_many(self, day_values):
        if not day_values:
            return []
        if not self.executable:
            return [self._fallback_result(days) for days in day_values]

        arguments = ["none" if days is None else str(int(days)) for days in day_values]
        command = [
            self.executable,
            "-q",
            "-s",
            str(self.rules_path),
            "--",
            *arguments,
        ]

        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
            if len(lines) != len(day_values):
                return [self._fallback_result(days) for days in day_values]

            results = []
            for line in lines:
                parts = line.split("|")
                if len(parts) != 2:
                    return [self._fallback_result(days) for days in day_values]
                results.append(LogicResult(parts[0], parts[1], "SWI-Prolog"))
            return results
        except (OSError, subprocess.SubprocessError):
            return [self._fallback_result(days) for days in day_values]

    @staticmethod
    def _fallback_result(days):
        status, priority = fallback_classification(days)
        return LogicResult(status, priority, "Python fallback")
