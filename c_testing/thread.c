#include <stdio.h>

#include "../include/tinycthread/tinycthread.h"


static int thread_func(void* arg) {
    printf("Hello from thread!\n");
    return 0;
}

static int thread_func2(void* arg) {
    printf("Testing number from thread2: %d\n", (int*)arg);
    return 0;
}


int main() {
    thrd_t thread1;
    int thread_code = thrd_create(&thread1, (thrd_start_t)thread_func, NULL);
    if (thread_code == thrd_success) {
        printf("Thread created successfully!\n");
    }

    thrd_t thread2;
    int thread_code2 = thrd_create(&thread2, (thrd_start_t)thread_func2, (void*)42);
    if (thread_code2 == thrd_success) {
        printf("Thread 2 created successfully!\n");
    }

    thrd_join(thread2, NULL);
    thrd_join(thread1, NULL);

    thrd_detach(thread1);
    thrd_detach(thread2);
    return 0;
}
