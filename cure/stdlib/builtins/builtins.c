#include "builtins.h"

#include <limits.h>
#include <float.h>


int int_min(void) { return INT_MIN; }
int int_max(void) { return INT_MAX; }

float float_min(void) { return FLT_MIN; }
float float_max(void) { return FLT_MAX; }
