import time

from src.core.utils.watchdog import Watchdog


def test_watchdog_alerts_on_failure():
    alerts: list[str] = []

    def check():
        raise RuntimeError("fail")

    def alert(exc: BaseException) -> None:
        alerts.append(str(exc))

    wd = Watchdog(0.05, check, alert)
    wd.start()
    time.sleep(0.2)
    wd.stop()
    assert alerts, "Watchdog did not report failure"
