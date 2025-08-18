import threading

from src.core.autonomy_guard import enforce


def test_enforce_triggers_recovery_on_stall():
    autopolicy = {"probe_timeout_ms": 20}
    recovered = {"called": False}

    done = threading.Event()

    def stalled_operation(signal_progress):
        # Wait until recovery signals completion
        done.wait(timeout=1)

    def recover():
        recovered["called"] = True
        done.set()

    enforce(stalled_operation, autopolicy, recover)

    assert recovered["called"], "Recovery action was not triggered for stalled operation"
