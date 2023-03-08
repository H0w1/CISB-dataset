/* https://github.com/torvalds/linux/commit/04ef0f1a0169a14b8e653af1178524ab4390133f */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct a {                   // with attribute res donot change
    int num2;
    int num3;
}__attribute__((aligned(4)));

struct b{
    int a;
    struct a stru;
};

int main(){
    struct a a1 = {1, 2};
    struct a *p = (struct a*)malloc(sizeof(struct a));
    memcpy(&p->num2, &a1.num2, 8);                  // with arm64 gcc/clang -O0, memcpy chenged to ldr xreg

    printf("%d %d", p->num2, p->num3);

    return 0;
}