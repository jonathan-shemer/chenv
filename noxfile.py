"""Nox sessions."""
import nox
import nox_poetry.patch  # noqa: F401
from nox.sessions import Session  # noqa: I100


package = "chenv"
nox.options.sessions = "lint", "safety", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install(".")
    session.install("black")
    session.run("black", *args)


@nox.session(python=["3.8"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(".")
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    session.install(".")
    session.install("safety")
    session.run("safety", "check", "--full-report")


@nox.session(python=["3.8"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install(".")
    session.install("mypy")
    session.run("mypy", "--ignore-missing-imports", *args)


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install(".")
    session.install("pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.install(".")
    session.install("coverage", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.install(".")
    session.install("pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.8"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install(".")
    session.install("coverage", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
