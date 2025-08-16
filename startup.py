#!/usr/bin/env python3
"""Unified startup script for the Agent Cell Phone project.

The script performs basic configuration validation before handing off
control to the main application logic. Additional initialization steps
can be added here in the future to keep startup consistent across
environments.
"""

from src.config_validator import validate_config
from src.core.utils.retry import retry


@retry(retries=3, delay=1.0, exceptions=(Exception,), timeout=5)
def _validated_startup() -> None:
    """Validate configuration with automatic retries."""
    validate_config()


def main() -> None:
    """Run the startup sequence."""
    try:
        _validated_startup()
        print("Startup sequence completed. Configuration is valid.")
    except Exception as exc:  # pragma: no cover - startup diagnostics
        print(f"Startup failed: {exc}")


if __name__ == "__main__":
    main()
