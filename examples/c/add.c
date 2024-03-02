// This file shows the use of the Cure compiler in C

// Include the main cure header file (relative to the current directory)
#include "../../compiler/cure.h"


// Define a function that returns adds two Ints using the Cure API
Int add(Int a, Int b) {
    return Int_add_Int(a, b);
}


// Define the main function, you can use the Int or int type
int main() {
    // Call the add function and print the result
    printf("%s\n", Int_repr(add(5, 5)));
    return 0; // Return 0 to indicate success
}
