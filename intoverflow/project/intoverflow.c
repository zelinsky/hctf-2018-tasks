#include <stdio.h>
#include <stdlib.h>

void givemeshellpls() {
    system("/bin/sh");
}

void dologic(char buf[], int a, int b) {
    for (int y = 0; y < b; y++) {
        for (int x = 0; x < a; x++) {
            buf[y * a + x] = (char) (buf[x] + y);
        }
    }

    for (int n = a * b - 1; n >= 0; n--) {
        printf("%c", buf[n]);
        if (!(n % a))
            printf("\n");
    }
}

typedef struct localdata_s {
    char buf[1024];
    void (*dologicptr)(char [], int, int);
    int a, b;
} localdata;

int main() {
    localdata d;
    d.dologicptr = dologic;
    
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    puts("Please enter width and height e.g.: 5 8");
    if (fscanf(stdin, "%d %d", &d.a, &d.b) != 2) {
        puts("Error! Invalid width / height provided.");
        return -1;
    }

    if ((size_t)(d.a * d.b) > sizeof(d.buf)) {
        puts("Sorry! Values are too big for the buffer. Please choose smaller values.");
        return -2;
    }

    puts("Please provide some data e.g.: 12345");
    while(fgetc(stdin) != '\n');
    fread(d.buf, 1, (size_t) d.a, stdin);
    
    d.dologicptr(d.buf, d.a, d.b);

    return 0;
}
