
.PHONY: clean

clean:
	-find . -name '*.pyc' -delete
	-find . -name '*~'    -delete
	-find . -name '*.pickle' -delete
