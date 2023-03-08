/*
	successful
	x86-64 gcc 4.1-12.0.1 -O1
	x86-64 clang 3.0.0-14.0.0 -O1
	Compile and run, if "buffer is NULL for second time", there is a bug
*/
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
static char*  const kern_buff_p;

void hello_start()
{

 if(!kern_buff_p)
        printf("buffer is NULL for first time \n");

  *((char**)(unsigned long int)((&kern_buff_p)))=(char*)malloc(10);

 if(!kern_buff_p)
        printf("buffer is NULL for second time \n");
}

int main(){
    hello_start();
}