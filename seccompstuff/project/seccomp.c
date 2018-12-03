#define _GNU_SOURCE 1
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>

#include <sys/prctl.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <linux/unistd.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

#define PAGE_SIZE 0x1000

/* if syscall nr == __NR_##name return allow, otherwise jump to next instruction. */
#define ALLOW_SYSCALL(name) \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, __NR_##name, 0, 1), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW)


int enable_security(void)
{
    struct sock_filter filter[] = {
        /* load syscall nr */
        BPF_STMT(BPF_LD+BPF_W+BPF_ABS, offsetof(struct seccomp_data, nr)),
        /* allow read and write */
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        /* required by us */
        ALLOW_SYSCALL(mmap),
        ALLOW_SYSCALL(mprotect),
        /* fstat required by printf */
        ALLOW_SYSCALL(fstat),
        /* munmap required by free */
        ALLOW_SYSCALL(munmap),
        /* brk required by malloc */
        ALLOW_SYSCALL(brk),
        /* exit_group required for a clean exit */
        ALLOW_SYSCALL(exit_group),
        /* no matches? return kill. */
        BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL),
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
        .filter = filter,
    };

    struct rlimit limit;
    
    
    /* set some RAM (8MiB) and CPU (1s) resource limits first */
    if (getrlimit(RLIMIT_AS, &limit) != 0) {
        return 1;
    }
    limit.rlim_cur = 0x800000;
    limit.rlim_max = 0x800000;
    if (setrlimit(RLIMIT_AS, &limit) != 0) {
        return 1;
    }
    if (getrlimit(RLIMIT_CPU, &limit) != 0) {
        return 1;
    }
    limit.rlim_cur = 1;
    limit.rlim_max = 1;
    if (setrlimit(RLIMIT_CPU, &limit) != 0) {
        return 1;
    }
    
    /* enable seccomp */
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        return 1;
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        return 1;
    }
    return 0;
}

int main()
{
    void *code = NULL;
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    /* better be safe. */
    if (enable_security())
        return 1;
    
    code = mmap(NULL, PAGE_SIZE, PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (code == MAP_FAILED)
        return 2;
    
    printf("%s", "How many bytes can I expect?\n");
    unsigned int nb;
    if (scanf("%u%*c", &nb) != 1 || !nb || nb > PAGE_SIZE)
        return 3;
    
    printf("Okay. Waiting for %u bytes.\n", nb);
    if (fread(code, 1, nb, stdin) != nb)
        return 4;
    
    if (mprotect(code, PAGE_SIZE, PROT_READ | PROT_EXEC))
        return 5;
    
    printf("%s", "Lets go!\n");
    ((void(*)())code)();
    
    munmap(code, PAGE_SIZE);
    
    return 0;
}
