all: install
	cd src/
	make

install:
	git pull

restore:
	cd src/
	make restore

