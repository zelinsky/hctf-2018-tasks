#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 32

signed char array[MAX_SIZE] = {0};

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    for(;;) {
        int index;
        signed char value;
        
        printf("give me an index:\n> ");
        if (scanf("%d", &index) != 1)
            exit(-1);

        if (index >= MAX_SIZE)
            continue;

        printf("the value at %d is %hhd. give me a new value:\n> ", index, array[index]);
        if (scanf("%hhd", &value) != 1)
            exit(-1);

        array[index] = value;
    }
}

