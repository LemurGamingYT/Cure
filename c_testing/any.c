#include <windows.h>
#include <stdlib.h>
#include <stdio.h>


int main() {
    int x = 50;
    void* ptr = &x;

    HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, GetCurrentProcessId());
    if (handle == NULL) {
        printf("Failed to open process\n");
        return 1;
    }

    int newValue = 100;
    if (!WriteProcessMemory(handle, ptr, &newValue, sizeof(x), NULL)) {
        printf("Failed to write process memory\n");
        CloseHandle(handle);
        return 1;
    }

    int oldValue;
    if (!ReadProcessMemory(handle, ptr, &oldValue, sizeof(x), NULL)) {
        printf("Failed to read process memory\n");
        CloseHandle(handle);
        return 1;
    }

    printf("Old value: %d\n", oldValue);
    printf("%d\n", x);

    CloseHandle(handle);
    return 0;
}
