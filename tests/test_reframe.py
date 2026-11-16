"""Pure geometry checks for smart face framing; no sample video or external service required."""
import sys
sys.path.insert(0, ".")
from studio import render

fails = []


def check(name, got, want=True):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"   got {got!r}"))
    if not ok:
        fails.append(name)


check("smart framing is an available layout", "smart" in render.LAYOUTS)
left = render._smart_crop_filter(0.0, 1920, 1080)
middle = render._smart_crop_filter(0.5, 1920, 1080)
right = render._smart_crop_filter(1.0, 1920, 1080)
check("smart crop keeps vertical output dimensions", "crop=1080:1920" in middle)
check("left-side face moves crop window left", "0.000000" in left)
check("right-side face moves crop window right", "1.000000" in right)
check("center face stays centered", "0.500000" in middle)
track = [(0.0, 0.15), (2.0, 0.85), (4.0, 0.40)]
expr = render._track_expression(track)
check("tracking expression includes time-based interpolation", "t-" in expr and expr.startswith("if(lt(t"))
check("tracking expression retains first and final target positions", "0.150000" in expr and "0.400000" in expr)
check("tracking expression clamps out-of-range face positions",
      "1.000000" in render._track_expression([(0, 1.4)]))
check("empty tracking data uses a safe centred crop", render._track_expression([]) == "0.5")
check("smart mode falls back to centre crop for portrait footage",
      render._face_center(None, 0, 10, 1080, 1920) is None)
print("ALL PASSED" if not fails else f"{len(fails)} failed")
sys.exit(1 if fails else 0)
