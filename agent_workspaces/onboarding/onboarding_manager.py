import os
import json
from pathlib import Path
from typing import List, Dict, Optional

ONBOARDING_ROOT = Path(__file__).parent
CHECKLIST_STATE_FILE = ONBOARDING_ROOT / "onboarding_checklist_state.json"

EXCLUDE_DIRS = {"logs", "temp", "__pycache__"}
INCLUDE_EXTS = {".md", ".py"}

class OnboardingManager:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else ONBOARDING_ROOT
        self.docs = self.discover_onboarding_docs()
        self.checklist = self.generate_checklist()
        self.state = self.load_state()

    def discover_onboarding_docs(self) -> List[Dict]:
        """Recursively find all .md and .py docs in onboarding directory."""
        docs = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Exclude certain directories
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext in INCLUDE_EXTS:
                    fpath = Path(dirpath) / fname
                    docs.append({
                        "path": str(fpath.relative_to(self.root_dir)),
                        "name": fname,
                        "ext": ext,
                        "type": "script" if ext == ".py" else "doc"
                    })
        return sorted(docs, key=lambda d: d["path"])

    def generate_checklist(self) -> List[Dict]:
        """Generate checklist items from discovered docs."""
        checklist = []
        for doc in self.docs:
            item = {
                "path": doc["path"],
                "name": doc["name"],
                "type": doc["type"],
                "completed": False
            }
            checklist.append(item)
        return checklist

    def load_state(self) -> Dict:
        if CHECKLIST_STATE_FILE.exists():
            try:
                with open(CHECKLIST_STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default state: all incomplete
        return {item["path"]: False for item in self.checklist}

    def save_state(self):
        with open(CHECKLIST_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def mark_item_complete(self, doc_path: str):
        self.state[doc_path] = True
        self.save_state()

    def get_checklist(self) -> List[Dict]:
        """Return checklist with completion status."""
        for item in self.checklist:
            item["completed"] = self.state.get(item["path"], False)
        return self.checklist

    def get_progress(self) -> Dict:
        total = len(self.checklist)
        completed = sum(1 for item in self.get_checklist() if item["completed"])
        percent = (completed / total * 100) if total else 0
        outstanding = [item for item in self.get_checklist() if not item["completed"]]
        return {
            "total": total,
            "completed": completed,
            "percent": percent,
            "outstanding": outstanding
        }

    def reset_checklist(self):
        self.state = {item["path"]: False for item in self.checklist}
        self.save_state()

# Example usage (for testing):
if __name__ == "__main__":
    mgr = OnboardingManager()
    print("Discovered docs:")
    for doc in mgr.docs:
        print(f"- {doc['path']} ({doc['type']})")
    print("\nChecklist:")
    for item in mgr.get_checklist():
        print(f"- {item['name']}: {'DONE' if item['completed'] else 'TODO'}")
    print("\nProgress:", mgr.get_progress()) 