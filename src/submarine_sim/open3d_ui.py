from __future__ import annotations

from pathlib import Path

import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

from .app import SubmarineApp


class Phase1Open3DUI:
    def __init__(self) -> None:
        self.submarine_app = SubmarineApp()

        self.window = gui.Application.instance.create_window("Phase 1 Submarine Simulation", 1400, 900)
        self.window.set_on_layout(self._on_layout)

        em = self.window.theme.font_size
        spacing = int(0.35 * em)
        margins = gui.Margins(spacing, spacing, spacing, spacing)

        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(self.window.renderer)
        self.scene.scene.set_background([0.05, 0.08, 0.12, 1.0])
        self._setup_scene_placeholder()

        self.inputs_panel = gui.Vert(spacing, margins)
        self.telemetry_panel = gui.Vert(spacing, margins)
        self.environment_panel = gui.Vert(spacing, margins)

        self._build_inputs_panel(spacing)
        self._build_telemetry_panel()
        self._build_environment_panel(spacing)

        self.window.add_child(self.scene)
        self.window.add_child(self.inputs_panel)
        self.window.add_child(self.telemetry_panel)
        self.window.add_child(self.environment_panel)

    def _setup_scene_placeholder(self) -> None:
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.5, origin=[0.0, 0.0, 0.0])
        axis.compute_vertex_normals()
        material = rendering.MaterialRecord()
        material.shader = "defaultLit"
        self.scene.scene.add_geometry("world_axis", axis, material)
        self.scene.setup_camera(60.0, axis.get_axis_aligned_bounding_box(), axis.get_center())

    def _build_inputs_panel(self, spacing: int) -> None:
        self.inputs_panel.add_child(gui.Label("Inputs"))

        self.inputs_panel.add_child(gui.Label("Case JSON"))
        self.case_input = gui.TextEdit()
        self.case_input.text_value = "data/base_case.json"
        self.inputs_panel.add_child(self.case_input)

        self.inputs_panel.add_child(gui.Label("Steps"))
        self.steps_input = gui.TextEdit()
        self.steps_input.text_value = "5"
        self.inputs_panel.add_child(self.steps_input)

        self.inputs_panel.add_child(gui.Label("Report CSV"))
        self.report_input = gui.TextEdit()
        self.report_input.text_value = "logs/phase1_gui_report.csv"
        self.inputs_panel.add_child(self.report_input)

        button_row = gui.Horiz(spacing)
        self.load_button = gui.Button("Load Case")
        self.load_button.set_on_clicked(self._on_load_clicked)
        button_row.add_child(self.load_button)

        self.run_button = gui.Button("Run Simulation")
        self.run_button.set_on_clicked(self._on_run_clicked)
        button_row.add_child(self.run_button)
        self.inputs_panel.add_child(button_row)

        self.save_button = gui.Button("Export CSV")
        self.save_button.set_on_clicked(self._on_save_clicked)
        self.inputs_panel.add_child(self.save_button)

        self.status_label = gui.Label("Status: ready")
        self.inputs_panel.add_child(self.status_label)

    def _build_telemetry_panel(self) -> None:
        self.telemetry_panel.add_child(gui.Label("Telemetry"))
        self.telemetry_labels: dict[str, gui.Label] = {}
        fields = [
            "drag_force_n",
            "buoyancy_force_n",
            "effective_velocity_ms",
            "torque_required_nm",
            "torque_margin_nm",
            "cavitation_risk",
            "gm_m",
            "stability_warning",
            "environment_mode",
        ]

        for field in fields:
            label = gui.Label(f"{field}: -")
            self.telemetry_labels[field] = label
            self.telemetry_panel.add_child(label)

        self.alert_label = gui.Label("Alerts: none")
        self.telemetry_panel.add_child(self.alert_label)

    def _build_environment_panel(self, spacing: int) -> None:
        self.environment_panel.add_child(gui.Label("Environment / Safety"))

        self.environment_panel.add_child(gui.Label("Mode"))
        self.mode_combo = gui.Combobox()
        self.mode_combo.add_item("base")
        self.mode_combo.add_item("real")
        self.mode_combo.selected_index = 0
        self.mode_combo.set_on_selection_changed(self._on_mode_changed)
        self.environment_panel.add_child(self.mode_combo)

        self.noise_checkbox = gui.Checkbox("Enable sensor noise")
        self.noise_checkbox.checked = False
        self.noise_checkbox.set_on_checked(self._on_noise_toggled)
        self.environment_panel.add_child(self.noise_checkbox)

        safety_row = gui.Horiz(spacing)
        self.emergency_button = gui.Button("Emergency Surface")
        self.emergency_button.set_on_clicked(self._on_emergency_clicked)
        safety_row.add_child(self.emergency_button)
        self.environment_panel.add_child(safety_row)

        self.environment_state_label = gui.Label("Mode: base | Noise: off | Emergency: off")
        self.environment_panel.add_child(self.environment_state_label)

    def _on_layout(self, layout_context: gui.LayoutContext) -> None:
        rect = self.window.content_rect

        bottom_height = int(rect.height * 0.23)
        left_width = int(rect.width * 0.24)
        right_width = int(rect.width * 0.24)

        top_height = rect.height - bottom_height
        scene_width = max(100, rect.width - left_width - right_width)

        self.inputs_panel.frame = gui.Rect(rect.x, rect.y, left_width, top_height)
        self.scene.frame = gui.Rect(rect.x + left_width, rect.y, scene_width, top_height)
        self.telemetry_panel.frame = gui.Rect(rect.x + left_width + scene_width, rect.y, right_width, top_height)
        self.environment_panel.frame = gui.Rect(rect.x, rect.y + top_height, rect.width, bottom_height)

    def _on_mode_changed(self, mode: str, index: int) -> None:  # noqa: ARG002
        self.submarine_app.ui_controller.set_environment_mode(mode)
        self.noise_checkbox.checked = self.submarine_app.ui_controller.state.noise_enabled
        self._refresh_environment_state()
        self._set_status(f"mode set to {mode}")

    def _on_noise_toggled(self, is_checked: bool) -> None:
        self.submarine_app.ui_controller.set_noise_enabled(is_checked)
        self._refresh_environment_state()
        self._set_status(f"noise {'enabled' if is_checked else 'disabled'}")

    def _on_emergency_clicked(self) -> None:
        self.submarine_app.ui_controller.trigger_emergency_surface()
        self._refresh_environment_state()
        self._set_status("emergency surface triggered")

    def _on_load_clicked(self) -> None:
        case = self.case_input.text_value.strip()
        try:
            self.submarine_app.ui_controller.load_case(case)
        except Exception as exc:  # noqa: BLE001
            self._set_status(f"load failed: {exc}")
            return
        self._set_status(f"loaded {case}")

    def _on_run_clicked(self) -> None:
        steps = self._read_steps()
        if steps is None:
            return

        case = self.case_input.text_value.strip()
        try:
            self.submarine_app.ui_controller.load_case(case)
            rows = self.submarine_app.ui_controller.run_simulation(steps)
        except Exception as exc:  # noqa: BLE001
            self._set_status(f"run failed: {exc}")
            return

        if rows:
            self._update_telemetry(rows[-1])
        self._set_status(f"simulation complete ({len(rows)} steps)")

    def _on_save_clicked(self) -> None:
        report = self.report_input.text_value.strip()
        try:
            self.submarine_app.ui_controller.save_report(report)
        except Exception as exc:  # noqa: BLE001
            self._set_status(f"export failed: {exc}")
            return
        self._set_status(f"report written to {Path(report)}")

    def _read_steps(self) -> int | None:
        raw_steps = self.steps_input.text_value.strip()
        try:
            steps = int(raw_steps)
        except ValueError:
            self._set_status("steps must be an integer")
            return None

        if steps <= 0:
            self._set_status("steps must be > 0")
            return None
        return steps

    def _update_telemetry(self, snapshot: dict) -> None:
        for field, label in self.telemetry_labels.items():
            label.text = f"{field}: {snapshot.get(field, '-')}"

        alerts: list[str] = []
        if snapshot.get("torque_margin_nm", 0.0) < 0.0:
            alerts.append("TORQUE LIMIT EXCEEDED")
        if snapshot.get("cavitation_risk"):
            alerts.append("CAVITATION RISK")
        if snapshot.get("stability_warning"):
            alerts.append("NEGATIVE GM - INSTABILITY")
        self.alert_label.text = f"Alerts: {', '.join(alerts) if alerts else 'none'}"

    def _refresh_environment_state(self) -> None:
        state = self.submarine_app.ui_controller.state
        self.environment_state_label.text = (
            f"Mode: {state.environment_mode} | "
            f"Noise: {'on' if state.noise_enabled else 'off'} | "
            f"Emergency: {'on' if state.emergency_surface else 'off'}"
        )

    def _set_status(self, message: str) -> None:
        self.status_label.text = f"Status: {message}"


def run_gui() -> int:
    app = gui.Application.instance
    app.initialize()
    Phase1Open3DUI()
    app.run()
    return 0
