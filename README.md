# Лабораторная работа №1. Консольный набор утилит

Python-пакет с CLI, содержащий калькулятор и конвертер величин.

## Структура проекта

python_lab1/
├── pyproject.toml
├── requirements.txt
├── README.md
├── .pre-commit-config.yaml
├── src/toolkit/
│ ├── init.py
│ ├── main.py # CLI на Typer: команды calc и convert
│ ├── calculator.py # tokenize -> _Parser -> calculate
│ ├── converter.py # convert(): длина / масса / температура
│ └── errors.py # ToolkitError и подклассы
└── tests/
├── test_calculator.py
├── test_converter.py
└── test_cli.py


## Установка

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
pip install pytest ruff mypy pre-commit
pre-commit install
```

## Использование

```bash
python -m toolkit calc "2 + 3 * 4"
python -m toolkit convert 1000 --from mm --to m
python -m toolkit --help
```

Успешная команда завершается кодом `0` и печатает результат в stdout.
Ошибка печатается в stderr, код завершения — `2`.

## Тесты

24 теста в `tests/`, из них 8+ негативных (проверяют, что при некорректном
вводе поднимается нужная ошибка) и 4 CLI-теста (проверяют команды `calc`
и `convert` через `typer.testing.CliRunner`, без запуска subprocess).

```bash
python -m pytest
```

## Проверка

```bash
python -m pytest
ruff check .
pre-commit run --all-files
```

## Дизайн

- Вычисление выражения разделено на три шага: `tokenize` → `_Parser` →
  результат. Не используются `eval`, `exec`, `ast.literal_eval`.
- Все ошибки — подклассы `ToolkitError` (`errors.py`).
- CLI построен на Typer: каждая команда — функция с `@app.command()`,
  типы аргументов Typer определяет по аннотациям.
- Конвертер приводит длину к метрам, массу — к граммам, температуру —
  к Цельсию, и уже оттуда переводит в целевую единицу.
