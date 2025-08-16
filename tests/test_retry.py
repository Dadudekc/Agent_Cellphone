from src.core.utils.retry import retry


def test_retry_succeeds_after_failures():
    calls = {"count": 0}

    @retry(retries=2, delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("fail")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 2


def test_retry_raises_after_exhaustion():
    @retry(retries=1, delay=0)
    def always_fail():
        raise RuntimeError("fail")

    try:
        always_fail()
    except RuntimeError:
        pass
    else:
        assert False, "RuntimeError not raised"
