from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt, hypot


MU_0 = 4 * pi * 1e-7


@dataclass(frozen=True)
class Wire:
    x_cm: float
    y_cm: float


@dataclass(frozen=True)
class WireFieldResult:
    radius_m: float
    field_t: float


@dataclass(frozen=True)
class DistanceForFieldResult:
    radius_m: float
    radius_cm: float


@dataclass(frozen=True)
class VectorFieldResult:
    bx: float
    by: float
    magnitude: float = 0.0

    def __post_init__(self):
        # Como es frozen=True, usamos object.__setattr__ para inicializar la magnitud automáticamente
        object.__setattr__(self, "magnitude", hypot(self.bx, self.by))


@dataclass(frozen=True)
class TwoWirePointResult:
    point_cm: tuple[float, float]
    wire_1: VectorFieldResult
    wire_2: VectorFieldResult
    total: VectorFieldResult


@dataclass(frozen=True)
class CoilTurnsResult:
    turns: float


def field_infinite_wire(current_a: float, radius_m: float) -> WireFieldResult:
    if radius_m <= 0:
        raise ValueError("El radio/distancia debe ser mayor a cero.")
    field_t = MU_0 * current_a / (2 * pi * radius_m)
    return WireFieldResult(radius_m=radius_m, field_t=field_t)


def distance_for_infinite_wire_field(current_a: float, field_t: float) -> DistanceForFieldResult:
    if field_t <= 0:
        raise ValueError("El campo magnético objetivo debe ser mayor a cero.")
    radius_m = MU_0 * current_a / (2 * pi * field_t)
    return DistanceForFieldResult(radius_m=radius_m, radius_cm=radius_m * 100)


def field_entering_wire_at_point(
    current_a: float,
    wire_x_cm: float,
    wire_y_cm: float,
    point_x_cm: float,
    point_y_cm: float,
) -> VectorFieldResult:
    dx_m = (point_x_cm - wire_x_cm) / 100
    dy_m = (point_y_cm - wire_y_cm) / 100
    r2 = dx_m * dx_m + dy_m * dy_m
    if r2 == 0:
        raise ValueError("El punto de medición no puede coincidir con la posición del conductor.")

    factor = MU_0 * current_a / (2 * pi * r2)
    bx = factor * dy_m
    by = -factor * dx_m
    return VectorFieldResult(bx=bx, by=by)


def two_parallel_entering_wires(
    current_a: float,
    distance_cm: float,
    points_cm: list[tuple[float, float]],
) -> list[TwoWirePointResult]:
    if distance_cm <= 0:
        raise ValueError("La distancia de separación entre conductores debe ser mayor a cero.")
    wire_1 = Wire(0.0, 0.0)
    wire_2 = Wire(distance_cm, 0.0)
    results: list[TwoWirePointResult] = []
    for point in points_cm:
        b1 = field_entering_wire_at_point(current_a, wire_1.x_cm, wire_1.y_cm, point[0], point[1])
        b2 = field_entering_wire_at_point(current_a, wire_2.x_cm, wire_2.y_cm, point[0], point[1])
        total = VectorFieldResult(
            bx=b1.bx + b2.bx,
            by=b1.by + b2.by,
        )
        results.append(TwoWirePointResult(point_cm=point, wire_1=b1, wire_2=b2, total=total))
    return results


def coil_turns_for_center_field(field_t: float, radius_m: float, current_a: float) -> CoilTurnsResult:
    if radius_m <= 0:
        raise ValueError("El radio de la bobina debe ser mayor a cero.")
    if current_a <= 0:
        raise ValueError("La corriente eléctrica debe ser mayor a cero.")
    turns = 2 * radius_m * field_t / (MU_0 * current_a)
    return CoilTurnsResult(turns=turns)
