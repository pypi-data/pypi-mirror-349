import argparse
from argparse import Namespace
import pytest
from boj.args_resolver import (
    add_add_parser,
    add_random_parser,
    add_run_parser,
    add_submit_parser,
    validate_code_open,
    get_version,
)
from boj.args_resolver import add_login_parser
from boj.args_resolver import add_open_parser


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (
            ["add", "1234", "--type", "cpp", "-f"],
            Namespace(command="add", problem_id=1234, filetype="cpp", force=True),
        ),
        (
            ["add", "14500", "--type", "rs", "--force"],
            Namespace(command="add", problem_id=14500, filetype="rs", force=True),
        ),
        (
            ["add", "1919", "--type", "java"],
            Namespace(command="add", problem_id=1919, filetype="java", force=False),
        ),
    ],
)
def test_add_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_add_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (["login"], Namespace(command="login")),
    ],
)
def test_login_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_login_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (["open", "1234"], Namespace(command="open", problem_id=1234)),
        (["open", "14131"], Namespace(command="open", problem_id=14131)),
        (["open", "1020"], Namespace(command="open", problem_id=1020)),
    ],
)
def test_open_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_open_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (["random"], Namespace(command="random", tags=[], tier=None)),
        (
            ["random", "--tier", "g2..g5"],
            Namespace(command="random", tags=[], tier="g2..g5"),
        ),
        (
            ["random", "--tags", "dp", "math"],
            Namespace(command="random", tags=["dp", "math"], tier=None),
        ),
        (
            ["random", "--tags", "dp", "math", "--tier", "g1..g5"],
            Namespace(command="random", tags=["dp", "math"], tier="g1..g5"),
        ),
    ],
)
def test_random_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_random_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (
            ["run", "1234"],
            Namespace(command="run", problem_id=1234, timeout=10),
        ),
        (
            ["run", "1234", "--timeout", "123"],
            Namespace(command="run", problem_id=1234, timeout=123),
        ),
        (
            ["run", "1234", "--timeout", "129"],
            Namespace(command="run", problem_id=1234, timeout=129),
        ),
        (
            ["run", "1234", "-t", "129"],
            Namespace(command="run", problem_id=1234, timeout=129),
        ),
        (
            ["run", "1234", "-t", "9"],
            Namespace(command="run", problem_id=1234, timeout=9),
        ),
    ],
)
def test_run_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_run_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (
            ["submit", "1234"],
            Namespace(
                command="submit", problem_id="1234", open="onlyaccepted", timeout=30
            ),
        ),
        (
            ["submit", "1234"],
            Namespace(
                command="submit", problem_id="1234", open="onlyaccepted", timeout=30
            ),
        ),
        (
            ["submit", "1234", "--open", "open"],
            Namespace(command="submit", problem_id="1234", open="open", timeout=30),
        ),
        (
            ["submit", "1234", "--timeout", "123"],
            Namespace(
                command="submit", problem_id="1234", open="onlyaccepted", timeout=123
            ),
        ),
        (
            ["submit", "1234", "--timeout", "123", "--open", "close"],
            Namespace(command="submit", problem_id="1234", open="close", timeout=123),
        ),
    ],
)
def test_submit_command_parser(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_submit_parser(subparsers)
    assert parser.parse_args(test_in) == expected


@pytest.mark.parametrize(
    "test_in, expected",
    [
        (
            ["submit", "1234.cpp", "--open", "INVALID_OPTION"],
            Namespace(
                command="submit", file="1234.cpp", lang=None, open=None, timeout=123
            ),
        ),
    ],
)
def test_submit_command_parser_should_throw_system_exit(test_in, expected):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_submit_parser(subparsers)
    with pytest.raises(SystemExit) as e:
        parser.parse_args(test_in)

    assert e.type == SystemExit


@pytest.mark.parametrize(
    "test_in, expected",
    [
        ("INVALID_OPTION", None),
    ],
)
def test_validate_code_open_should_throw_value_error(test_in, expected):
    with pytest.raises(ValueError) as e:
        r = validate_code_open(test_in)
        print(r)

    assert e.type == ValueError


@pytest.mark.parametrize(
    "test_in, expected",
    [
        ("open", "open"),
        ("close", "close"),
        ("onlyaccepted", "onlyaccepted"),
    ],
)
def test_validate_code_open(test_in, expected):
    assert validate_code_open(test_in) == expected


def test_get_version():
    assert get_version().startswith("boj-cli")
