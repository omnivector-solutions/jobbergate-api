# Use one shell for all commands in a target recipe
.ONESHELL:

.DEFAULT_GOAL 	:= help
SHELL 			:= /bin/bash
.PHONY			:= clean lint test help format


clean: # Remove .tox and build dirs
	rm -rf .tox/
	rm -rf venv/


format:
	isort setup.py jobbergate_api apps --skip-glob '*/[0-9][0-9][0-9][0-9]*.py'
	black setup.py jobbergate_api apps --exclude '\d{4}.*\.py'


help: # Display target comments in 'make help'
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


lint: # Run linter
	tox -e lint


test:
	tox -e unit
	# TODO: tox -e functional?


requirements/requirements.txt: setup.py
	python3 -m venv _virtual_tmp
	. _virtual_tmp/bin/activate \
		&& pip install wheel \
		&& pip install . \
		&& pip freeze > requirements/requirements.txt
	rm -rf _virtual_tmp
