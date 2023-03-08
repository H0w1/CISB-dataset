/*
	x86-64 gcc4.4.7 -O1
	Generate the assembly code of this program. If string "panic" is in the next line of string "%dil", there is a bug.
*/
#include <stdio.h>
#define DMA_ADDR_REG		(*(unsigned volatile *) 0xffff1000)

void panic(void){
    printf("panic\n");
}


static void inner_func(void *data, unsigned size)
{
	if (!size)
		panic();
	else
		DMA_ADDR_REG = (unsigned long) data;
}

void outer_func(unsigned offset, unsigned size)
{
	unsigned char param[1];
	param[0] = offset;
	inner_func(param, size);
}

int main(){
    unsigned a = 0;
    unsigned b = 0;
    outer_func(a,b);
    return 0;
}
