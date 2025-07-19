#include "builtins.h"

#define _USE_MATH_DEFINES
#include <math.h>


float Math_pi(void) { return M_PI; }
float Math_e(void) { return M_E; }
float Math_pow(float base, float exponent) { return powf(base, exponent); }
int Math_pow_0(int base, int exponent) { return (int)powf((float)base, (float)exponent); }
float Math_sqrt(float x) { return sqrtf(x); }
int Math_sqrt_1(int x) { return (int)sqrtf((int)x); }
float Math_min(float a, float b) { return fminf(a, b); }
int Math_min_2(int a, int b) { return (int)fminf((int)a, (int)b); }
float Math_max(float a, float b) { return fmaxf(a, b); }
int Math_max_3(int a, int b) { return (int)fmaxf((int)a, (int)b); }
