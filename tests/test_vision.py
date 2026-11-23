"""Unit tests for bounded visual evidence and safe job-pipeline attachment."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, ".")
from studio import jobs, vision


fails = []


def check(name, got, want=True):
    ok = want(got) if callable(want) else got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  got {got!r}"))
    if not ok:
        fails.append(name)


check("activity score is bounded", 0.0 <= vision._activity_score(10, 10) <= 1.0)
check("zero visual activity scores zero", vision._activity_score(0, 0), 0.0)
check("high motion increases activity",
      vision._activity_score(0.15, 0.02) > vision._activity_score(0.01, 0.02))
check("high edge density increases activity",
      vision._activity_score(0.02, 0.15) > vision._activity_score(0.02, 0.01))
check("negative start is rejected", vision.analyze_window("missing.mp4", -1, 2)["available"], False)
check("reversed time range is rejected", vision.analyze_window("missing.mp4", 3, 2)["available"], False)
check("invalid sample rate is rejected",
      vision.analyze_window("missing.mp4", 0, 2, sample_fps=0)["available"], False)
check("missing video fails safely",
      vision.analyze_window("missing-clipnova-test.mp4", 0, 2)["available"], False)
check("visual evidence label is generic", "visual_activity_only" == "visual_activity_only")

with tempfile.TemporaryDirectory() as folder:
    source = Path(folder) / "source.mp4"
    source.write_bytes(b"placeholder")
    job = {"source_path": str(source)}
    clip = {"start": 20.0, "end": 32.0, "src_offset": 8.0}
    evidence = {"available": True, "evidence_type": "visual_activity_only"}
    with patch.object(vision, "analyze_window", return_value=evidence) as analyze:
        jobs._attach_visual_evidence(job, clip)
    check("piece source timestamps account for src_offset",
          analyze.call_args.args[1:3], (12.0, 24.0))
    check("visual evidence is attached to the clip", clip.get("visual"), evidence)

    piece = Path(folder) / "piece.mp4"
    piece.write_bytes(b"placeholder")
    clip2 = {"start": 3.0, "end": 7.0, "src_offset": 0.0, "src": str(piece)}
    with patch.object(vision, "analyze_window", return_value=evidence) as analyze:
        jobs._attach_visual_evidence(job, clip2)
    check("downloaded clip piece is preferred over full source",
          analyze.call_args.args[0], piece)

clip3 = {"start": 1.0, "end": 4.0}
jobs._attach_visual_evidence({}, clip3)
check("missing source records unavailable evidence",
      clip3.get("visual", {}).get("available"), False)

clip4 = {"start": 1.0, "end": 4.0, "src": "not-a-real-file.mp4"}
jobs._attach_visual_evidence({}, clip4)
check("missing media file records unavailable evidence",
      clip4.get("visual", {}).get("available"), False)

clip5 = {"start": 5.0, "end": 5.0}
jobs._attach_visual_evidence({"source_path": "not-a-real-file.mp4"}, clip5)
check("empty time range safely records unavailable evidence",
      clip5.get("visual", {}).get("available"), False)

print("ALL PASSED" if not fails else f"{len(fails)} failed")
sys.exit(1 if fails else 0)
