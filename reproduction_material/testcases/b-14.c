/*successful
    x86-64 gcc 4.1-trunk -O0
    x86-64 clang 3.0.0-trunk -O1
    Compilers will use puts instead of printf, and the argument of puts can't be null.
*/
#include<stdio.h>
int main ()
{
        printf ("%s\n", ((void *)0));
        return 0;
}