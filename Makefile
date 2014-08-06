all:
	python -c "import inspect; import inspector; print inspect.getdoc(inspector)" > README.md
	pandoc -o README.rst README.md

upload:
	python setup.py sdist upload