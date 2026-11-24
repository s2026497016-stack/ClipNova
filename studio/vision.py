"""Lightweight visual analysis for selected video windows.

This module reports visual activity and scene-change evidence.
It does not identify specific game events.
"""
import math
from pathlib import Path


def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, float(value)))


def _activity_score(motion, edge_density):
    """Combine normalized motion and edge density into a visual activity score."""
    motion_score = _clamp(motion / 0.18)
    edge_score = _clamp(edge_density / 0.18)
    return round(_clamp(0.65 * motion_score + 0.35 * edge_score), 4)


def analyze_window(src, start, end, sample_fps=1.0, max_samples=24,
                   resize_width=320):
    """Analyze a bounded video window and return measurable visual evidence."""
    try:
        start = float(start)
        end = float(end)
        sample_fps = float(sample_fps)
        max_samples = int(max_samples)
        resize_width = int(resize_width)
    except (TypeError, ValueError):
        return {"available": False, "reason": "invalid arguments"}

    if not (math.isfinite(start) and math.isfinite(end)):
        return {"available": False, "reason": "invalid time range"}
    if start < 0 or end <= start:
        return {"available": False, "reason": "invalid time range"}
    if not (0 < sample_fps <= 5) or max_samples < 2 or resize_width < 64:
        return {"available": False, "reason": "invalid sampling settings"}

    cap = None
    try:
        import cv2
        import numpy as np

        path = Path(src)
        if not path.is_file():
            return {"available": False, "reason": "source file not found"}

        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            return {"available": False, "reason": "video could not be opened"}

        duration = end - start
        count = min(max_samples, max(2, int(math.ceil(duration * sample_fps)) + 1))
        times = [start + duration * i / (count - 1) for i in range(count)]

        previous_gray = None
        previous_hist = None
        motions = []
        edges = []
        scene_changes = 0
        sampled = 0

        for timestamp in times:
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ok, frame = cap.read()
            if not ok or frame is None:
                continue

            height, width = frame.shape[:2]
            if width < 1 or height < 1:
                continue

            target_height = max(1, int(height * resize_width / width))
            frame = cv2.resize(frame, (resize_width, target_height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            edge_map = cv2.Canny(gray, 80, 160)
            edges.append(float(np.count_nonzero(edge_map)) / edge_map.size)

            hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
            cv2.normalize(hist, hist)

            if previous_gray is not None:
                motion = float(np.mean(cv2.absdiff(gray, previous_gray))) / 255.0
                motions.append(motion)

                distance = float(cv2.compareHist(
                    previous_hist, hist, cv2.HISTCMP_BHATTACHARYYA
                ))
                if distance >= 0.45:
                    scene_changes += 1

            previous_gray = gray
            previous_hist = hist
            sampled += 1

        if sampled < 2:
            return {
                "available": False,
                "reason": "not enough readable frames",
                "sampled_frames": sampled,
            }

        average_motion = sum(motions) / len(motions) if motions else 0.0
        average_edges = sum(edges) / len(edges) if edges else 0.0

        return {
            "available": True,
            "start": round(start, 3),
            "end": round(end, 3),
            "sampled_frames": sampled,
            "average_motion": round(average_motion, 4),
            "edge_density": round(average_edges, 4),
            "scene_changes": scene_changes,
            "visual_activity": _activity_score(average_motion, average_edges),
            "evidence_type": "visual_activity_only",
        }

    except Exception as exc:
        return {
            "available": False,
            "reason": f"visual analysis failed: {type(exc).__name__}",
        }
    finally:
        if cap is not None:
            cap.release()
