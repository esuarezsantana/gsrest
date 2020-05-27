.PHONY: default ci edit tests install edit pytest \
	docs docs-html docs-autogen docs-coverage docs-server docs-clean \
	interrogate docker-start docker-stop license-headers \
	bump-patch bump-minor bump-major publish

SELF = gsrest
DOC_HTTP_PORT = 9000
# GEOSERVER_VERSION = 2.15.5

PROGRAM_NAME = GsRest
# omit last period, because GPL-v3 template adds extra period.
LICENSE_OWNER = Instituto Tecnológico de Canarias, S.A
PROGRAM_HOMEPAGE = https://github.com/esuarezsantana/gsrest

default: ci

ci: docs interrogate tests

# tests: geoserver-start pytest geoserver-stop
tests: pytest

# install may be required for sphinx to find the $(SELF) package
# try:
#     $ poetry run python -c 'import mypackage'
install:
	poetry install

edit:
	poetry run $(EDITOR) .

pytest:
	poetry run pytest --cov=$(SELF)

docs: install docs-html docs-coverage

# html now already includes autogen
docs-html:
	poetry run $(MAKE) -C docs html

# docs-autogen: install
docs-autogen:
	poetry run $(MAKE) -C docs autogen

docs-coverage:
	poetry run $(MAKE) -C docs coverage

docs-server:
	python -m http.server -d docs/build/html $(DOC_HTTP_PORT)

docs-clean:
	-rm docs/build/* -rf
	-rm docs/source/autogen/* -rf

# docstring coverage
interrogate:
	-poetry run interrogate -Impsvv $(SELF)

# geoserver docker container is started/stopped by pytest automatically
# these targets are just in case you want to do it manually
docker-start:
	docker-compose -f tests/docker-compose.yml up -d

docker-stop:
	docker-compose -f tests/docker-compose.yml down

license-headers:
	for license_dir in gsrest tests; do \
		poetry run licenseheaders \
			-t helper/licenseheaders-gpl-v3.tmpl -d $$license_dir \
			-n "$(PROGRAM_NAME)" -o "$(LICENSE_OWNER)" \
			-u "$(PROGRAM_HOMEPAGE)" -y 2020 ; \
	done

bump-patch:
	poetry run bump2version patch

bump-minor:
	poetry run bump2version minor

bump-major:
	poetry run bump2version major

publish:
	poetry check && poetry build && poetry publish
