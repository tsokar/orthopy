# -*- coding: utf-8 -*-
#
from __future__ import division

import numpy
import sympy


# pylint: disable=too-many-arguments
def orth_tree(n, bary, standardization):
    '''Evaluates the entire tree of orthogonal triangle polynomials.

    The return value is a list of arrays, where `out[k]` hosts the `2*k+1`
    values of the `k`th level of the tree

        (0, 0)
        (0, 1)   (1, 1)
        (0, 2)   (1, 2)   (2, 2)
          ...      ...      ...

    For reference, see

    Abedallah Rababah,
    Recurrence Relations for Orthogonal Polynomials on Triangular Domains,
    Mathematics 2016, 4(2), 25,
    <https://doi.org/10.3390/math4020025>.
    '''
    if standardization == '1':
        return _standardization_1(n, bary)

    assert standardization == 'normal'
    return _standardization_normal(n, bary)


def _standardization_1(n, bary):
    out = [numpy.full(bary.shape[1:], 1.0)]

    def alpha(n, r):
        return n*(2*n+1) / (n-r) / (n+r+1)

    def beta(n, r):
        return n * (2*r+1)**2 / (n-r) / (n+r+1) / (2*n-1)

    def gamma(n, r):
        return (n-r-1) * (n+r) * (2*n+1) / (n-r) / (n+r+1) / (2*n-1)

    u, v, w = bary

    if n > 0:
        L = 1
        out.append([
            (alpha(L, 0) * (1-2*w) - beta(L, 0)) * out[0][0],
            (2*L-1)/L * (u-v) * out[0][0],
            ])

    for L in range(2, n+1):
        out.append([
            + (alpha(L, r) * (1-2*w) - beta(L, r)) * out[L-1][r]
            - gamma(L, r) * out[L-2][r]
            for r in range(L-1)
            ] +
            [
            (alpha(L, L-1) * (1-2*w) - beta(L, L-1)) * out[L-1][L-1]
            ] +
            [
            + (2*L-1)/L * (u-v) * out[L-1][L-1]
            - (L-1)/L * (u+v)**2 * out[L-2][L-2]
            ]
            )
    return out


def _standardization_normal(n, bary):
    '''The coefficients here are based on the insight that

      int_T P_{n, r}^2 =
          int_0^1 L_r^2(t) dt * int_0^1 q_{n,r}^2(w) (1-w)^(r+s+1) dw.

    For reference, see
    page 219 (and the reference to Gould, 1972) in

     Farouki, Goodman, Sauer,
     Construction of orthogonal bases for polynomials in Bernstein form
     on triangular and simplex domains,
     Computer Aided Geometric Design 20 (2003) 209–230.

    From this, one gets

      int_T P_{n, r}^2 = 1 / (2*r+1) / (2*n+2)
          sum_{i=0}^{n-r} sum_{j=0}^{n-r}
              (-1)**(i+j) * binom(n+r+1, i) * binom(n-r, i)
                          * binom(n+r+1, j) * binom(n-r, j)
                          / binom(2*n+1, i+j)

    The Legendre integral is 1/(2*r+1) and, astonishingly, the double sum
    is always 1, hence

      int_T P_{n, r}^2 = 1 / (2*r+1) / (2*n+2).
    '''
    def alpha(n, r):
        return sympy.Rational(2*n+1, (n-r) * (n+r+1)) * sympy.sqrt((n+1)*n)

    def beta(n, r):
        return sympy.Rational((2*r+1)**2, (n-r) * (n+r+1) * (2*n-1)) \
            * sympy.sqrt((n+1)*n)

    def gamma(n, r):
        return sympy.Rational(
            (n-r-1) * (n+r) * (2*n+1),
            (n-r) * (n+r+1) * (2*n-1)
            ) * sympy.sqrt(sympy.Rational(n+1, n-1))

    def delta(n):
        return sympy.sqrt(sympy.Rational((2*n+1) * (n+1) * (2*n-1), n**3))

    def epsilon(n):
        return sympy.sqrt(sympy.Rational(
            (2*L+1) * (L+1) * (L-1), (2*L-3) * L**2
            ))

    out = [[numpy.full(bary.shape[1:], sympy.sqrt(2))]]

    u, v, w = bary

    if n > 0:
        L = 1
        out.append([
            out[0][0] * (alpha(L, 0) * (1-2*w) - beta(L, 0)),
            out[0][0] * (u-v) * delta(L),
            ])

    for L in range(2, n+1):
        out.append([
            + out[L-1][r] * (alpha(L, r) * (1-2*w) - beta(L, r))
            - out[L-2][r] * gamma(L, r)
            for r in range(L-1)
            ] +
            [
            out[L-1][L-1] * (alpha(L, L-1) * (1-2*w) - beta(L, L-1))
            ] +
            [
            + out[L-1][L-1] * (u-v) * delta(L)
            - out[L-2][L-2] * (u+v)**2 * epsilon(L)
            ]
            )
    return out
