/*
	x86-64clang 3.0.0-14.0.0 -O1
	Generate the disassembly code of this program, if the section "<main>:" contains "memset", it means the compiler changes the assignments to memset, so there is a bug.
*/

#include<stdio.h>

unsigned int a[100];

int main() {
    for (int i = 0; i < 100; ++i) {
        a[i] = 0x11111111;
    }
    return 0;
}
