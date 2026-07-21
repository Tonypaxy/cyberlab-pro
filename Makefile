.PHONY: install run clean test

install:
	python3 setup.py

run:
	export DISPLAY=:0 && python3 launcher.py

test:
	python3 -c "from launcher import CyberLabApp; print('OK')"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf logs/*.log tmp/* cache/*

desktop:
	cp cyberlab.desktop ~/.local/share/applications/

termux-install:
	pkg install python-tkinter termux-api -y
	python3 setup.py

linux-install:
	sudo apt install python3-tk -y
	bash install_linux.sh
