
all: libcigaleLAMB.so

libcigaleLAMB.so: cigLAMB.c
	gcc -fPIC -shared -o libcigaleLAMB.so cigLAMB.c
	
clean:
	rm libcigaleLAMB.so
