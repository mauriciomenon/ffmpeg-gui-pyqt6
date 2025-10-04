PY ?= python
PIP ?= $(PY) -m pip

.PHONY: venv install test lint run-pyqt run-tk hooks build-macos build-windows clean-build

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip

install:
	. .venv/bin/activate && $(PIP) install -r requirements.txt

test:
	QT_QPA_PLATFORM=offscreen . .venv/bin/activate && PYTHONPATH=. pytest tests/ -q

run-pyqt:
	. .venv/bin/activate && $(PY) GUI_pyqt6_WINFF.py

run-tk:
	. .venv/bin/activate && $(PY) GUI_tkinter_WINFF.py

hooks:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit
	@echo "Git hooks installed."

build-macos:
	. .venv/bin/activate && $(PY) build_macos.py

build-windows:
	. .venv/bin/activate && $(PY) build_windows.py

clean-build:
	rm -rf build/ dist/ *.spec *.dmg *.zip version_info.txt
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Build artifacts cleaned."
