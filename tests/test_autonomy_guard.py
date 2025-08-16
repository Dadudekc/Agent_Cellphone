import time

from src.core.autonomy_guard import enforce


def test_enforce_triggers_recovery_on_stall():
    autopolicy = {"probe_timeout_ms": 20}
    recovered = {"called": False}

    def stalled_operation(signal_progress):
        # No progress is signalled; sleep longer than the timeout
        time.sleep(0.05)

    def recover():
        recovered["called"] = True

    enforce(stalled_operation, autopolicy, recover)

    assert recovered["called"], "Recovery action was not triggered for stalled operation"
