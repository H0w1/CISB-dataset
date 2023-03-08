// https://github.com/torvalds/linux/commit/02828845dda5ccf921ab2557c6ca17b6e7fc70e2
#include <stdio.h>
#define prefetch(ptr)				\
	({					\
		__asm__ __volatile__(		\
		"PREFETCHNTA \t%0"			\
		:				\
		: "o" (*(char *)(ptr))		\
		: "cc");			\
	})

void bar(char *x) {
    printf("%c",*x);
}

void foo(char *x)
{
	prefetch(x);
	if (x)                  //  x86-64  gcc 4.1.2 -O2
		bar(x);
}

int main () {
    foo(0);
    return 0;
}



/*
asm code:
foo:
        pld     BYTE PTR [%rdi]
        jmp     bar
*/
