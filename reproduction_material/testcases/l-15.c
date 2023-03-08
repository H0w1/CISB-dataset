/*
	x86-64 gcc4.4-12.0.1 -O1
	x86-64 clang3.0.0-14.0.0 -O1
	Compile and get disassembly code of this program. If section "<main>:" doesn't contains instruction "memset", "memset" is deleted, so there is a bug.
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>

int main() {
    char* a = (char*)malloc(100);
    // scanf("%s",a);
    printf("%s",a);
    memset(a,0,100);
    return 0;
}