help:
	@egrep '.*:$$' Makefile

new-env:
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

unit:
	python -m unittest discover -s scrapenews/tests/unit -t scrapenews

test-iol:
	scrapy crawl -s ITEM_PIPELINES="{}" -a since_lastmod=2018-01-01 iol

test-help:
	@echo 'scrapy crawl -s ITEM_PIPELINES="{}" -a since_lastmod=2018-01-01 <CRAWLER>'

list:
	@scrapenews/utils/list_spiders.py
