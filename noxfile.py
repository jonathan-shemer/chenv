"""Nox sessions."""
import nox
from nox.sessions import Session
import nox_poetry


package = "chenv"
nox.options.sessions = "lint", "safety", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "black")
    session.run("black", *args)


@nox.session(python=["3.8"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    nox_poetry.install(session, ".")
    nox_poetry.install(
        session,
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
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "safety")
    session.run("safety", "check", "--full-report")


@nox.session(python=["3.8"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "mypy")
    session.run("mypy", "--ignore-missing-imports", *args)


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "coverage", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.8"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "coverage", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    nox_poetry.install(session, ".")
    nox_poetry.install(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
