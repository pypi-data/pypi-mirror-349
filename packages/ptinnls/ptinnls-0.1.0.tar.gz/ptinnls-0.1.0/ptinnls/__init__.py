# -*- coding: utf-8 -*-

#!/usr/bin/python
 
# See http://maggotroot.blogspot.ch/2013/11/constrained-linear-least-squares-in.html for more info
'''
    A simple library to solve constrained linear least squares problems
    with sparse and dense matrices. Uses cvxopt library for 
    optimization
'''
 
__author__ = 'Valeriy Vishnevskiy'
__email__ = 'valera.vishnevskiy@yandex.ru'
__version__ = '1.0'
__date__ = '22.11.2013'
__license__ = 'WTFPL'

import numpy as np
from cvxopt import solvers, matrix, spmatrix, mul
from scipy import sparse
from scipy.optimize import nnls

# Import and expose the methods
from .methods import (
    scipy_sparse_to_spmatrix,
    spmatrix_sparse_to_scipy,
    sparse_None_vstack,
    numpy_None_vstack,
    numpy_None_concatenate,
    get_shape,
    numpy_to_cvxopt_matrix,
    cvxopt_to_numpy_matrix,
    lsqlin,
    lsqnonneg
)