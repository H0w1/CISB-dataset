/*successful
    X86-64 gcc 4.1.2-10.1 -O2
    x86-64 clang 3.0-14.0.0 -O1
    Compile and get disassembly code of this program. If section "<main>:" doesn't contains instruction "cmpl   $0x0,"， check "if (g == 0" is removed, so there is a bug.
*/
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>

int main(int argc, char** argv) {
    int size;
    //input 32
    size = atoi(argv[1]);
    int g = 0;
    g = 1 << size;
    if (g == 0 || g == 1)
        printf("%d\n", g);
    return 0;
}