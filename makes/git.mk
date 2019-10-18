git_push:
	git pull
	git push -u origin $(shell git rev-parse --abbrev-ref HEAD)