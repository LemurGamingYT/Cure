// This file shows the use of the Cure compiler in C

// Include the main cure header file (relative to the current directory)
#include "../../compiler/cure.h"


// Define the main function
int main() {
    // Call the sqrt function and print the result
    printf("%s\n", Float_repr(Math_sqrt(25.0)));

    // Call the pow function and print the result
    printf("%s\n", Float_repr(Math_pow(5.0, 2.0)));

    return 0; // Return 0 to indicate success
}
