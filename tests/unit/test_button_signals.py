import os
import pytest


@pytest.fixture(autouse=True)
def _offscreen_qt():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    yield


def test_button_emits_signal_and_slot():
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
        from PyQt5.QtTest import QTest, QSignalSpy
        from PyQt5.QtCore import Qt
    except Exception as e:  # pragma: no cover - PyQt5 optional
        pytest.skip(f"PyQt5 not available: {e}")

    app = QApplication.instance() or QApplication([])

    class Demo(QWidget):
        def __init__(self):
            super().__init__()
            self.button = QPushButton("Test")
            layout = QVBoxLayout(self)
            layout.addWidget(self.button)
            self.triggered = False
            self.button.clicked.connect(self.on_clicked)

        def on_clicked(self):
            self.triggered = True

    widget = Demo()
    widget.show()

    spy = QSignalSpy(widget.button.clicked)
    QTest.mouseClick(widget.button, Qt.LeftButton)

    assert len(spy) == 1
    assert widget.triggered
