# tests/test_cli.py

import pytest
from typer.testing import CliRunner

from {{ project_slug }}.cli import app # Import your Typer app
from {{ project_slug }} import __version__

runner = CliRunner()

# Test the main app help message
def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: {{ project_slug }}" in result.stdout
    assert "{{ project_description | default('A cool CLI application built with Typer.') }}" in result.stdout
    assert "example" in result.stdout # Check if subcommand is listed

# Test the version callback
def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{{ project_name }} CLI Version: {__version__}" in result.stdout

# Test the 'example hello' command
def test_example_hello_default():
    result = runner.invoke(app, ["example", "hello"])
    assert result.exit_code == 0
    assert "Hello there!" in result.stdout

def test_example_hello_with_name():
    result = runner.invoke(app, ["example", "hello", "--name", "Tester"])
    assert result.exit_code == 0
    assert "Hey Tester!" in result.stdout

def test_example_hello_with_name_formal():
    result = runner.invoke(app, ["example", "hello", "--name", "Dr. Tester", "--formal"])
    assert result.exit_code == 0
    assert "How do you do, Dr. Tester?" in result.stdout

# Test the 'example goodbye' command
def test_example_goodbye_default():
    result = runner.invoke(app, ["example", "goodbye"])
    assert result.exit_code == 0
    assert "Farewell, World!" in result.stdout

def test_example_goodbye_with_name():
    result = runner.invoke(app, ["example", "goodbye", "Alice"])
    assert result.exit_code == 0
    assert "Farewell, Alice!" in result.stdout

def test_example_goodbye_with_time():
    result = runner.invoke(app, ["example", "goodbye", "Bob", "--show-time"])
    assert result.exit_code == 0
    assert "Farewell, Bob!" in result.stdout
    assert "The time is now" in result.stdout # Check for the time string part

# Test that giving just 'example' without a subcommand shows its help
def test_example_subcommand_help():
    result = runner.invoke(app, ["example", "--help"]) # or just ["example"]
    assert result.exit_code == 0
    assert "Usage: {{ project_slug }} example [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "hello" in result.stdout
    assert "goodbye" in result.stdout 