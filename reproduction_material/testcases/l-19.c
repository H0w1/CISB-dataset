/*
	x86-64 gcc4.8-4.9 -O2
	Compile and run the program, if the result is not "ok", there is a bug.
*/

#include <stdio.h>
#include <sys/mman.h>
#include <error.h>
// #define PROT_READ 1
#define errno 1

int g_1 = 1;

int g_2[1024] __attribute__((section ("safe_section"), aligned (4096)));

int c = 4;

int __attribute__ ((noinline)) foo (void){
	int l;
	for (l = 0; (l != 4); l++) {
	  if (g_1)
		return l;
	  for (g_2[0] = 0; (g_2[0] >= 26); ++g_2[0])
		;
	}
	return 2;
}

int main (int argc, char* argv[])
{
	if (mprotect (g_2, sizeof(g_2), PROT_READ) == -1){
		int e = errno;
		error (e, e, "mprotect error %i", e);
	}
	foo ();
	__builtin_printf("ok");
	return 0;
}