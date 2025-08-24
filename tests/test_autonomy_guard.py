import time

from src.core.autonomy_guard import enforce


def test_enforce_triggers_recovery_on_stall():
    autopolicy = {"probe_timeout_ms": 20}
    recovered = {"called": False}

    def stalled_operation(signal_progress):
        # Busy-wait without signalling progress to exceed the timeout
        end = time.monotonic() + 0.05
        while time.monotonic() < end:
            pass

    def recover():
        recovered["called"] = True

    enforce(stalled_operation, autopolicy, recover)

    assert recovered["called"], "Recovery action was not triggered for stalled operation"
