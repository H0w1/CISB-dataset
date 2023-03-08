/*successful
    x86-64 gcc 4.1-7.4 -O1 gcc 8-12 -O0
    x86-64 clang 3.0.0-14.0.0 -O1
    Compile and run the executable file，input 2147483647. If the output is "ok", then check "if (a + 10 > a)" is removed and there is a bug.
*/
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) int test(int a) {
    if (a + 10 > a) {   // removed
        puts("ok");
    }
    return 0;
}

int main(int argc, char* argv[]){
    int a = 2147483640;
    test(a);
    return 0;
}