#!/usr/bin/env python3
"""Launch helper for the Open3D GUI runner."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def _configure_display_backend() -> None:
    """Prefer X11 backend on Wayland systems that are known to fail with GLFW."""

    # Open3D/GLFW can crash on some Wayland+libdecor stacks; prefer X11 when available.
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    has_x11_display = bool(os.environ.get("DISPLAY"))
    glfw_platform_set = os.environ.get("GLFW_PLATFORM")
    if session_type == "wayland" and has_x11_display and not glfw_platform_set:
        os.environ["GLFW_PLATFORM"] = "x11"


if __name__ == "__main__":
    _configure_display_backend()
    from submarine_sim.open3d_ui import run_gui

    raise SystemExit(run_gui())
