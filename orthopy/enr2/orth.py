# -*- coding: utf-8 -*-
#
from __future__ import division, print_function

import numpy
import scipy.special

from ..line.recurrence_coefficients import hermite


# pylint: disable=too-many-locals
def tree(n, X, symbolic=False):
    p0, a, b, c = hermite(n+1, 'normal', symbolic=symbolic)

    dim = X.shape[0]

    p0n = p0 ** dim
    out = []

    level = numpy.array([numpy.ones(X.shape[1:], dtype=int) * p0n])
    out.append(level)

    # TODO use a simpler binom implementation
    for L in range(n):
        level = []
        for i in range(dim-1):
            m1 = int(scipy.special.binom(L+dim-i-1, dim-i-1))
            if L > 0:
                m2 = int(scipy.special.binom(L+dim-i-2, dim-i-1))
            r = 0
            for k in range(L+1):
                m = int(scipy.special.binom(k+dim-i-2, dim-i-2))
                val = out[L][-m1:][r:r+m] * (a[L-k] * X[i] - b[L-k])
                if L-k > 0:
                    val -= out[L-1][-m2:][r:r+m] * c[L-k]
                r += m
                level.append(val)

        # treat the last one separately
        val = out[L][-1] * (a[L] * X[-1] - b[L])
        if L > 0:
            val -= out[L-1][-1] * c[L]
        level.append([val])

        out.append(numpy.concatenate(level))

    return out
