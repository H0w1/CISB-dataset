/*
	x86-64gcc 4.1.2 -O0 9.1-12.0.1  -O1
	x86-64clang 3.3 - 14.0.0   -O1
	Compile and run the program, if the result isn't "ok", it means the check "if (!&t->b)" is remove, so there is a bug.
*/
#include<stdio.h>

struct ccc{
    int a;
    int b;
} c;

__attribute__((noinline))
int test(struct ccc *t) {
    //printf("%d", &t->b);
    if (!&t->b) {
        printf("ok");
    }
    return 0;
}

int main() {
    test((struct ccc *)0xfffffffffffffffc);
    return 0;
}

