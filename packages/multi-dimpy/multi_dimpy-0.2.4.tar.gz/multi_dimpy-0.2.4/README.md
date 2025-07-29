# Overview

[![PyPI - Version](https://img.shields.io/pypi/v/multi-dimpy)](https://pypi.org/project/multi-dimpy/)
[![Read the Docs](https://img.shields.io/readthedocs/multi-dimpy)](https://multi-dimpy.readthedocs.io/en/latest/)

Everyone knows you can't add apples and oranges.<br>
Most people also know you can't add meters and seconds.<br>
But sometimes people do—accidentally, when it's hidden in code or in matrix computations.

Models and algorithms with dimensional inconsistencies might still yield decent results, but they don't make physical sense, and a change of units results in a change to the output, when units shouldn't make a difference.

Software packages for managing dimensions already exist, but they lack the ability to do **dimensioned linear algebra**—they mostly just work with scalar values.
So as a first go and a proof-of-concept, this package wraps NumPy and tracks physical dimensions of $n$-dimensional arrays using theory developed in the book *Multidimensional Analysis* (citation below).

Hart, G. W. (1995). Multidimensional Analysis: Algebras and Systems for Science and Engineering. Springer-Verlag.
