openopenings: main.py
	pyinstaller -F --add-data 'img/*png:img' main.py
	mv dist/main dist/openopenings

clean:
	rm -R dist build
	rm main.spec
