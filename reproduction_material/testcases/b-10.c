/*
	x86-64 gcc4.6.4-12.0.1 -O1; 4.4 -O2
	x86-64 clang 3.0.0-14.0.0 -O1
	Compile and get disassembly code of this program. If section "<main>:" doesn't contains instruction "cmp", "while (x<10000000000)" is removed,so there is a bug.
*/

#include    <stdio.h>

int main (void)
{
    int x=0, y=0;
    long z=0;
    
    for (; y<10000000; y++) {
        
        if (y%7 == 0)
            continue;
               
        x = 0;
                
        while (x<10000000000) {  // KEY LINE - see below
            
            x++;
            z+=1;
        }
    }
    
    printf ("%li\n", z);
    
    return  0;
}