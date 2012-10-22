
.PHONY: all clean

all: test_fmci.exe

fmci.o: fmci.c fmci.h
	$(CC)  -c -o $@ $< -std=c89

test_fmci.exe: %.exe : %.exe.c fmci.o
	$(CC)  -o $@ $^ -std=c89

clean:
	-rm -f *~
	-rm -f *.exe *.o *log
