from typer.testing import CliRunner

from toolkit.__main__ import app

runner = CliRunner()

def test_cli_calc_success() -> None:
    result = runner.invoke(app, ["calc", "2 + 3"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "5"

def test_cli_convert_success() -> None:
    result = runner.invoke(app, ["convert", "1000", "--from", "mm", "--to", "m"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "1.0"

def test_cli_calc_error() -> None:
    result = runner.invoke(app, ["calc", ""])
    assert result.exit_code == 2
    assert "Error" in result.output

def test_cli_convert_error() -> None:
    result = runner.invoke(app, ["convert", "abc", "--from", "mm", "--to", "m"])
    assert result.exit_code == 2
