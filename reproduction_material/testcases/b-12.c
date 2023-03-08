#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

/*
For Linux the correct command is: gcc -pthread b_12.c
in O3 it is in the assembly code      
.L7:
jmp .L7
so there is a bug.
in O2/O1, "if(x==y)" is deleted, so the program would never stop
*/


int x = 23;
int y = 29;

void* set_x(void* arg)
{
    (void)arg;
    x = 29;

    return NULL;
}

int main(void)
{

        pthread_t p1;

        pthread_create(&p1, NULL, set_x, NULL);
        pthread_detach(p1);
        while (x < y)
                if (x == y)
                        break;

        return 0;
}
