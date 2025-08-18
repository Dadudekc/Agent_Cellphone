import threading

from src.core.utils.watchdog import Watchdog


def test_watchdog_alerts_on_failure():
    alerts: list[str] = []

    def check():
        raise RuntimeError("fail")

    triggered = threading.Event()

    def alert(exc: BaseException) -> None:
        alerts.append(str(exc))
        triggered.set()

    wd = Watchdog(0.01, check, alert)
    wd.start()
    assert triggered.wait(timeout=1), "Watchdog did not report failure in time"
    wd.stop()
    assert alerts, "Watchdog did not report failure"
