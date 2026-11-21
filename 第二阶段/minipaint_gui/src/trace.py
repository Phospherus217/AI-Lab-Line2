import json
import time
from pathlib import Path

class Trace:
    def __init__(self,run_dir:Path):
        self.run_dir = run_dir
        self.steps = []
        self.t0 = time.time()

    def add(self, step:str, ok:bool, **extra)->None:
        self.steps.append({
            "step": step,
            "ok": ok,
            "ms": int((time.time() - self.t0) * 1000),
            **extra,
        })

    def save(self, success:bool)->None:
        data = {
            "success": success,
            "cost_ms": int((time.time() - self.t0) * 1000),
            "steps": self.steps,
        }
        (self.run_dir / "trace.json").write_text(
            json.dumps(data,indent=1),encoding="utf-8")
