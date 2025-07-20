#include "tinycthread/source/tinycthread.h"
#include "builtins/builtins.h"


typedef struct {
    int x, y;
} thread_arg_t;


int hello_thread(void* arg) {
    thread_arg_t* t = (thread_arg_t*)arg;
    printf("Thread produced: %d\n", t->x + t->y);
    return 0;
}


int main(void) {
    thread_arg_t a = {1, 2};
    thrd_t t;
    if (thrd_create(&t, hello_thread, &a) != thrd_success)
        perror("Failed to create thread");
    
    thrd_join(t, NULL);
    printf("Main thread: %d\n", a.x + a.y);
    return 0;
}
