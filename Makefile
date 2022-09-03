build:
	poetry build

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader
pyt:
	poetry run pytest page_loader