#include "builtins.h"


Ref* Ref_new(pointer data, RefFunction destroy_fn) {
    Ref* ref = (Ref*)heap_alloc(sizeof(Ref));
    ref->destroy_fn = destroy_fn;
    ref->ref_count = 1;
    ref->data = data;
    return ref;
}

nil Ref_inc(Ref* ref) {
    ref->ref_count++;
    return NIL;
}

nil Ref_dec(Ref* ref) {
    ref->ref_count--;
    if (ref->ref_count == 0) {
        if (ref->destroy_fn == NIL)
            heap_free(ref->data);
        else
            ref->destroy_fn(ref->data);
        
        ref->data = NIL;
        heap_free(ref);
    }
    
    return NIL;
}
