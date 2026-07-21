.PHONY: run install clean test

run:
	bash run.sh

linux:
	bash run_linux.sh

install:
	python3 setup.py

test:
	python3 -c "from launcher import CyberLabApp; print('Import OK')"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf logs/*.log tmp/* cache/*

update:
	git pull

push:
	git add -A && git commit -m "Update" && git push
