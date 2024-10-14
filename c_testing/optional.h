#ifndef CUREUI_OPTIONAL_H
#define CUREUI_OPTIONAL_H


#ifdef __cplusplus
extern "C" {
#endif


#include <stdbool.h>


#define OPT(T) typedef struct { T* value; } T##_opt_t;\
T##_opt_t T##_opt_new(T* value) { return (T##_opt_t){ .value = value }; }\
bool T##_opt_is_nil(T##_opt_t opt) { return opt.value == NULL; }


#ifdef __cplusplus
}
#endif


#endif
