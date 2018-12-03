#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void printmenu(unsigned int coins) {
    printf("Select your action! (coins : %u)\n[ 1 ] : malloc\n[ 2 ] : free\n[ 3 ] : write\n[ 4 ] : bye!\n", coins);
}

unsigned long readnum() {
    unsigned long res;
    if (scanf("%lu%*c", &res) != 1)
        exit(-1);
    return res;
}

void *slot_malloc() {
    puts("How much?");
    return malloc(readnum());
}

void slot_free(char *ref) {
    puts("Where?");
    free(&ref[readnum()]);
}

void slot_write(char *ref) {
    puts("What?");
    read(STDIN_FILENO, ref, 8);
}

void slot_bye() {
    puts("Baiii");
    exit(0);
}

int main() {
    int coins = 7;
    void *addr = NULL;
    
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    printf("Hi!\nYou currently have %d coins!. With each coin you can either malloc, free or do an 8-byte write on the heap! good luck!\nHere is system : %p\n", coins, system);
    while(coins > 0) {
        printmenu(coins);
        switch(readnum()) {
            case 1:
                addr = slot_malloc();
                break;
            case 2:
                slot_free(addr);
                break;
            case 3:
                slot_write(addr);
                break;
            case 4:
                slot_bye();
                break;
            default:
                break;
        }
        coins--;
    }
    slot_bye();
}
