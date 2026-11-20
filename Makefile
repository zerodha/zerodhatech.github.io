ZOLA ?= zola

.PHONY: build check serve run-dev build-public-folder

build:
	$(ZOLA) build
	python3 scripts/taxonomy-feeds.py public

check:
	$(ZOLA) check --skip-external-links

serve:
	$(ZOLA) serve --drafts

run-dev: serve

build-public-folder: build
