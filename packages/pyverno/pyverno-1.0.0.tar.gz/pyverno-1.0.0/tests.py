import pytest
import pyverno


def test_usage():
    with pytest.raises(SystemExit) as info:
        pyverno.main([])

    msg = str(info.value)
    assert '  pyverno check PY_FILE GIT_TAG_REF\n' in msg
    assert '  pyverno update PY_FILE\n' in msg


def test_check_without_ref():
    with pytest.raises(SystemExit) as info:
        pyverno.main(["pyverno", "check", "pyverno.py"])

    assert str(info.value) == "GIT_TAG_REF argument is required"


def test_check_bad_ref():
    with pytest.raises(SystemExit) as info:
        pyverno.main(["pyverno", "check", "pyverno.py", "refs/bad"])

    assert str(info.value) == "unexpected ref: refs/bad\nexpected: refs/tags/v..."


def test_check_version_mismatch():
    with pytest.raises(SystemExit) as info:
        pyverno.main(["pyverno", "check", "pyverno.py", "refs/tags/v1.0"])

    assert str(info.value) == f"version mismatch: 1.0 != {pyverno.__version__}"


def test_check_version_match():
    ref = f"refs/tags/v{pyverno.__version__}"
    pyverno.main(["pyverno", "check", "pyverno.py", ref])


def test_update_version(tmp_path):
    py_file = tmp_path / "__init__.py"
    with open(py_file, "w") as file:
        file.write('# module\n__version__ = "2025.05"# comment\n# comment\n')
    pyverno.main(["pyverno", "update", str(py_file)])

    with open(py_file, "r") as file:
        module_text = file.read()
        verno = pyverno.parse_version(module_text, str(py_file))
    assert verno.startswith("2025.05.dev")
    assert verno[len("2025.05.dev"):].isdigit()


def test_update_version_fail(tmp_path):
    py_file = tmp_path / "__init__.py"
    with open(py_file, "w") as file:
        file.write('# no version here\n\n#__version__ = "2025.05"\n')
    with pytest.raises(SystemExit) as info:
        pyverno.main(["pyverno", "update", str(py_file)])

    assert str(info.value) == f"__version__ assignement not found in {py_file}"


def test_unknown_command():
    with pytest.raises(SystemExit) as info:
        pyverno.main(["pyverno", "unknown", "arg"])

    assert str(info.value) == "unknown command: unknown"


def test_parse_version_fail():
    module_text = '__version__ = "1.0.0"'
    version = pyverno.parse_version(module_text, "pyverno.py")
    assert version == "1.0.0"

    with pytest.raises(SystemExit) as info:
        pyverno.parse_version("no version here", "pyverno.py")

    assert str(info.value) == "__version__ assignement not found in pyverno.py"
