help:
	@egrep '^\w*:' Makefile

mkenv:
	# Use the venv builtin module to create a virtual environment also called venv.
	python3 -m venv venv

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt

lint:
	# Stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude setup.py,scrapenews/settings.py
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude setup.py,scrapenews/settings.py

lint-py3:
	# Check for PY3 compatibility.
	pylint --py3k scrapenews

unit:
	python -m unittest discover -s scrapenews/tests/unit -t scrapenews

test-iol:
	# Test a certain crawler without using the upload pipeline.
	# Note that is works from the project root because of how scrapy runs.
	scrapy crawl iol -s ITEM_PIPELINES="{}" -a since_lastmod=2018-01-01
