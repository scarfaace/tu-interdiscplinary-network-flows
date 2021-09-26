export PYTHONPATH="$PYTHONPATH:./src/main/python:src/test/python"
python -c "import sys;print(sys.path)"
pytest -v