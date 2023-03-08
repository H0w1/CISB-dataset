/*
	x86-64 gcc4.1-12.0.1 -O1
	x86-64 clang3.0.0-14.0.0 -O1
	Compile and run the program, if output is "ok", it means assert(a+100 > a) is removed, so there is a bug.
*/
#include <assert.h>
#include <stdio.h>

__attribute__((noinline))
int foo(int a) {
  assert(a+100 > a);
  printf("ok\n");
  return a;
}

int main() {
//   foo(100);
  foo(0x7fffffff);
  return 0;
}
