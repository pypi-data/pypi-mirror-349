# typically

Types, data(types), and utilities (for types) that are *typically* used at some point in most of the projects I work on.

The goal is to minimize the number of required dependencies, reimplementing permissively licensed code in this project if required. Currently, the dependencies are:

- [pydantic](https://github.com/pydantic/pydantic)
- [orjson](https://github.com/ijl/orjson)

## Integrated Packages

### [MIT] [python-case-converter](https://github.com/chrisdoherty4/python-case-converter)

Changes:

- Some modifications made to allow for subclasses of `str` for which the constructor sets the relevant case.
- Additional cases added.
- Type annotations added where missing.
- Other assorted modifications.
- Log statements removed.
- Parametrized whitespace delimiters.

<!--
Maybe will add, but probably split into separate project:

- [cryptography](https://github.com/pyca/cryptography)
- [scipy](https://github.com/scipy/scipy)
- [sympy](https://github.com/sympy/sympy)
- [numpy](https://github.com/numpy/numpy)

## References

- [superstring]()
- [adict]()

-->
Ö