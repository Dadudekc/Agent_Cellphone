from threading import Event

from src.core.utils.watchdog import Watchdog


def test_watchdog_alerts_on_failure():
    alerts: list[str] = []
    done = Event()

    def check():
        raise RuntimeError("fail")

    def alert(exc: BaseException) -> None:
        alerts.append(str(exc))
        done.set()

    wd = Watchdog(0.01, check, alert)
    wd.start()
    assert done.wait(timeout=0.3), "Watchdog did not report failure"
    wd.stop()
    assert alerts, "Watchdog did not report failure"
