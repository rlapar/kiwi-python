Python Weekend
===================

# Usage

```
python3 book_flight.py [OPTION]

Options:
  --date TEXT         Date of departure.  [required]
  --from TEXT         IATA code from.  [required]
  --to TEXT           IATA code to.  [required]
  --bags INTEGER      Luggage quantity.
  --return INTEGER    Nights in destination.
  --cheapest          Book the cheapest flight.
  --fastest           Book the fastest flight.
  --one-way           Book one way ticket.
  --warn / --no-warn  Show warning and error messages.
  --help              Show this message and exit.
```
# Tests

Tests for CLI are available running command `python3 tests.py`. Command-line options are identical to unittest package ones (https://docs.python.org/2/library/unittest.html#command-line-options).

**Author**: Radovan Lapár