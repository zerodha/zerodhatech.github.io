build-dev-docker:
	docker build --target builder -t zerodha/zerodhatech:latest .

run-dev-docker:
	docker run -v "$(shell pwd)":/public \
			    -w /public \
			    -p 1313:1313 \
			    zerodha/zerodhatech:latest \
			    hugo serve -D --bind 0.0.0.0

build-public-folder-docker:
	docker run -v "$(shell pwd)":/public \
			-w /public \
			-p 1313:1313 \
			zerodha/zerodhatech:latest \
			hugo 

run-dev:
	hugo serve -D --bind 0.0.0.0

build-public-folder:
	hugo

.PHONY: build-dev-docker run-dev-docker build-public-folder-docker run-dev build-public-folder
