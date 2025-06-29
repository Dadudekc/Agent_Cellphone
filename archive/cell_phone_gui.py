#!/usr/bin/env python3
"""
Dream.OS Cell Phone – Qt GUI
------------------------------------------------------------
• Visual controller for Agent Cell Phone backend
• 3 tabs: Controls │ Messaging │ Status
• Requires: PyQt5  (pip install pyqt5 pyqt5-qt5)
"""

from __future__ import annotations
import sys, json, logging, asyncio
from functools        import partial
from pathlib          import Path
from PyQt5.QtWidgets  import (
    QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout,
    QHBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui      import QIcon
from PyQt5.QtCore     import Qt, QTimer

# ─────────────────── backend bridge
# REPO_ROOT   = Path(__file__).resolve().parents[1]
# sys.path.append(str(REPO_ROOT / "src"))        # adjust if layout differs
from agent_cell_phone import AgentCellPhone, MsgTag     # noqa: E402

log = logging.getLogger("cell_phone_gui")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ─────────────────── GUI
class CellPhoneGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Dream.OS Cell Phone")
        self.resize(980, 560)
        self.phone   = AgentCellPhone()              # backend instance
        self.agents  = sorted(self.phone._coords)    # agent id list

        self._build_ui()

    # ─────────────────── UI builders
    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        root    = QVBoxLayout(central)

        # Header ----------------------------------------------------------------
        header = QHBoxLayout()
        title  = QLabel("📱  <b>Dream.OS Cell Phone</b>")
        title.setStyleSheet("font-size:22px;color:#4ddb71;")
        header.addWidget(title); header.addStretch()

        header.addWidget(QLabel("<b>Select Agent:</b>"))
        self.agent_combo = QComboBox()
        self.agent_combo.addItems(self.agents)
        header.addWidget(self.agent_combo)
        root.addLayout(header)

        # Tabs ------------------------------------------------------------------
        tabs = QTabWidget(); root.addWidget(tabs)
        tabs.addTab(self._build_controls_tab(),  "Controls")
        tabs.addTab(self._build_message_tab(),   "Messaging")
        tabs.addTab(self._build_status_tab(),    "Status")

        # Status bar ------------------------------------------------------------
        self.statusBar().showMessage(f"Connected to {len(self.agents)} agents: {', '.join(self.agents)}")

    # controls tab ──────────────────────────────────────────────────────────────
    def _build_controls_tab(self) -> QWidget:
        w = QWidget(); g = QVBoxLayout(w)

        # individual -----------------------------------------------------------
        indiv_box = self._group("Individual Agent Controls")
        indiv_lay = indiv_box.layout()
        self._btn(indiv_lay,"Send Resume",lambda:self._act_ind(MsgTag.RESUME))
        self._btn(indiv_lay,"Sync Status",lambda:self._act_ind(MsgTag.SYNC))
        self._btn(indiv_lay,"Pause Agent",lambda:self._act_ind("Pause…", MsgTag.NORMAL))
        self._btn(indiv_lay,"Resume Agent",lambda:self._act_ind("Resume…", MsgTag.NORMAL))
        self._btn(indiv_lay,"Get Status",lambda:self._act_ind("Report status", MsgTag.VERIFY))
        self._btn(indiv_lay,"Ping Agent",lambda:self._act_ind("Ping", MsgTag.NORMAL))
        self._btn(indiv_lay,"Assign Task",lambda:self._act_ind("Awaiting task", MsgTag.TASK))
        self._btn(indiv_lay,"Emergency Stop",lambda:self._act_ind("EMERGENCY STOP", MsgTag.REPAIR), danger=True)
        g.addWidget(indiv_box)

        # broadcast ------------------------------------------------------------
        bc_box = self._group("Broadcast Controls")
        bc_lay = bc_box.layout()
        self._btn(bc_lay,"Broadcast Resume",partial(self._broadcast, MsgTag.RESUME))
        self._btn(bc_lay,"Broadcast Sync",partial(self._broadcast, MsgTag.SYNC))
        self._btn(bc_lay,"Broadcast Pause",partial(self._broadcast, MsgTag.RESTORE))
        self._btn(bc_lay,"Broadcast Task",partial(self._broadcast, MsgTag.TASK))
        self._btn(bc_lay,"Broadcast Ping",partial(self._broadcast, MsgTag.NORMAL,"Ping"))
        self._btn(bc_lay,"Emergency Broadcast",partial(self._broadcast, MsgTag.REPAIR,"EMERGENCY STOP"), danger=True)
        g.addWidget(bc_box)

        # quick actions --------------------------------------------------------
        quick = self._group("Quick Actions"); ql=quick.layout()
        self._btn(ql,"Start All Agents",partial(self._broadcast, MsgTag.RESUME))
        self._btn(ql,"Stop All Agents",partial(self._broadcast, MsgTag.REPAIR,"Stop immediately"), danger=True)
        self._btn(ql,"Restart All",partial(self._broadcast, MsgTag.RESTORE,"Restart sequence"))
        g.addWidget(quick); g.addStretch()
        return w

    # messaging tab ─────────────────────────────────────────────────────────────
    def _build_message_tab(self) -> QWidget:
        w = QWidget(); g = QVBoxLayout(w)

        # sender row
        send_grp = self._group("Send Message"); sg = send_grp.layout()
        self.msg_type = QComboBox(); self.msg_type.addItems([e.name.title() for e in MsgTag])
        self.msg_edit = QLineEdit(); self.msg_edit.setPlaceholderText("Enter your message here…")
        send_btn = QPushButton("📤 Send"); send_btn.clicked.connect(self._send_custom)
        sg.addWidget(QLabel("Message Type:")); sg.addWidget(self.msg_type); sg.addWidget(self.msg_edit); sg.addWidget(send_btn)
        g.addWidget(send_grp)

        # history
        hist_grp = self._group("Message History"); hg = QVBoxLayout()
        hist_grp.setLayout(hg)
        self.history = QTextEdit(); self.history.setReadOnly(True)
        hg.addWidget(self.history)
        row = QHBoxLayout()
        refresh = QPushButton("🔄 Refresh"); refresh.clicked.connect(self._refresh_history)
        clear   = QPushButton("🗑️ Clear");   clear.clicked.connect(self.history.clear)
        row.addWidget(refresh); row.addWidget(clear); row.addStretch()
        hg.addLayout(row)
        g.addWidget(hist_grp); g.addStretch()
        return w

    # status tab ────────────────────────────────────────────────────────────────
    def _build_status_tab(self) -> QWidget:
        w = QWidget(); g = QVBoxLayout(w)

        # system status
        sys_grp = self._group("System Status", QVBoxLayout); sl = sys_grp.layout()
        self.sys_status = QTextEdit(); self.sys_status.setReadOnly(True)
        sl.addWidget(self.sys_status)
        row = QHBoxLayout()
        ref = QPushButton("🔄 Refresh Status"); ref.clicked.connect(self._refresh_status)
        det = QPushButton("📑 Detailed Report"); det.clicked.connect(lambda:self._log("Detailed report requested"))
        row.addWidget(ref); row.addWidget(det); row.addStretch()
        sl.addLayout(row)
        g.addWidget(sys_grp)

        # agent grid
        grid_grp = self._group("Agent Status Grid"); gl = grid_grp.layout()
        self.agent_tiles = {}
        for i, agent in enumerate(self.agents):
            tile = QLabel(f"{agent}\n🟢 Online")
            tile.setAlignment(Qt.AlignCenter)
            tile.setStyleSheet("background:#44aa44;color:#fff;padding:8px;")
            self.agent_tiles[agent] = tile
            gl.addWidget(tile, i//4, i%4)
        g.addWidget(grid_grp); g.addStretch()
        return w

    # helpers ──────────────────────────────────────────────────────────────────
    def _group(self, title:str, layout_type=QGridLayout) -> QGroupBox:
        box = QGroupBox(title); box.setLayout(layout_type()); return box

    def _btn(self, layout, text, fn, danger=False):
        btn = QPushButton(text); btn.clicked.connect(fn)
        if danger: btn.setStyleSheet("background:#c0392b;color:#fff;")
        layout.addWidget(btn)

    def _act_ind(self, msg:str|MsgTag, tag:MsgTag|None=None):
        agent = self.agent_combo.currentText()
        if isinstance(msg, MsgTag): tag, msg = msg, msg.value
        self.phone.send(agent, msg, tag or MsgTag.NORMAL)

    def _broadcast(self, tag:MsgTag, msg:str|None=None):
        self.phone.broadcast(msg or tag.value, tag)

    def _send_custom(self):
        txt = self.msg_edit.text().strip()
        if not txt: return
        tag = MsgTag[self.msg_type.currentText().upper()]
        agent = self.agent_combo.currentText()
        self.phone.send(agent, txt, tag)
        self.history.append(f"{datetime.now().strftime('%H:%M:%S')} → {agent}: {tag.value} {txt}")
        self.msg_edit.clear()

    def _refresh_history(self): self._log("History refreshed (placeholder)")

    def _refresh_status(self):
        self.sys_status.setPlainText("All systems nominal.\nLast check: "+datetime.now().isoformat(timespec='seconds'))

    def _log(self, text): log.info(text); self.statusBar().showMessage(text, 4000)

# ─────────────────── run
def main():
    app = QApplication(sys.argv)
    gui = CellPhoneGUI(); gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    from datetime import datetime
    main() 