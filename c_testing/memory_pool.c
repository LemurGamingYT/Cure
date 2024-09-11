#include <stdlib.h>
#include <string.h>
#include <stdio.h>


void error(const char* msg) {
    printf("Error: %s\n", msg);
    exit(1);
}


typedef struct {
    void** blocks;
    size_t block_size;
    size_t used;
} MemoryPool;


MemoryPool* pool_create(size_t block_size) {
    MemoryPool* pool = malloc(sizeof(MemoryPool));
    if (pool == NULL) {
        error("Failed to allocate memory pool");
    }

    pool->blocks = malloc(block_size);
    if (pool == NULL) {
        error("Failed to allocate memory pool");
    }

    pool->block_size = block_size;
    pool->used = 0;

    return pool;
}

void pool_destroy(MemoryPool* pool) {
    free(pool->blocks);
    free(pool);
}

void pool_allocate(MemoryPool* pool, void* ptr) {
    if (pool->used >= pool->block_size) {
        error("Pool is full");
    }

    pool->blocks[pool->used++] = ptr;
}

void pool_deallocate(MemoryPool* pool, size_t index) {
    if (index >= pool->used) {
        error("Index out of bounds");
    }

    pool->used--;
    pool->blocks[index] = NULL;
}

void* pool_get(MemoryPool* pool, size_t index) {
    if (index >= pool->used) {
        error("Index out of bounds");
    }

    return pool->blocks[index];
}


int main() {
    const int block_size = 1024 * 1024 * 50;
    MemoryPool* pool = pool_create(block_size); // 50 MB

    for (int i = 0; i < block_size; i++) {
        pool_allocate(pool, &i);
    }

    for (int i = 0; i < block_size; i++) {
        printf("Block %d: %p\n", i, pool_get(pool, i));
    }

    pool_destroy(pool);
    return 0;
}