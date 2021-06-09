#!/bin/bash
echo "Переключаюсь на виртуалное окружение env369..."
. env38/bin/activate
echo "...готово."
echo "Устанавливаю poetry через curl..."
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
echo "...готово."
echo "Перехожу в папку videorender..."
cd videorender
echo "...запускаю poetry..."
poetry install
echo "...зависимости установлены через poetry."
echo "Выхожу..."
cd ..
