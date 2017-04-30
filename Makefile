init:
	pip install -r requirements.txt

install:
	pip install .

develop:
	pip install -e .

uninstall:
	pip uninstall dotty

test:
	py.test tests

.PHONY: init test install develop uninstall
