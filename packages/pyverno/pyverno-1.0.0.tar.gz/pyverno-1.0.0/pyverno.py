"""Python package version checker/updater

Usage:
    pyverno check PY_FILE GIT_TAG_REF
    pyverno update PY_FILE
"""
import re
import sys
from datetime import datetime, timezone

__version__ = '1.0.0'
V_EXPR = re.compile(r"""(^__version__\s*=\s*)(['"])(.+?)\2""", flags=re.M)


def main(argv=sys.argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd, *args = argv[1:]
    if cmd in COMMANDS:
        COMMANDS[cmd](*args)
    else:
        sys.exit(f"unknown command: {argv[1]}")


def check(py_file, ref=None):
    if ref is None:
        sys.exit("GIT_TAG_REF argument is required")
    if not ref.startswith("refs/tags/v"):
        sys.exit(f"unexpected ref: {ref}\nexpected: refs/tags/v...")
    tag_version = ref.removeprefix("refs/tags/v")
    pkg_version = parse_version(get_module_text(py_file), py_file)
    if tag_version != pkg_version:
        sys.exit(f"version mismatch: {tag_version} != {pkg_version}")


def update(py_file):
    """Add a timestamped dev version qualifier to the current version

    Do not pass a sha argument when updating the version for a PyPI release.
    PyPI error: The use of local versions ... is not allowed
    """
    devv = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    module_text = get_module_text(py_file)
    version = f"{parse_version(module_text, py_file)}.dev{devv}"
    print("new version:", version)
    with open(py_file, "w") as file:
        file.write(V_EXPR.sub(rf"\1\g<2>{version}\2", module_text))


def get_module_text(py_file):
    with open(py_file, "r") as file:
        return file.read()


def parse_version(module_text, py_file):
    match = V_EXPR.search(module_text)
    if not match:
        sys.exit(f"__version__ assignement not found in {py_file}")
    return match.group(3)


COMMANDS = {"check": check, "update": update}


if __name__ == "__main__":
    main()
