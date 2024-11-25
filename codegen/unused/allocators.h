#ifndef ALLOCATORS_H
#define ALLOCATORS_H

#include <stddef.h>
#include <stdint.h>

// Page Allocator
typedef struct PageAllocator PageAllocator;
PageAllocator* page_allocator_create(size_t page_size);
void* page_alloc(PageAllocator* alloc);
void page_free(PageAllocator* alloc, void* ptr);
void page_allocator_destroy(PageAllocator* alloc);

// Arena Allocator
typedef struct ArenaAllocator ArenaAllocator;
ArenaAllocator* arena_allocator_create(size_t size);
void* arena_alloc(ArenaAllocator* alloc, size_t size);
void arena_reset(ArenaAllocator* alloc);
void arena_allocator_destroy(ArenaAllocator* alloc);

// Fixed Buffer Allocator
typedef struct FixedBufferAllocator FixedBufferAllocator;
FixedBufferAllocator* fixed_buffer_allocator_create(void* buffer, size_t size);
void* fixed_buffer_alloc(FixedBufferAllocator* alloc, size_t size);
void fixed_buffer_reset(FixedBufferAllocator* alloc);
void fixed_buffer_allocator_destroy(FixedBufferAllocator* alloc);

#endif
