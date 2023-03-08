/*
	x86-64 gcc 4.1.2-12.0.1 -O0
	x86-64 clang 3.0.0-14.0.0 -O0
	Compile and run the program, if the result is 16, it means the struct is reordered, so there is a bug.
*/

#include<stdio.h>

struct foo {
    char a;
    int b;
    short c;
    int d;
};

int main() {
    printf("%ld", sizeof(struct foo));
    return 0;
}