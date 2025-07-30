"""Pytest plugin for generating Xray JSON reports."""

import base64
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest


class XrayReporter:
    """Pytest plugin that generates Xray JSON reports."""

    def __init__(self, config: pytest.Config) -> None:
        self.config = config
        self.results: Dict[str, Any] = {
            "tests": [],
            "info": {
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "skipped": 0,
                    "duration": 0.0,
                },
                "testEnvironments": [],
                "project": None,
                "testPlanKey": None,
                "testExecutionKey": None,
            },
        }
        self.start_time = datetime.now(timezone.utc)
        self._current_test: Optional[Dict[str, Any]] = None
        self.marker_reasons: Dict[str, List[Dict[str, str]]] = {}  # nodeid -> list of marker info
        self.test_key = config.getoption("--xray-test-key")
        if not self.test_key:
            import warnings

            warnings.warn(
                "No Xray test key provided. Using test function name as test key. "
                "Results may not be properly linked in Jira Xray.",
                UserWarning,
                stacklevel=2,
            )

    def pytest_runtest_logstart(self, nodeid: str) -> None:
        """Record test start time."""
        # Use provided test key or fall back to test name
        test_key = self.test_key or nodeid.split("::")[-1]

        self._current_test = {
            "testKey": test_key,
            "start": datetime.now(timezone.utc).isoformat(),
            "evidence": [],
            "steps": [],
            "defects": [],
            "customFields": [{"id": "test_path", "name": "Test Path", "value": nodeid}],
        }
        # Add marker reasons if present
        for marker_info in self.marker_reasons.get(nodeid, []):
            self._current_test["customFields"].append(marker_info)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """Process test results and collect evidence."""
        if report.when == "call" or (report.when == "setup" and report.outcome == "skipped"):
            if not self._current_test:
                return

            # Get captured output
            evidence: List[Dict[str, str]] = []

            # Add stdout if present
            if report.capstdout:
                evidence.append(
                    {
                        "data": base64.b64encode(report.capstdout.encode()).decode(),
                        "filename": "stdout.txt",
                        "contentType": "text/plain",
                    }
                )

            # Add stderr if present
            if report.capstderr:
                evidence.append(
                    {
                        "data": base64.b64encode(report.capstderr.encode()).decode(),
                        "filename": "stderr.txt",
                        "contentType": "text/plain",
                    }
                )

            # Add stack trace for failures/errors
            if report.longrepr:
                evidence.append(
                    {
                        "data": base64.b64encode(str(report.longrepr).encode()).decode(),
                        "filename": "stacktrace.txt",
                        "contentType": "text/plain",
                    }
                )

            # Add captured log if available
            if hasattr(report, "caplog"):
                evidence.append(
                    {
                        "data": base64.b64encode(report.caplog.encode()).decode(),
                        "filename": "test.log",
                        "contentType": "text/plain",
                    }
                )

            # Calculate test duration
            finish_time = datetime.now(timezone.utc)
            duration = (finish_time - self.start_time).total_seconds()

            # Add test metadata
            if hasattr(report, "keywords"):
                for marker in report.keywords:
                    # Skip empty markers and internal pytest markers
                    if (
                        not marker
                        or marker.startswith("test_")
                        or marker
                        in ["pytestmark", "pytest-xray-reporter", "tests", "skip", "xfail"]
                    ):
                        continue

                    # Get marker value and arguments
                    marker_obj = report.keywords[marker]
                    print(f"DEBUG: Marker {marker}: {marker_obj}")  # Debug print
                    print(f"DEBUG: Marker type: {type(marker_obj)}")  # Debug print
                    print(f"DEBUG: Marker dir: {dir(marker_obj)}")  # Debug print

                    if hasattr(marker_obj, "args") and marker_obj.args:
                        value = str(marker_obj.args[0])
                        print(f"DEBUG: Using args[0]: {value}")  # Debug print
                    elif hasattr(marker_obj, "kwargs") and "reason" in marker_obj.kwargs:
                        value = str(marker_obj.kwargs["reason"])
                        print(f"DEBUG: Using kwargs['reason']: {value}")  # Debug print
                    else:
                        value = str(marker_obj)
                        print(f"DEBUG: Using str(marker_obj): {value}")  # Debug print

                    # Only add markers that have meaningful values
                    if value and value != "1":
                        # Convert marker to a more readable name
                        # e.g., "xfail" -> "Expected Failure"
                        name = marker.replace("_", " ").title()
                        self._current_test["customFields"].append(
                            {"id": marker, "name": name, "value": value}
                        )

            # Create test result in Xray format
            self._current_test.update(
                {
                    "finish": finish_time.isoformat(),
                    "status": self._get_status(report.outcome),
                    "comment": str(report.longrepr) if report.longrepr else "",
                    "evidence": evidence,
                    "duration": duration,
                }
            )

            self.results["tests"].append(self._current_test)

            # Update summary
            self.results["info"]["summary"]["total"] += 1
            if report.outcome == "passed":
                self.results["info"]["summary"]["passed"] += 1
            elif report.outcome == "failed":
                self.results["info"]["summary"]["failed"] += 1
            elif report.outcome == "error":
                self.results["info"]["summary"]["errors"] += 1
            elif report.outcome == "skipped":
                self.results["info"]["summary"]["skipped"] += 1

            # Update duration
            self.results["info"]["summary"]["duration"] += duration

            # Reset current test
            self._current_test = None

    def _get_status(self, outcome: str) -> str:
        """Convert pytest outcome to Xray status."""
        return {"passed": "PASSED", "failed": "FAILED", "error": "ERROR", "skipped": "SKIPPED"}.get(
            outcome, "UNKNOWN"
        )

    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        """Write results to file when test session ends."""
        # Add test environment info
        self.results["info"]["testEnvironments"] = [
            platform.system(),
            platform.release(),
            platform.python_version(),
        ]

        # Get optional info from config
        self.results["info"].update(
            {
                "project": self.config.getoption("--xray-project", default=None),
                "testPlanKey": self.config.getoption("--xray-test-plan", default=None),
                "testExecutionKey": self.config.getoption("--xray-test-execution", default=None),
            }
        )

        output_file = self.config.getoption("--xray-output")
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(self.results, f, indent=2)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options."""
    parser.addoption(
        "--xray-output",
        action="store",
        default="xray-report.json",
        help="Output file for Xray JSON report",
    )
    parser.addoption(
        "--xray-project",
        action="store",
        help="Xray project key",
    )
    parser.addoption(
        "--xray-test-plan",
        action="store",
        help="Xray test plan key",
    )
    parser.addoption(
        "--xray-test-execution",
        action="store",
        help="Xray test execution key",
    )
    parser.addoption(
        "--xray-test-key",
        action="store",
        help="Xray test key to use for all tests (if not provided, uses test function name)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure the plugin."""
    if config.getoption("--xray-output"):
        reporter = XrayReporter(config)
        config.pluginmanager.register(reporter)


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: List[pytest.Item],
) -> None:
    reporter = config.pluginmanager.getplugin("xray-reporter")
    if not hasattr(reporter, "marker_reasons"):
        return
    for item in items:
        nodeid = item.nodeid
        for marker in item.iter_markers():
            if marker.name in ("skip", "xfail") and "reason" in marker.kwargs:
                if nodeid not in reporter.marker_reasons:
                    reporter.marker_reasons[nodeid] = []
                reporter.marker_reasons[nodeid].append(
                    {
                        "id": marker.name,
                        "name": marker.name.title(),
                        "value": marker.kwargs["reason"],
                    }
                )
