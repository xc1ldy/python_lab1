import typer

from toolkit.calculator import calculate
from toolkit.converter import convert as convert_value
from toolkit.errors import InvalidNumberError, ToolkitError

app = typer.Typer(help="Консольный калькулятор и конвертер величин.")


@app.command(context_settings={'ignore_unknown_options': True})
def calc(expression: str) -> None:
    """Вычислить выражение."""
    try:
        result = calculate(expression)
    except ToolkitError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=2)
    typer.echo(result)


@app.command(context_settings={'ignore_unknown_options': True})
def convert(value: str, from_unit: str = typer.Option(..., "--from"),
            to_unit: str = typer.Option(..., "--to")) -> None:
    """Сконвертировать величину между единицами."""
    try:
        try:
            numeric_value = float(value)
        except ValueError:
            raise InvalidNumberError(f"Неверное числовое значение: {value!r}")
        result = convert_value(numeric_value, from_unit, to_unit)
    except ToolkitError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=2)
    typer.echo(result)


if __name__ == "__main__":
    app()
