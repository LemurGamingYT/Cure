#include <stdlib.h>
#include <string.h>
#include "allocators.h"

// Page Allocator Implementation
struct PageAllocator {
    size_t page_size;
    void** free_pages;
    size_t free_count;
    size_t capacity;
};

PageAllocator* page_allocator_create(size_t page_size) {
    PageAllocator* alloc = malloc(sizeof(PageAllocator));
    alloc->page_size = page_size;
    alloc->capacity = 16;  // Initial capacity
    alloc->free_count = 0;
    alloc->free_pages = malloc(sizeof(void*) * alloc->capacity);
    return alloc;
}

void* page_alloc(PageAllocator* alloc) {
    if (alloc->free_count > 0) {
        return alloc->free_pages[--alloc->free_count];
    }
    return malloc(alloc->page_size);
}

void page_free(PageAllocator* alloc, void* ptr) {
    if (alloc->free_count == alloc->capacity) {
        alloc->capacity *= 2;
        alloc->free_pages = realloc(alloc->free_pages, sizeof(void*) * alloc->capacity);
    }
    alloc->free_pages[alloc->free_count++] = ptr;
}

void page_allocator_destroy(PageAllocator* alloc) {
    for (size_t i = 0; i < alloc->free_count; i++) {
        free(alloc->free_pages[i]);
    }
    free(alloc->free_pages);
    free(alloc);
}

// Arena Allocator Implementation
struct ArenaAllocator {
    void* memory;
    size_t size;
    size_t used;
};

ArenaAllocator* arena_allocator_create(size_t size) {
    ArenaAllocator* alloc = malloc(sizeof(ArenaAllocator));
    alloc->memory = malloc(size);
    alloc->size = size;
    alloc->used = 0;
    return alloc;
}

void* arena_alloc(ArenaAllocator* alloc, size_t size) {
    if (alloc->used + size > alloc->size) {
        return NULL;
    }
    void* ptr = (char*)alloc->memory + alloc->used;
    alloc->used += size;
    return ptr;
}

void arena_reset(ArenaAllocator* alloc) {
    alloc->used = 0;
}

void arena_allocator_destroy(ArenaAllocator* alloc) {
    free(alloc->memory);
    free(alloc);
}

// Fixed Buffer Allocator Implementation
struct FixedBufferAllocator {
    void* buffer;
    size_t size;
    size_t used;
};

FixedBufferAllocator* fixed_buffer_allocator_create(void* buffer, size_t size) {
    FixedBufferAllocator* alloc = malloc(sizeof(FixedBufferAllocator));
    alloc->buffer = buffer;
    alloc->size = size;
    alloc->used = 0;
    return alloc;
}

void* fixed_buffer_alloc(FixedBufferAllocator* alloc, size_t size) {
    if (alloc->used + size > alloc->size) {
        return NULL;
    }
    void* ptr = (char*)alloc->buffer + alloc->used;
    alloc->used += size;
    return ptr;
}

void fixed_buffer_reset(FixedBufferAllocator* alloc) {
    alloc->used = 0;
}

void fixed_buffer_allocator_destroy(FixedBufferAllocator* alloc) {
    free(alloc);
}
