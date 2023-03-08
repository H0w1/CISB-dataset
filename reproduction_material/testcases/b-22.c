#include<stdio.h>

union U {
       struct {
               int a;
               int b;
               int c;
       };
       struct {
               int s1;
               int s2;
               int s3;
               int s4;
       };
};

// void foo(union U *);
void bar(int a, int b)
{   
    char c = 'a';
    printf("%s\n", &c);
    // memset(&c, 1, 20);
    union U u = {
            .a = a,
            .b = b
    };
    printf("%p\n", &u);
    printf("a:%d\n", u.a);
    printf("b:%d\n", u.b);
    printf("s3:%d\n", u.s3);
    printf("s4:%d", u.s4);
    
    
    // foo(&u);
}

int main() {
    bar(1, 2);
    return 0;
}