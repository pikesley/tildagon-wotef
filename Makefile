APP = $(shell basename $$(pwd))

all: format test clean

push:
	python scripts/pusher.py

slim-push:
	python scripts/pusher.py slim-includes

connect:
	python -m mpremote

deploy: push connect

convert-conf:
	@python scripts/conf_yaml_to_json.py

format:
	ruff format
	ruff check --fix

generate:
	python tools/cropper.py
	python tools/bitmapper.py
	python tools/slimmer.py
	python tools/encoder.py
	PYTHONPATH=common python tools/rainbow.py

clean-sources:
	rm -fr sources/bitmaps/
	rm -fr sources/crops/
	rm -fr sources/encoded/
	rm -fr sources/slimmed_bitmaps/

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;
	@find . -depth -name .DS_Store -exec rm -fr {} \;

test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

install: guard-LIBRARY
	mkdir -p pikesley
	rsync --archive --verbose --exclude tests ../pikesley/${LIBRARY} pikesley/

build:
	docker build \
		--build-arg APP=${APP} \
		--tag ${APP} .

run:
	docker run \
		--name ${APP} \
		--hostname ${APP} \
		--volume $(shell pwd):/opt/${APP} \
		--interactive \
		--tty \
		--rm \
		${APP} \
		bash

guard-%:
	@if [ -z "${${*}}" ] ; \
    then \
        echo "You must provide the ${*} variable" ; \
        exit 1 ; \
    fi

-include Makefile.local
