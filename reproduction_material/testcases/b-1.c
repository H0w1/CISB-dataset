#include<stdio.h>
/*
"if ((!s1 && s2) || (s1 && !s2))" will be removed in 4.1.2-10.1 -O1. We can check the disassembly code if section ""<strcmp>:" contains instruction "test   %rdi,%rdi" as it corresponds to "if ((!s1 && s2) || (s1 && !s2))".
*/
int strcmp (const char *s1, const char *s2)
{

    if ((!s1 && s2) || (s1 && !s2))
        return (int) (s1 - s2);

    if (s1 == s2)
        return 0;

    while (*s1 == *s2++)
        if (*s1++ == '\0')
             return 0;

    return (*(unsigned char *)s1 - *(unsigned char *)--s2);
}

int main(int argc, char** argv){
    // char *p = NULL;
    // char *q = "aaa";
    char *p = argv[1];
    char *q = argv[2];
    int a  = strcmp(p,q);
    printf("%d", a);//output is -4202500
    //printf("ok\n");
}