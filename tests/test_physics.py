import unittest
from math import isclose, pi

from app.physics import (
    MU_0,
    coil_turns_for_center_field,
    distance_for_infinite_wire_field,
    field_infinite_wire,
    two_parallel_entering_wires,
    field_entering_wire_at_point,
    VectorFieldResult,
)


class PhysicsFormulaTests(unittest.TestCase):
    def test_infinite_wire_field_at_one_meter(self):
        result = field_infinite_wire(current_a=1, radius_m=1)
        self.assertTrue(isclose(result.field_t, 2e-7, rel_tol=1e-12))

    def test_infinite_wire_invalid_radius(self):
        with self.assertRaises(ValueError):
            field_infinite_wire(current_a=1, radius_m=0)
        with self.assertRaises(ValueError):
            field_infinite_wire(current_a=1, radius_m=-0.5)

    def test_distance_for_target_field(self):
        result = distance_for_infinite_wire_field(current_a=1, field_t=1e-4)
        self.assertTrue(isclose(result.radius_m, 0.002, rel_tol=1e-12))
        self.assertTrue(isclose(result.radius_cm, 0.2, rel_tol=1e-12))

    def test_distance_for_target_field_invalid(self):
        with self.assertRaises(ValueError):
            distance_for_infinite_wire_field(current_a=1, field_t=0)
        with self.assertRaises(ValueError):
            distance_for_infinite_wire_field(current_a=1, field_t=-1e-5)

    def test_two_wire_known_points(self):
        results = two_parallel_entering_wires(
            current_a=1,
            distance_cm=2,
            points_cm=[(1, 1), (1.5, 0)],
        )

        p1 = results[0].total
        self.assertTrue(isclose(p1.bx, 2e-5, rel_tol=1e-12))
        self.assertTrue(isclose(p1.by, 0, abs_tol=1e-18))
        self.assertTrue(isclose(p1.magnitude, 2e-5, rel_tol=1e-12))

        p2 = results[1].total
        self.assertTrue(isclose(p2.bx, 0, abs_tol=1e-18))
        self.assertTrue(isclose(p2.by, 2.6666666666666667e-5, rel_tol=1e-12))
        self.assertTrue(isclose(p2.magnitude, 2.6666666666666667e-5, rel_tol=1e-12))

    def test_two_wire_invalid_distance(self):
        with self.assertRaises(ValueError):
            two_parallel_entering_wires(current_a=1, distance_cm=0, points_cm=[(1, 1)])

    def test_point_coincides_with_wire(self):
        with self.assertRaises(ValueError):
            field_entering_wire_at_point(
                current_a=1.0,
                wire_x_cm=0.0,
                wire_y_cm=0.0,
                point_x_cm=0.0,
                point_y_cm=0.0,
            )

    def test_coil_turns(self):
        result = coil_turns_for_center_field(field_t=3e-3, radius_m=0.1, current_a=10)
        expected = 2 * 0.1 * 3e-3 / (MU_0 * 10)
        self.assertTrue(isclose(result.turns, expected, rel_tol=1e-12))
        self.assertTrue(isclose(result.turns, 150 / pi, rel_tol=1e-12))

    def test_coil_turns_invalid(self):
        with self.assertRaises(ValueError):
            coil_turns_for_center_field(field_t=3e-3, radius_m=0, current_a=10)
        with self.assertRaises(ValueError):
            coil_turns_for_center_field(field_t=3e-3, radius_m=0.1, current_a=0)

    def test_vector_field_magnitude_autocalculation(self):
        res = VectorFieldResult(bx=3.0, by=4.0)
        self.assertTrue(isclose(res.magnitude, 5.0, rel_tol=1e-12))


if __name__ == "__main__":
    unittest.main()
