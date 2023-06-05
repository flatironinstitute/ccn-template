# Tests

Use [pytest](https://docs.pytest.org/en/), under `tests/`, all scripts must start with `test_*py`, and all classes/functions start with `Test` / `test_`. Aim to have as complete coverage as possible.

Tests should be written as code as written, PRs should not be merged unless the new functionality is tested. Tests should be started as soon as possible.

Tests should include testing compatibility with other packages, even if they're not strict requirements. e.g., check that code objects can be used by scikit-learn's cross-validation procedure.
