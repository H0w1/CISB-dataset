/*
	x86-64 gcc4.5.3-7.1 -O2 
	x86-64 8-12.0.1 -O1
	arm gcc4-7 O2 
	arm gcc8- O1
	Compile and get disassembly code of this program. If sections "<bad_code>:" doesn't contains "test", there is a bug.
*/

#include <stdio.h>
#include <stdlib.h>

void bad_code(void *a)
{
   int *b = a;
   int c = *b;
   static int d;

   if (b) {
      d = c;
   }
   printf("%d\n",d);
}

int main(int argc, char** argv){
	int a = atoi(argv[1]);
	bad_code(&a);
}