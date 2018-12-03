#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    printf("Welcome to the echo chamber!\n");
    for (;;) {
        char *str;
        if (scanf("%ms", &str) != 1 || !strcmp(str, "q"))
            break;
        printf(str);
        free(str);
    }
    
    char *q1 = malloc(50);
    printf("Was it fun?\n");
    scanf("%50s", q1);
    
    char *q2 = malloc(50);
    printf("Would you echo again?\n");
    scanf("%50s", q2);
    
    printf("k. Bye.\n");
    free(q2);
    free(q1);
    return 0;
}
