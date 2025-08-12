from __future__ import annotations
from typing import Callable, Optional, List, Dict, Any
import threading
import time
import json
from pathlib import Path
import fnmatch
import shutil


class InboxListener:
    """Phase 2 scaffold: directory file-tail listener wired to MessagePipeline.

    - Polls a directory for new *.json (configurable) files
    - Parses minimal schema: {"from":"Agent-1","to":"Agent-2","message":"..."}
    - Invokes callbacks with raw message dict
    - If a pipeline is provided, enqueues (to, message)
    """

    def __init__(
        self,
        inbox_dir: Optional[str] = None,
        file_pattern: str = "*.json",
        poll_interval_s: float = 0.2,
        pipeline: Optional[object] = None,
    ) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._dir = Path(inbox_dir) if inbox_dir else None
        self._pattern = file_pattern
        self._poll_interval_s = poll_interval_s
        self._seen: set[str] = set()
        self._pipeline = pipeline
        # processed index for idempotency across restarts
        self._processed_dir = (self._dir.parent / "processed") if self._dir else None
        self._processing_dir = (self._dir.parent / "processing") if self._dir else None
        self._index_path = (self._dir.parent / "processed_index.json") if self._dir else None
        self._processed_index: Dict[str, float] = {}
        self._load_processed_index()

    def on_message(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        self._callbacks.append(callback)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def _loop(self) -> None:
        # If no directory configured, idle
        while self._running:
            if not self._dir or not self._dir.exists():
                time.sleep(self._poll_interval_s)
                continue

            for path in self._iter_new_files(self._dir, self._pattern):
                # Move to processing to avoid duplicate readers
                proc_path = self._move_to_processing(path)
                data = None
                try:
                    with open(proc_path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                except Exception:
                    data = None

                if isinstance(data, dict):
                    msg_id = str(data.get("id") or proc_path.name)
                    if self._is_processed(msg_id):
                        self._finalize_processed(proc_path, already=True)
                        continue

                    # Fan out to callbacks
                    for cb in list(self._callbacks):
                        try:
                            cb(data)
                        except Exception:
                            pass

                    # Enqueue to pipeline if available
                    if self._pipeline is not None:
                        to_agent = str(data.get("to", "")).strip() or "unknown"
                        message = str(data.get("message", "")).strip()
                        try:
                            enqueue = getattr(self._pipeline, "enqueue", None)
                            if callable(enqueue):
                                enqueue(to_agent, message)
                        except Exception:
                            pass

                    # Mark processed and move file
                    self._mark_processed(msg_id)
                    self._finalize_processed(proc_path)

            time.sleep(self._poll_interval_s)

    def _iter_new_files(self, directory: Path, pattern: str):
        for p in directory.iterdir():
            if not p.is_file():
                continue
            if not fnmatch.fnmatch(p.name, pattern):
                continue
            key = str(p.resolve())
            if key in self._seen:
                continue
            self._seen.add(key)
            yield p

    # ─────────────── processed index helpers ───────────────
    def _load_processed_index(self) -> None:
        try:
            if self._index_path and self._index_path.exists():
                self._processed_index = json.loads(self._index_path.read_text(encoding="utf-8"))
        except Exception:
            self._processed_index = {}

    def _save_processed_index(self) -> None:
        try:
            if self._index_path:
                self._index_path.write_text(json.dumps(self._processed_index, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _is_processed(self, msg_id: str) -> bool:
        return msg_id in self._processed_index

    def _mark_processed(self, msg_id: str) -> None:
        self._processed_index[msg_id] = time.time()
        self._save_processed_index()

    def _move_to_processing(self, src: Path) -> Path:
        try:
            if self._processing_dir:
                self._processing_dir.mkdir(parents=True, exist_ok=True)
                dst = self._processing_dir / src.name
                shutil.move(str(src), str(dst))
                return dst
        except Exception:
            pass
        return src

    def _finalize_processed(self, proc_path: Path, already: bool = False) -> None:
        try:
            if self._processed_dir:
                self._processed_dir.mkdir(parents=True, exist_ok=True)
                dst = self._processed_dir / proc_path.name
                shutil.move(str(proc_path), str(dst))
            else:
                # fallback: delete
                if not already:
                    proc_path.unlink(missing_ok=True)  # type: ignore[arg-type]
        except Exception:
            try:
                if not already:
                    proc_path.unlink(missing_ok=True)  # type: ignore[arg-type]
            except Exception:
                pass


