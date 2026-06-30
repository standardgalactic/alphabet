from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "configs" / "batch.example.json"
runs = json.loads(BATCH.read_text(encoding="utf-8"))["runs"]
for idx, run in enumerate(runs):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(run.get("params", {}), f)
        params_path = f.name
    env = dict(os.environ)
    env["PARAMS"] = params_path
    env["OUTPUT_DIR"] = str(ROOT / "output_v4" / f"batch_{idx:03d}_{run['generator']}")
    subprocess.check_call([str(ROOT / "scripts" / "render_one_v4.sh"), run["generator"]], env=env)
    os.unlink(params_path)
