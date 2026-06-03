from __future__ import annotations

from flask import Flask, render_template, request

from app.physics import (
    MU_0,
    coil_turns_for_center_field,
    distance_for_infinite_wire_field,
    field_infinite_wire,
    two_parallel_entering_wires,
)


app = Flask(__name__)


def read_float(name: str, default: float) -> float:
    raw_value = request.args.get(name, "")
    if raw_value.strip() == "":
        return default
    return float(raw_value.replace(",", "."))


@app.get("/")
def index():
    active_view = request.args.get("view", "home")
    if active_view not in {"home", "ex1", "ex2", "ex7"}:
        active_view = "home"

    ex1_current = read_float("ex1_current", 1.0)
    ex1_radius_cm = read_float("ex1_radius_cm", 100.0)
    ex1_target_field = read_float("ex1_target_field", 1e-4)

    ex2_current = read_float("ex2_current", 1.0)
    ex2_distance_cm = read_float("ex2_distance_cm", 2.0)
    p1x = read_float("p1x", 1.0)
    p1y = read_float("p1y", 1.0)
    p2x = read_float("p2x", 1.5)
    p2y = read_float("p2y", 0.0)

    ex7_radius_m = read_float("ex7_radius_m", 0.1)
    ex7_current = read_float("ex7_current", 10.0)
    ex7_field = read_float("ex7_field", 3e-3)

    data = {
        "active_view": active_view,
        "mu_0": MU_0,
        "ex1": {
            "current": ex1_current,
            "radius_cm": ex1_radius_cm,
            "radius_m": ex1_radius_cm / 100,
            "target_field": ex1_target_field,
            "field": field_infinite_wire(ex1_current, ex1_radius_cm / 100),
            "distance": distance_for_infinite_wire_field(ex1_current, ex1_target_field),
        },
        "ex2": {
            "current": ex2_current,
            "distance_cm": ex2_distance_cm,
            "points": two_parallel_entering_wires(
                ex2_current,
                ex2_distance_cm,
                [(p1x, p1y), (p2x, p2y)],
            ),
            "form": {"p1x": p1x, "p1y": p1y, "p2x": p2x, "p2y": p2y},
        },
        "ex7": {
            "radius_m": ex7_radius_m,
            "current": ex7_current,
            "field": ex7_field,
            "turns": coil_turns_for_center_field(ex7_field, ex7_radius_m, ex7_current),
        },
    }
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
