from subprocess import check_call


def hooks():
    check_call(["pre-commit", "run", "--all-files"])


def format():
    check_call(["black", "."])
    check_call(["isort", "."])


def lint():
    check_call(["pylint", "src", "tests"])
    check_call(["mypy", "src", "tests"])


def test():
    check_call(["pytest"])


def test_cov_term():
    check_call(
        [
            "pytest",
            "--cov=src",
            "--cov-branch",
            "--cov-report=term-missing",
        ]
    )


def test_cov_html():
    check_call(
        [
            "pytest",
            "--cov=src",
            "--cov-branch",
            "--cov-report=html",
        ]
    )
