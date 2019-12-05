
#include "cigale.h"

#include <sys/types.h>
# include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

struct cigale  *c;
struct image   *it;
#define SHM_PERMCIG 0666
//long a64l();

/*
 * c = (struct cigale *)open_seg(suf, sizeof(*c));
 */

//------------------------------
unsigned long cig_len(int x, int y, int n){
	
	//return (x * y * n * sizeof(cig_int) + 100);
	return (x * y * n * sizeof(cig_int));
}

//------------------------------
char * open_seg(char *suf){
	
	key_t           key;
	int             dim;
	char           *shma;
	char            s[6];
	struct shmid_ds *buf;
	int             shmid,
	                t;

	suf += 2;
	s[0] = *suf;
	suf += 2;
	s[1] = *suf++;
	s[2] = *suf++;
	s[3] = *suf++;
	s[4] = *suf;
	s[5] = 0;
	printf("apertura del segmento %s \n", s);
	key = a64l(s);
	shmid = shmget(key, 0, SHM_R | SHM_W);
	printf("retour %x \n", shmid);
	if (shmid == -1)
		exit(printf("error de apertura \n"));
	shma = (char *) shmat(shmid, 0, 0);
	if (shma == (char *)-1)
		exit(printf("error  %d\n", errno));
	printf("direccion %p \n", shma);
	return (shma);
}

long
a64l(s)
	const char *s;
{
	long value, digit, shift;
	int i;

	value = 0;
	shift = 0;
	for (i = 0; *s && i < 6; i++, s++) {
		if (*s <= '/')
			digit = *s - '.';
		else if (*s <= '9')
			digit = *s - '0' + 2;
		else if (*s <= 'Z')
			digit = *s - 'A' + 12;
		else
			digit = *s - 'a' + 38; 

		value |= digit << shift;
		shift += 6;
	}

	return (long) value;
}

void swapelc(char *it, int n){
	int i;
	char c;
	i=sizeof(n)*n;
	while((i-=4)>=0){
		c=it[i+3];
		it[i+3]=it[i];
		it[i]=c;
		c=it[i+2];
		it[i+2]=it[i+1];
		it[i+1]=c;
	}
}


#define IDIM 2048

void unpack_new (int id, int it[], int nv)
//cig_int it[];
{
    int fl[IDIM];
    int kl, i, l, m, ibid;
    int ind = 0, ipr = 0, index = 0, ret = -1;
    
    static int jt[] = {13,  9,  7,  6,  5,  4,  3,  2  , 1};
    static int kt[] = {2,  3,  4,  5,  6,  7, 10, 14  , 25};
    static int la[] = {0xfc000000, 0xf8000000, 0xf0000000, 
                       0xc0000000, 0xc0000000, 0xf0000000, 
                       0xc0000000, 0xf0000000, 0xfe000000};
    static int lt[] = {0x04000000, 0x08000000, 0x10000000, 
                       0x40000000, 0x80000000, 0x20000000, 
                       0xc0000000, 0x30000000, 0x02000000};
    static int  ma[] = {3, 7, 15, 31, 63, 127, 1023, 16383, 33554431};
    static int  mi[] = {1, 3,  7, 15, 31,  63, 511, 8191, 16777216};
    static int  mt[] = {4, 8, 16, 32, 64, 128, 1024, 16384, 33554432};
    
    for (ibid=0;ind<nv ;ibid++ ) {
        ret = read(id,fl,IDIM)/4;

        swapelc((char *)fl, ret);

        if(ret==0){
            fl[0]=nv-ind;
            ret=1;
            ipr=0;
        }
        
        for(index = 0; index < ret;){
            kl = fl[index];
            for(i = 0; i < 9; i++) {
                if ((kl & la[i]) == lt[i]) {
                    for (l = 0; l < jt[i]; l++) {
                        m = kl & ma[i];
                        kl = kl >> kt[i];
                        if (m <= mi[i])
                            ipr += m;
                        else
                            ipr += m - mt[i];
                        it[ind] = ipr;
                        ind++;
                    }
                    goto suite;
                }
            }
            
            for (l = 0; l < (kl & 0x01ffffff); l++) {
                it[ind] = ipr;
                ind++;
            }
suite:  
        index++;
        }
    }
}
















