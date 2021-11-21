all: csort jsort
.PHONY: all

csort: 
	gcc csort.c -o csort -pthread
	
csortso:
	gcc -Wall -fPIC -c *.c
	gcc -shared -Wl,-soname,csort.so -o csort.so *.o
jsort:
	javac JSort.java Merger.java Sorter.java
clean:
	rm -f csort csort.o csort.so JSort.class Merger.class Sorter.class
