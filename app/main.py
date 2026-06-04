from __future__ import annotations

from flask import Flask, render_template, request

from app.physics import (
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
    try:
        return float(raw_value.replace(",", "."))
    except ValueError:
        return default


def render_page(template_name: str, active_view: str, **context):
    data = {"active_view": active_view, "error": None, **context}
    return render_template(template_name, data=data)


@app.get("/")
def home():
    return render_page("home.html", "home")


@app.get("/ejercicio-1")
def exercise1():
    ex1_current = read_float("ex1_current", 1.0)
    ex1_radius_cm = read_float("ex1_radius_cm", 100.0)
    ex1_target_field = read_float("ex1_target_field", 1e-4)
    error_msg = None
    try:
        ex1_data = {
            "current": ex1_current,
            "radius_cm": ex1_radius_cm,
            "radius_m": ex1_radius_cm / 100,
            "target_field": ex1_target_field,
            "field": field_infinite_wire(ex1_current, ex1_radius_cm / 100),
            "distance": distance_for_infinite_wire_field(ex1_current, ex1_target_field),
        }
    except ValueError as e:
        error_msg = str(e)
        ex1_data = {
            "current": ex1_current,
            "radius_cm": ex1_radius_cm,
            "radius_m": ex1_radius_cm / 100,
            "target_field": ex1_target_field,
            "field": None,
            "distance": None,
        }
    return render_page("exercises/ex1.html", "ex1", error=error_msg, ex1=ex1_data)


@app.get("/ejercicio-2")
def exercise2():
    ex2_current = read_float("ex2_current", 1.0)
    ex2_distance_cm = read_float("ex2_distance_cm", 2.0)
    p1x = read_float("p1x", 1.0)
    p1y = read_float("p1y", 1.0)
    p2x = read_float("p2x", 1.5)
    p2y = read_float("p2y", 0.0)
    error_msg = None
    try:
        ex2_data = {
            "current": ex2_current,
            "distance_cm": ex2_distance_cm,
            "points": two_parallel_entering_wires(
                ex2_current,
                ex2_distance_cm,
                [(p1x, p1y), (p2x, p2y)],
            ),
            "form": {"p1x": p1x, "p1y": p1y, "p2x": p2x, "p2y": p2y},
        }
    except ValueError as e:
        error_msg = str(e)
        ex2_data = {
            "current": ex2_current,
            "distance_cm": ex2_distance_cm,
            "points": [],
            "form": {"p1x": p1x, "p1y": p1y, "p2x": p2x, "p2y": p2y},
        }
    return render_page("exercises/ex2.html", "ex2", error=error_msg, ex2=ex2_data)


@app.get("/ejercicio-7")
def exercise7():
    ex7_radius_m = read_float("ex7_radius_m", 0.1)
    ex7_current = read_float("ex7_current", 10.0)
    ex7_field = read_float("ex7_field", 3e-3)
    error_msg = None
    try:
        ex7_data = {
            "radius_m": ex7_radius_m,
            "current": ex7_current,
            "field": ex7_field,
            "turns": coil_turns_for_center_field(ex7_field, ex7_radius_m, ex7_current),
        }
    except ValueError as e:
        error_msg = str(e)
        ex7_data = {
            "radius_m": ex7_radius_m,
            "current": ex7_current,
            "field": ex7_field,
            "turns": None,
        }
    return render_page("exercises/ex7.html", "ex7", error=error_msg, ex7=ex7_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
