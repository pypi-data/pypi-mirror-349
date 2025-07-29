"""File test_linesearch.py

:author: Michel Bierlaire
:date: Thu Jun 22 16:04:39 2023

Tests for the linesearch module
"""

import unittest
import numpy as np

from biogeme_optimization.exceptions import (
    OptimizationError,
)  # Import the required exception class
from biogeme_optimization.linesearch import (
    line_search,
    newton_line_search,
    bfgs_line_search,
    DirectionManagement,
    NewtonDirection,
    InverseBfgsDirection,
)
from .examples import MyFunctionToMinimize, Example58, Rosenbrock


class TestDirectionManagement(unittest.TestCase):
    def test_abstract_class(self):
        fct = MyFunctionToMinimize(dimension=2)
        with self.assertRaises(TypeError):
            _ = DirectionManagement(function=fct)


class TestNewtonDirection(unittest.TestCase):
    def test_get_direction(self):
        fct = MyFunctionToMinimize(dimension=2)
        newton_direction = NewtonDirection(function=fct)
        iterate = np.array([1, 1])
        the_dir = newton_direction.get_direction(iterate)
        expected_dir = np.array([-1, -1])
        np.testing.assert_array_almost_equal(the_dir, expected_dir, decimal=6)

        optimal_solution = np.array([0, 0])
        the_dir = newton_direction.get_direction(optimal_solution)
        self.assertIsNone(the_dir)


class TestInverseBfgsDirection(unittest.TestCase):
    def test_get_direction(self):
        fct = MyFunctionToMinimize(dimension=2)
        inverse_bfgs_direction = InverseBfgsDirection(function=fct)
        iterate = np.array([1, 1])
        the_dir = inverse_bfgs_direction.get_direction(iterate)
        expected_dir = np.array([-1, -1])
        np.testing.assert_array_almost_equal(the_dir, expected_dir, decimal=6)

        iterate = np.array([0.5, 0.5])
        the_dir = inverse_bfgs_direction.get_direction(iterate)
        expected_dir = np.array([-0.5, -0.5])
        np.testing.assert_array_almost_equal(the_dir, expected_dir, decimal=6)

        optimal_solution = np.array([0, 0])
        the_dir = inverse_bfgs_direction.get_direction(optimal_solution)
        self.assertIsNone(the_dir)


class LineSearchTestCase(unittest.TestCase):
    def test_linesearch(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = 1.0
        beta1 = 1.0e-4
        beta2 = 0.99
        lbd = 2.0

        alpha = line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

        # Perform assertions to validate the output
        self.assertIsInstance(alpha, float)
        self.assertEqual(alpha, 1)

    def test_linesearch_wolfe_1(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = 1.0
        beta1 = 0.98
        beta2 = 0.99
        lbd = 2.0

        alpha = line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

        # Perform assertions to validate the output
        self.assertIsInstance(alpha, float)
        self.assertEqual(alpha, 0.03125)

    def test_linesearch_wolfe_2(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = 1.0e-10
        beta1 = 1.0e-5
        beta2 = 1.0e-4
        lbd = 2.0

        alpha = line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

        # Perform assertions to validate the output
        self.assertIsInstance(alpha, float)
        self.assertEqual(alpha, 1.7179869184)

    def test_linesearch_lambda_less_than_one(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = 1.0
        beta1 = 1.0e-4
        beta2 = 0.99
        lbd = 0.5

        with self.assertRaises(OptimizationError):
            line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

    def test_linesearch_alpha0_less_than_zero(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = -1.0
        beta1 = 1.0e-4
        beta2 = 0.99
        lbd = 2.0

        with self.assertRaises(OptimizationError):
            line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

    def test_linesearch_beta1_greater_than_beta2(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([-1.0, -1.0])
        alpha0 = 1.0
        beta1 = 0.99
        beta2 = 0.5
        lbd = 2.0

        with self.assertRaises(OptimizationError):
            line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

    def test_linesearch_non_descent_direction(self):
        fct = MyFunctionToMinimize(dimension=2)
        iterate = np.array([1.0, 1.0])
        descent_direction = np.array([1.0, 1.0])
        alpha0 = 1.0
        beta1 = 1.0e-4
        beta2 = 0.99
        lbd = 2.0

        with self.assertRaises(OptimizationError):
            line_search(fct, iterate, descent_direction, alpha0, beta1, beta2, lbd)

    def test_newton_linesearch(self):
        fct = MyFunctionToMinimize(dimension=2)

        # Set the starting point
        starting_point = np.array([2.0, 2.0])

        # Set the expected solution
        expected_solution = np.array([0.0, 0.0])

        # Call the newton_linesearch function
        optimization_results = newton_line_search(
            the_function=fct, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=1e-6
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = '),
        )
        self.assertTrue(optimization_results.convergence)

    def test_bfgs_linesearch(self):
        fct = MyFunctionToMinimize(dimension=2)

        # Set the starting point
        starting_point = np.array([2.0, 2.0])

        # Set the expected solution
        expected_solution = np.array([0.0, 0.0])

        # Call the newton_linesearch function
        optimization_results = bfgs_line_search(
            the_function=fct, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=1e-6
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = 0 <='),
        )

        self.assertTrue(optimization_results.convergence)

    def test_newton_linesearch_ex58(self):
        fct = Example58()

        # Set the starting point
        starting_point = np.array([1.0, 1.0])

        # Set the expected solution
        expected_solution = np.array([1.0, np.pi])

        # Call the newton_linesearch function
        optimization_results = newton_line_search(
            the_function=fct, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=1e-3
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = ')
        )
        self.assertTrue(optimization_results.convergence)

    def test_bfgs_linesearch_58(self):
        fct = Example58()

        # Set the starting point
        starting_point = np.array([1.0, 1.0])

        # Set the expected solution
        expected_solution = np.array([-1.0, 0])

        # Call the newton_linesearch function
        optimization_results = bfgs_line_search(
            the_function=fct, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=3e-3
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = '),
        )
        self.assertTrue(optimization_results.convergence)

    def test_newton_linesearch_rosenbrock(self):
        rosenbrock = Rosenbrock()
        # Set the starting point
        starting_point = np.array([-1.5, 1.5])

        # Set the expected solution
        expected_solution = np.array([1.0, 1.0])

        # Call the newton_linesearch function
        optimization_results = newton_line_search(
            the_function=rosenbrock, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=1e-3
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = '),
        )
        self.assertTrue(optimization_results.convergence)

    def test_bfgs_linesearch_rosenbrock(self):
        rosenbrock_2 = Rosenbrock()
        # Set the starting point
        starting_point = np.array([-1.5, 1.5])

        # Set the expected solution
        expected_solution = np.array([1.0, 1.00])

        # Call the newton_linesearch function
        optimization_results = bfgs_line_search(
            the_function=rosenbrock_2, starting_point=starting_point
        )

        # Check the solution
        np.testing.assert_allclose(
            optimization_results.solution, expected_solution, atol=3e-3
        )

        # Check the termination message
        self.assertTrue(
            optimization_results.messages['Cause of termination'].startswith('Relative gradient = '),
        )
        self.assertTrue(optimization_results.convergence)


if __name__ == '__main__':
    unittest.main()
