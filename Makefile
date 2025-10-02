PY ?= python
PIP ?= $(PY) -m pip

.PHONY: venv install test lint run-pyqt run-tk hooks

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip

install:
	. .venv/bin/activate && $(PIP) install -r requirements.txt

test:
	QT_QPA_PLATFORM=offscreen . .venv/bin/activate && pytest -q

run-pyqt:
	. .venv/bin/activate && $(PY) GUI_pyqt6_WINFF.py

run-tk:
	. .venv/bin/activate && $(PY) GUI_tkinter_WINFF.py

hooks:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit
	@echo "Git hooks installed."
