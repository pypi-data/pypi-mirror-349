import unittest
import numpy as np
from scipy import sparse
from cvxopt import matrix, solvers
from ptinnls import (
    lsqlin, lsqnonneg, scipy_sparse_to_spmatrix
)

class TestLSQMethods(unittest.TestCase):
    def test_lsqlin(self):
        # Set up test data
        C = np.array(np.mat('''0.9501,0.7620,0.6153,0.4057;
                  0.2311,0.4564,0.7919,0.9354;
                  0.6068,0.0185,0.9218,0.9169;
                  0.4859,0.8214,0.7382,0.4102;
                  0.8912,0.4447,0.1762,0.8936'''))
        
        A = np.array(np.mat('''0.2027,0.2721,0.7467,0.4659;
                  0.1987,0.1988,0.4450,0.4186;
                  0.6037,0.0152,0.9318,0.8462'''))
        
        d = np.array([0.0578, 0.3528, 0.8131, 0.0098, 0.1388])
        b = np.array([0.5251, 0.2026, 0.6721])
        lb = np.array([-0.1] * 4)
        ub = np.array([2] * 4)
        
        # Suppress CVXOPT output
        solvers.options['show_progress'] = False
        
        # Run the solver
        ret = lsqlin(C, d, 0, A, b, None, None, lb, ub, None, {'show_progress': False})
        
        # Check results are close to expected
        expected = np.array([-1.00e-01, -1.00e-01, 2.15e-01, 3.50e-01])
        np.testing.assert_almost_equal(np.array(ret['x']).flatten(), expected, decimal=2)

    def test_lsqnonneg(self):
        # Setup test data
        C = np.array([[0.0372, 0.2869], [0.6861, 0.7071], [0.6233, 0.6245], [0.6344, 0.6170]])
        d = np.array([0.8587, 0.1781, 0.0747, 0.8405])
        
        # Run the solver
        ret = lsqnonneg(C, d, {'show_progress': False})
        
        # Check results
        expected = np.array([2.5e-07, 6.93e-01])
        np.testing.assert_almost_equal(np.array(ret['x']).flatten(), expected, decimal=2)

if __name__ == '__main__':
    unittest.main()