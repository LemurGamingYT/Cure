#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


typedef struct {
    int data;
    struct DoublyLinkedNode* previous;
    struct DoublyLinkedNode* next;
} DoublyLinkedNode;

typedef struct {
    DoublyLinkedNode* head;
} DoublyLinkedList;


typedef struct {
    int* data;
    int front;
    int rear;
    size_t capacity;
    size_t size;
} Queue;


Queue create_queue(size_t capacity) {
    Queue queue = {
        .front = 0, .rear = capacity - 1, .size = 0, .capacity = capacity,
        .data = (int*)malloc(capacity * sizeof(int))
    };
    if (queue.data == NULL) {
        printf("out of memory\n");
        exit(1);
    }

    return queue;
}

bool queue_is_full(Queue queue) {
    return queue.size == queue.capacity;
}

bool queue_is_empty(Queue queue) {
    return queue.size == 0;
}

bool queue_enqueue(Queue* queue, int item) {
    if (queue_is_full(*queue)) {
        return false;
    }

    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->data[queue->rear] = item;
    queue->size++;
    return true;
}

int queue_dequeue(Queue* queue) {
    if (queue_is_empty(*queue)) {
        return -1;
    }

    int item = queue->data[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;
    return item;
}

void queue_free(Queue* queue) {
    if (queue->data) {
        free(queue->data);
    }
}

int main() {
    Queue queue = create_queue(25);
    for (int i = 0; i < 25; i++) {
        queue_enqueue(&queue, i);
    }
    
    printf("%d\n", queue_dequeue(&queue));

    queue_free(&queue);
    return 0;
}
