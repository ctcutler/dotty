init:
	pip install -r requirements.txt

test:
	py.test test_dotty.py

.PHONY: init test
