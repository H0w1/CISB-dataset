#include <stdio.h>

/*
	arm
*/

typedef struct structA{
    int a;
    int b;
    int c;
}A;

typedef struct structB{
    int iData;
    A a;
}B;

int test(A aa)
{
    aa.a = 123;
    aa.b = 321;
    aa.c = 213;
    printf("\r\n line:%d func:%s [%d][%d][%d]\r\n", __LINE__, __FUNCTION__, aa.a, aa.b, aa.c);
    return 0;
}

int main()
{
    char buf[1024];
    A aaa = {1,2,3};

    B *pb = (B *)(buf + 1);
    pb->a = aaa;
    test(pb->a);
    return 0;
}