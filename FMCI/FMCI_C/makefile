
.PHONY: all clean

all: test_read_fmci_file.exe

read_fmci_file.o: read_fmci_file.c read_fmci_file.h
	$(CC)  -c -o $@ $< -std=c89

test_read_fmci_file.exe: %.exe : %.exe.c read_fmci_file.o
	$(CC)  -o $@ $^ -std=c89

clean:
	-rm -f *~
	-rm -f *.exe *.o *log
