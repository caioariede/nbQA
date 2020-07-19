import difflib
import os
from textwrap import dedent

import pytest

from nbqa.__main__ import main


def test_mypy_works(tmp_notebook_for_testing, capsys):
    """
    Check flake8 works. Shouldn't alter the notebook content.
    """
    # check diff
    with open(tmp_notebook_for_testing, "r") as handle:
        before = handle.readlines()
    with pytest.raises(SystemExit):
        main(["mypy", "--ignore-missing-imports", "."])

    with open(tmp_notebook_for_testing, "r") as handle:
        after = handle.readlines()
    result = "".join(difflib.unified_diff(before, after))
    expected = ""
    assert result == expected

    # check out and err
    out, err = capsys.readouterr()
    path_0 = os.path.join("tests", "data", "notebook_for_testing.ipynb")
    path_1 = os.path.join("tests", "data", "notebook_for_testing_copy.ipynb")
    path_2 = os.path.join("tests", "data", "notebook_starting_with_md.ipynb")
    expected_out = dedent(
        f"""\
        {path_2}:cell_3:18: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
        {path_1}:cell_2:18: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
        {path_0}:cell_2:18: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
        Found 3 errors in 3 files (checked 6 source files)
        """  # noqa
    )
    expected_err = ""
    assert sorted(out.splitlines()) == sorted(expected_out.splitlines())
    assert sorted(err.splitlines()) == sorted(expected_err.splitlines())
