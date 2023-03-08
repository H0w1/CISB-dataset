#include<stdio.h>

const int b;

int main(){

    *(int*) &b = 100;
    // int *p = &a;
    // *p = 100;
    printf("%d", b);
    return 0;
}