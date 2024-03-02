// This file shows the use of the Cure compiler in C

// Include the main cure header file (relative to the current directory)
#include "../../compiler/cure.h"


// Define a new struct type called Vector2
typedef struct {
    Int x;
    Int y;
} Vector2;


// Define a repr function for the Vector2 type
String Vector2_repr(Vector2 v) {
    // Concatenate strings into (v.x, v.y)
    return String_add_String(String_add_String(
        String_add_String(
            String_add_String("(", Int_repr(v.x)), ", "
        ), Int_repr(v.y)), ")"
    );
}


// Define the main function
int main() {
    // Create a new Vector2
    Vector2 v = {.x = 5, .y = 10};

    // Print the Vector2
    printf("%s\n", Vector2_repr(v));

    return 0; // Return 0 to indicate success
}
