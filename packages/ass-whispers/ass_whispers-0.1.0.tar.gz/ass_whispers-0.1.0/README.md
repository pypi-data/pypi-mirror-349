poetry install

poetry build
pip install dist/ass_whispers-0.1.0-py3-none-any.whl
poetry publish
